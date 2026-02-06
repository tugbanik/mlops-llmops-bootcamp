from __future__ import annotations
from typing import List


def generate_answer(question: str, label: str, docs: List[object]) -> str:
    """
    MVP generator:
    - docs içinden en iyi 2 parçayı al (retriever zaten sorted döndürüyor varsayıyoruz)
    - label'a göre kısa şablon üret
    - administrative ise örnek haftalık mesaj ekle
    - kaynak snippet + skor ekle
    """

    picked = docs[:2] if docs else []

    sources = []
    for d in picked:
        doc_id = getattr(d, "doc_id", "unknown")
        score = float(getattr(d, "score", 0.0))

        content = getattr(d, "content", None)
        if content is None:
            content = getattr(d, "chunk", "")

        snippet = str(content or "").strip().replace("\n", " ")
        snippet = snippet[:140] + ("..." if len(snippet) > 140 else "")
        sources.append(f"- ({doc_id}, score={score:.3f}) {snippet}")

    # plan (label bazlı)
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
        # administrative veya diğerleri buraya düşsün
        plan = (
            "Öneri planı (idari):\n"
            "1) Kısa-nezih iletişim taslağı.\n"
            "2) Ölçülebilir BEP hedefi (davranış/koşul/kriter).\n"
        )

    # administrative için ekstra çıktı
    extra = ""
    if label == "administrative":
        extra = (
            "\nÖrnek haftalık mesaj:\n"
            "Merhaba,\n"
            "Bu hafta [davranış/hedef] alanında [kısa ölçülebilir ilerleme] gözlemledik.\n"
            "Etkili olan destek: [görsel ipucu/zamanlayıcı/pekiştireç].\n"
            "Önümüzdeki hafta hedefimiz: [tek hedef].\n"
            "Saygılarımla.\n"
        )

    answer = (
        f"Soru: {question}\n"
        f"Etiket (ML tahmini): {label}\n\n"
        f"{plan}"
        f"{extra}\n"
        "İlgili doküman parçaları:\n"
        + ("\n".join(sources) if sources else "- (kaynak bulunamadı)")
    )
    return answer
