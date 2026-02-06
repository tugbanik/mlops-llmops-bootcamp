from __future__ import annotations

import math
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parents[1] / "data/app.db"
REPORT_PATH = Path(__file__).resolve().parents[1] / "reports" / "summary.md"


def wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a proportion."""
    if n == 0:
        return (0.0, 0.0)
    phat = successes / n
    denom = 1 + (z**2) / n
    center = (phat + (z**2) / (2 * n)) / denom
    margin = (z * math.sqrt((phat * (1 - phat) / n) + (z**2) / (4 * n**2))) / denom
    return (max(0.0, center - margin), min(1.0, center + margin))


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # counts
    cur.execute("SELECT COUNT(*) FROM interaction;")
    n_interactions = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM feedback;")
    n_feedback = cur.fetchone()[0]

    # rating stats
    cur.execute("SELECT AVG(rating), MIN(rating), MAX(rating) FROM feedback;")
    avg_rating, min_rating, max_rating = cur.fetchone()
    avg_rating = float(avg_rating) if avg_rating is not None else None

    # share of positive feedback (>=4)
    cur.execute("SELECT COUNT(*) FROM feedback WHERE rating >= 4;")
    n_pos = cur.fetchone()[0]
    pos_rate = (n_pos / n_feedback) if n_feedback else 0.0
    ci_low, ci_high = wilson_ci(n_pos, n_feedback) if n_feedback else (0.0, 0.0)

    # top questions (simple)
    cur.execute(
        "SELECT question, COUNT(*) as c FROM interaction GROUP BY question ORDER BY c DESC LIMIT 5;"
    )
    top_questions = cur.fetchall()

    conn.close()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    md = []
    md.append("# Bootcamp MVP – Daily Summary\n")
    md.append(f"- Generated at: **{now}**\n")
    md.append("\n## Usage\n")
    md.append(f"- Total interactions: **{n_interactions}**\n")
    md.append(f"- Total feedback: **{n_feedback}**\n")

    md.append("\n## Feedback Quality (Statistical)\n")
    if avg_rating is None:
        md.append("- No feedback yet.\n")
    else:
        md.append(f"- Average rating: **{avg_rating:.2f}** (min={min_rating}, max={max_rating})\n")
        md.append(
            f"- Positive feedback rate (rating ≥ 4): **{pos_rate:.2%}** "
            f"with 95% CI (Wilson): **[{ci_low:.2%}, {ci_high:.2%}]**\n"
        )

    md.append("\n## Top Questions\n")
    if not top_questions:
        md.append("- No interactions yet.\n")
    else:
        for q, c in top_questions:
            md.append(f"- ({c}) {q}\n")

    REPORT_PATH.write_text("".join(md), encoding="utf-8")
    print(f"Report written: {REPORT_PATH}")


if __name__ == "__main__":
    main()
