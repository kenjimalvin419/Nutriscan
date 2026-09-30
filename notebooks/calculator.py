def classify_nutrition_status(
    age_months: float,
    weight_kg: float,
    height_cm: float,
    gender: str | None = None,
    muac_cm: float | None = None
):
    # 1. Validasi dasar
    if age_months <= 0 or weight_kg <= 0 or height_cm <= 0:
        return (
            "Invalid Input",
            "Age (months), weight (kg), and height (cm) must all be positive.",
            "Please correct the input values."
        )

    gender_norm = (gender or "").strip().lower()
    if gender_norm in ["laki-laki", "laki", "male", "m"]:
        gender_norm = "male"
    elif gender_norm in ["perempuan", "wanita", "female", "f"]:
        gender_norm = "female"
    elif gender_norm:
        gender_norm = "other"
    else:
        gender_norm = "unspecified"

    # Hitung BMI (pakai sebagai pendukung, bukan satu-satunya penentu)
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m ** 2)

    # Klasifikasi BMI sederhana (prototype)
    if bmi < 12:
        bmi_cat = "Severe Underweight"
        bmi_adjust = -20
    elif 12 <= bmi < 14:
        bmi_cat = "Underweight"
        bmi_adjust = -15
    elif 14 <= bmi < 15.5:
        bmi_cat = "At-Risk"
        bmi_adjust = -10
    elif 15.5 <= bmi <= 18.5:
        bmi_cat = "Normal"
        bmi_adjust = +10
    else:
        bmi_cat = "Overweight"
        bmi_adjust = +15

    # 2. Jika MUAC diisi → MUAC + BMI digabung jadi skor
    if muac_cm is not None and muac_cm > 0:
        if muac_cm < 11.5:
            muac_cat = "SAM"
            muac_score = 15
        elif 11.5 <= muac_cm < 12.5:
            muac_cat = "MAM"
            muac_score = 35
        elif 12.5 <= muac_cm <= 13.5:
            muac_cat = "At-Risk"
            muac_score = 60
        else:
            muac_cat = "Healthy"
            muac_score = 80

        # Gabungkan jadi skor risiko 0–100
        raw_score = muac_score + bmi_adjust
        risk_score = max(0, min(100, raw_score))

        # Terjemahkan skor → status akhir
        if risk_score >= 75:
            status = "Healthy"
        elif risk_score >= 55:
            status = "At-Risk of Undernutrition"
        elif risk_score >= 30:
            status = "MAM (Moderate Acute Malnutrition)"
        else:
            status = "SAM (Severe Acute Malnutrition)"

        explanation = (
            f"Gender = {gender_norm}.\n"
            f"Age = {age_months:.0f} months.\n"
            f"MUAC = {muac_cm:.1f} cm → MUAC category: {muac_cat}.\n"
            f"BMI ≈ {bmi:.1f} → BMI category: {bmi_cat}.\n"
            f"Combined risk score = {risk_score:.0f} (0 = highest risk, 100 = lowest risk).\n"
            "MUAC is the primary indicator; BMI is used here as supporting information."
        )

        # Saran berdasarkan status akhir
        if "SAM" in status:
            advice = (
                "This result suggests a high risk of severe acute malnutrition (SAM). "
                "Immediate referral to the nearest health facility is recommended. "
                "This prototype cannot replace medical assessment."
            )
        elif "MAM" in status:
            advice = (
                "This result suggests moderate acute malnutrition (MAM). "
                "Home-based nutritional support, caregiver counseling, and close follow-up "
                "at a health facility are recommended."
            )
        elif "At-Risk" in status:
            advice = (
                "There are signs of undernutrition risk. Improve diet diversity, increase "
                "feeding frequency, and re-check the child's growth within 2–4 weeks."
            )
        else:  # Healthy
            advice = (
                "Current indicators are within a healthy range. Maintain a balanced diet and "
                "continue regular growth monitoring. If you have concerns, consult a health professional."
            )

        return status, explanation, advice

    # 3. Kalau MUAC tidak diisi → pakai BMI saja (fallback sederhana)
    if bmi < 12:
        status = "Severe Underweight (BMI-based Prototype)"
        explanation = (
            f"Gender = {gender_norm}.\n"
            f"Age = {age_months:.0f} months.\n"
            f"BMI ≈ {bmi:.1f}, which is extremely low for a child.\n"
            "This suggests a high risk of severe undernutrition based on BMI only."
        )
        advice = (
            "Seek immediate evaluation at a health facility. "
            "This tool is not a medical device and must not replace clinical judgment."
        )
    elif 12 <= bmi < 14:
        status = "Underweight (BMI-based Prototype)"
        explanation = (
            f"Gender = {gender_norm}.\n"
            f"Age = {age_months:.0f} months.\n"
            f"BMI ≈ {bmi:.1f}, below a healthy range.\n"
            "This suggests moderate undernutrition risk based on BMI only."
        )
        advice = (
            "Nutritional improvement and monitoring are recommended. "
            "Please consult a health worker for proper assessment."
        )
    elif 14 <= bmi < 15.5:
        status = "At-Risk (BMI-based Prototype)"
        explanation = (
            f"Gender = {gender_norm}.\n"
            f"Age = {age_months:.0f} months.\n"
            f"BMI ≈ {bmi:.1f}, slightly below typical healthy range.\n"
            "This indicates a risk of undernutrition."
        )
        advice = (
            "Improve dietary quality and monitor weight and height regularly. "
            "If growth remains slow, consult a health professional."
        )
    elif 15.5 <= bmi <= 18.5:
        status = "Healthy Range (BMI-based Prototype)"
        explanation = (
            f"Gender = {gender_norm}.\n"
            f"Age = {age_months:.0f} months.\n"
            f"BMI ≈ {bmi:.1f}, within a normal range based on simplified thresholds."
        )
        advice = (
            "Maintain current feeding practices and continue routine growth monitoring."
        )
    else:
        status = "Possible Overweight (BMI-based Prototype)"
        explanation = (
            f"Gender = {gender_norm}.\n"
            f"Age = {age_months:.0f} months.\n"
            f"BMI ≈ {bmi:.1f}, above the simplified healthy range.\n"
            "This prototype focuses on undernutrition, but this suggests possible overweight."
        )
        advice = (
            "Discuss the child's growth pattern with a health worker to ensure a healthy "
            "balance of nutrition and activity."
        )

    return status, explanation, advice
