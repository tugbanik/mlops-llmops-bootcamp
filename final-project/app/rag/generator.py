from __future__ import annotations
from typing import List

# retriever'daki dataclass'ı import ediyorsan kalsın; şart değil
# from app.rag.retriever import RetrievedDoc


def generate_answer(question: str, label: str, docs: List[object]) -> str:
    """
    MVP generator:
    - docs içinden en iyi 2 parçayı al
    - label'a göre kısa şablon öneri üret
    - kaynak snippet'larını ekle

    Not: RetrieverDoc alan adı 'text' değilse 'content' kullanıyoruz.
    """

    picked = docs[:2] if docs else []

    sources = []
    for d in picked:
        # doc_id / score bekliyoruz
        doc_id = getattr(d, "doc_id", "unknown")
        score = float(getattr(d, "score", 0.0))

        # !!! kritik fix: retriever doc'u 'content' alanı ile geliyor
        content = getattr(d, "content", None)
        if content is None:
            # güvenlik için: bazen 'chunk' diye yazmış olabilirsin
            content = getattr(d, "chunk", "")

        snippet = str(content or "").strip().replace("\n", " ")
        snippet = snippet[:140] + ("..." if len(snippet) > 140 else "")
        sources.append(f"- ({doc_id}, score={score:.3f}) {snippet}")

    if label == "support":
        plan = (
            "Öneri planı (destek):\n"
            "1) Uyaranı azalt (ses/ışık/kalabalık), yönergeleri tek cümle yap.\n"
            "2) 2 dakikalık regülasyon: 4-6 nefes + duvar itme / sıkıştırma topu.\n"
            "3) Görsel ipucu + zamanlayıcı ile geçişleri yönet (önceden haber ver).\n"
            "4) Krizde: güvenlik → düşük ses → A/B seçeneği (kontrol duygusu).\n"
        )
    elif label == "education":
        plan = (
            "Öneri planı (eğitim):\n"
            "1) 10–15 dk mikro hedef + 2 dk mola.\n"
            "2) Tek beceri: örnek → birlikte → bağımsız deneme.\n"
            "3) Başarıyı anlık pekiştir (davranış odaklı övgü).\n"
        )
    elif label == "health":
        plan = (
            "Öneri planı (iyi oluş):\n"
            "1) Duygu/beden sinyalini adlandır (0–10 ölçeği).\n"
            "2) 60–90 sn kutu nefesi (4-4-4-4).\n"
            "3) Sakin köşe + kısa hareket (germe/yürüme).\n"
        )
    else:
        plan = (
            "Öneri planı (idari):\n"
            "1) Kısa-nezih iletişim taslağı.\n"
            "2) Ölçülebilir BEP hedefi (davranış/koşul/kriter).\n"
        )

    answer = (
        f"Soru: {question}\n"
        f"Etiket (ML tahmini): {label}\n\n"
        f"{plan}\n"
        "İlgili doküman parçaları:\n"
        + ("\n".join(sources) if sources else "- (kaynak bulunamadı)")
    )
    return answer
