def generate_explanation(row):

    reasons = []

    if row["academic_score"] >= 90:
        reasons.append(
            "Excellent academic compatibility with the college cutoff."
        )

    elif row["academic_score"] >= 70:
        reasons.append(
            "Your academic profile is reasonably compatible with the cutoff."
        )

    if row["affordability_score"] >= 85:
        reasons.append(
            "The college fits comfortably within your budget."
        )

    elif row["affordability_score"] >= 60:
        reasons.append(
            "The college is within or close to your budget range."
        )

    if row["location_score"] >= 90:
        reasons.append(
            "The college matches your preferred location."
        )

    if row["preference_score"] >= 90:
        reasons.append(
            "The college offers your preferred branch."
        )

    elif row["preference_score"] >= 70:
        reasons.append(
            "The college offers a branch related to your preference."
        )

    if row["placement_score"] >= 85:
        reasons.append(
            "The college has strong placement indicators."
        )

    if row["career_score"] >= 90:
        reasons.append(
            "The branch aligns strongly with your career goal."
        )

    if row["content_similarity"] >= 50:
        reasons.append(
            "The college profile has strong similarity with your preferences."
        )

    if not reasons:
        reasons.append(
            "This college matches multiple parameters of your student profile."
        )

    return reasons