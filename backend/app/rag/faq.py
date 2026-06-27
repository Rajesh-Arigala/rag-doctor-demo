from __future__ import annotations

from app.rag.text import terms

FAQ_ANSWERS = [
    (
        {"how successful is ivf", "ivf success", "success rate", "success rates"},
        "💖 **IVF success** depends on age, egg and sperm quality, underlying health conditions, and the reason for infertility.\n✨ Women under 35 are mentioned as having higher success rates, around 40–50% per cycle.\n🩺 Success can gradually decline in the late 30s and 40s due to reduced egg quality and quantity.\n📅 For a realistic estimate, Dr. Madhu Patil’s Clinic can review your reports and history during consultation.",
        "WEB-DRMADHU-001",
    ),
    (
        {"improve my fertility before treatment", "improve fertility", "before treatment", "prepare body for ivf"},
        "💖 **Before treatment**, lifestyle preparation can support egg and sperm health.\n✨ Dr. Madhu Patil’s Clinic recommends a healthy balanced diet, optimal weight, moderate exercise, good sleep, and stress management.\n🩺 It also mentions avoiding smoking, limiting alcohol/caffeine, taking prenatal vitamins with folic acid, completing screenings, and reducing environmental toxin exposure.\n📅 Dr. Madhu Patil’s Clinic can personalize these steps based on your age, history, and reports.",
        "WEB-DRMADHU-001",
    ),
    (
        {"what age should i start thinking about fertility", "age should i start", "thinking about fertility", "fertility age"},
        "💖 **Fertility planning** is especially important as fertility naturally starts declining with age, particularly after 35.\n✨ Women in the late 20s and early 30s are mentioned as generally having better fertility potential.\n🩺 If pregnancy is being delayed or there are medical concerns, fertility assessment, ovarian reserve testing, or fertility preservation may be considered earlier.\n📅 Dr. Madhu Patil’s Clinic can guide the right timing based on personal goals and health history.",
        "WEB-DRMADHU-001",
    ),
    (
        {"what can be done after a failed ivf cycle", "failed ivf", "after failed ivf", "ivf cycle fails"},
        "💖 **After a failed IVF cycle**, further evaluation can help identify possible reasons.\n✨ Dr. Madhu Patil’s Clinic mentions hysteroscopy, ERA, PGT-A, sperm DNA fragmentation tests, hormonal evaluation, and immunological profile assessment.\n🩺 These tests can help review embryo quality, uterine environment, sperm integrity, hormonal balance, or immune-related factors.\n📅 Dr. Madhu Patil’s Clinic can suggest the next step after reviewing the previous cycle details.",
        "WEB-DRMADHU-001",
    ),
    (
        {"normal pregnancy and delivery after ivf", "normal pregnancy", "delivery after ivf", "pregnancy after ivf"},
        "💖 **Many women who conceive through IVF can have a normal healthy pregnancy and delivery.**\n✨ Dr. Madhu Patil’s Clinic notes that early pregnancy often needs close monitoring and hormonal support.\n🩺 Some risks may be higher depending on age or underlying fertility issues, but overall health and history matter a lot.\n📅 Dr. Madhu Patil’s Clinic can guide monitoring and delivery planning after reviewing your case.",
        "WEB-DRMADHU-001",
    ),
    (
        {"treatment options for men with low sperm count", "low sperm count", "male low sperm"},
        "💖 **Low sperm count** can still have treatment options after proper evaluation.\n✨ Dr. Madhu Patil’s Clinic mentions lifestyle modification, medical therapy for hormonal or underlying conditions, and assisted reproductive techniques.\n🩺 IUI may help in mild cases, while IVF with ICSI can help even when sperm count is very low.\n📅 Dr. Madhu Patil’s Clinic can recommend the right pathway after semen analysis and related tests.",
        "WEB-DRMADHU-001",
    ),
    (
        {"treatment options for men with zero sperm count", "zero sperm count", "azoospermia"},
        "💖 **Zero sperm count**, also called azoospermia, needs evaluation to understand the cause.\n✨ Dr. Madhu Patil’s Clinic mentions obstructive and non-obstructive causes, with options such as medical or hormonal therapy and surgical correction in selected cases.\n🩺 Advanced sperm retrieval options such as TESA, TESE, or micro-TESE may be considered, followed by IVF with ICSI if sperm are retrieved.\n📅 Dr. Madhu Patil’s Clinic can guide this after detailed male fertility evaluation.",
        "WEB-DRMADHU-001",
    ),

    (
        {"what initially drew you toward infertility", "drew you toward infertility", "focused area of practice", "assisted reproductive technology as a focused area"},
        "💖 **At present, I’m not sure about her personal motivation in her own words.**\n✨ Dr. Madhu Patil’s profile highlights 13+ years in obstetrics and gynecology, with 9+ years focused on infertility and ART.\n🩺 Her background includes advanced ART training from KEIL, Germany, and experience guiding more than 10,000 couples.\n📅 For a personal perspective on her journey, Dr. Madhu Patil’s team can help with an appointment or direct interaction.",
        "WEB-DRMADHU-001",
    ),
    (
        {"profile of infertility cases evolve", "urban india infertility", "age lifestyle underlying medical conditions", "infertility cases evolve"},
        "💖 **At present, I’m not sure about broad urban India trends from Dr. Madhu Patil’s Clinic.**\n✨ The clinic does highlight age as important, especially fertility decline after 35.\n🩺 Fertility assessment at the clinic reviews medical history, lifestyle history, ovarian reserve, uterus/tubes, and semen parameters.\n📅 For a doctor-led perspective on changing infertility patterns, Dr. Madhu Patil’s team can help arrange a consultation.",
        "WEB-DRMADHU-002",
    ),
    (
        {"balance expectations with realistic clinical outcomes", "counselling couples", "realistic clinical outcomes", "large number of ivf and icsi cycles"},
        "💖 **Counselling should balance hope with realistic expectations.**\n✨ Dr. Madhu Patil’s Clinic notes that IVF success depends on age, egg/sperm quality, underlying health conditions, and infertility reasons.\n🩺 The clinic also explains risks such as multiple pregnancy, OHSS, procedure risks, emotional stress, and financial considerations.\n📅 A consultation can help map these factors to the couple’s own reports and treatment history.",
        "WEB-DRMADHU-003",
    ),
    (
        {"poor ovarian reserve", "individualize stimulation protocols", "oocyte yield", "cycle cancellation"},
        "💖 **For poor ovarian reserve, Dr. Madhu Patil’s Clinic mentions mild stimulation protocols.**\n✨ Mild stimulation uses lower-dose medications and is described for women with low ovarian reserve.\n🩺 The IVF/ICSI service information also emphasizes treatment plans tailored to each patient’s needs.\n📅 Final protocol selection should be discussed after reviewing ovarian reserve, age, previous response, and reports.",
        "WEB-DRMADHU-003",
    ),
    (
        {"recurrent implantation failure", "uterine embryological immunological factors", "diagnostic framework", "rif"},
        "💖 **For recurrent implantation failure, the clinic describes a stepwise evaluation.**\n✨ Anatomical, genetic, and hormonal causes are ruled out first.\n🩺 Immune and clotting factors may be assessed when appropriate, especially when immunotherapy is being considered.\n📅 Dr. Madhu Patil’s Clinic can personalize the workup after reviewing previous IVF cycles and reports.",
        "WEB-DRMADHU-007",
    ),
    (
        {"transition point from conservative management", "iui to ivf", "pcos and endometriosis-related infertility", "transition from conservative management or iui"},
        "💖 **The exact transition point is personalized.**\n✨ Dr. Madhu Patil’s Clinic offers care for PCOS and endometriosis, and IVF/ICSI is listed for patients with these conditions.\n🩺 The IVF/ICSI service information also notes that multiple unsuccessful IUI attempts can be a reason to consider IVF-based treatment.\n📅 A consultation helps decide timing based on age, duration of infertility, reports, ovarian reserve, semen parameters, and prior treatment response.",
        "WEB-DRMADHU-003",
    ),
]

def find_faq_answer(question: str) -> tuple[str, str] | None:
    query_terms = terms(question)
    query_text = " ".join(sorted(query_terms))
    raw = question.lower()
    for patterns, answer, doc_id in FAQ_ANSWERS:
        for pattern in patterns:
            pattern_terms = terms(pattern)
            if pattern in raw or pattern_terms.issubset(query_terms) or pattern in query_text:
                return answer, doc_id
    return None
