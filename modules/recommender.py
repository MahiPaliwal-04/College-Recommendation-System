import pandas as pd


def academic_fit(student_score, cutoff):
    """
    Calculates academic compatibility between
    student's score and college cutoff.
    """

    difference = student_score - cutoff

    if difference >= 10:
        return 100

    elif difference >= 5:
        return 95

    elif difference >= 0:
        return 90

    elif difference >= -5:
        return 70

    elif difference >= -10:
        return 40

    else:
        return 0


def affordability_score(budget, fees):
    """
    Calculates how comfortably the college
    fits inside student's budget.
    """

    if fees <= budget * 0.60:
        return 100

    elif fees <= budget * 0.80:
        return 95

    elif fees <= budget:
        return 85

    elif fees <= budget * 1.10:
        return 60

    elif fees <= budget * 1.20:
        return 30

    return 0


def location_score(preferred_location, college_location):
    """
    Calculates location preference score.
    """

    if not preferred_location or preferred_location == "Any":
        return 70

    if preferred_location.lower() == college_location.lower():
        return 100

    return 40


def branch_score(preferred_branch, college_branch):
    """
    Calculates branch preference score.
    """

    preferred = preferred_branch.lower()
    college = college_branch.lower()

    if preferred == college:
        return 100

    similar_branches = {
        "cse": ["ai ml", "it"],
        "it": ["cse", "ai ml"],
        "ai ml": ["cse", "it"]
    }

    if college in similar_branches.get(preferred, []):
        return 70

    return 30


def placement_score(avg_package, placement_rate):
    """
    Combines average package and placement rate.
    """

    package_score = min(
        (avg_package / 1000000) * 100,
        100
    )

    placement_rate_score = min(
        placement_rate,
        100
    )

    return (
        package_score * 0.50
        + placement_rate_score * 0.50
    )


def career_score(career_goal, branch):
    """
    Matches career goal with branch.
    """

    goal = career_goal.lower()
    branch = branch.lower()

    if goal == "software development":

        if branch == "cse":
            return 100

        if branch == "it":
            return 95

        if branch == "ai ml":
            return 85

    elif goal == "artificial intelligence":

        if branch == "ai ml":
            return 100

        if branch == "cse":
            return 90

        if branch == "it":
            return 80

    elif goal == "data science":

        if branch == "ai ml":
            return 100

        if branch == "cse":
            return 90

        if branch == "it":
            return 85

    elif goal == "higher studies":

        return 80

    elif goal == "core engineering":

        return 70

    return 60


def calculate_final_score(
    academic,
    affordability,
    location,
    placement,
    preference,
    career
):
    """
    Hybrid weighted recommendation score.

    Academic       = 25%
    Affordability  = 20%
    Location       = 10%
    Placement      = 20%
    Preference     = 15%
    Career         = 10%
    """

    score = (
        academic * 0.25
        + affordability * 0.20
        + location * 0.10
        + placement * 0.20
        + preference * 0.15
        + career * 0.10
    )

    return round(score, 2)


def recommend_colleges(df, student):
    """
    Main recommendation function.
    """

    recommendations = []

    for _, college in df.iterrows():

        academic = academic_fit(
            student["academic_score"],
            college["cutoff"]
        )

        affordability = affordability_score(
            student["budget"],
            college["fees"]
        )

        location = location_score(
            student["location"],
            college["location"]
        )

        preference = branch_score(
            student["branch"],
            college["branch"]
        )

        placement = placement_score(
            college["avg_package"],
            college["placement_rate"]
        )

        career = career_score(
            student["career_goal"],
            college["branch"]
        )

        # --------------------------------
        # HARD ELIGIBILITY FILTER
        # --------------------------------

        if academic == 0:
            continue

        # Allow a small budget flexibility
        if college["fees"] > student["budget"] * 1.20:
            continue

        final_score = calculate_final_score(
            academic,
            affordability,
            location,
            placement,
            preference,
            career
        )

        recommendations.append({

            "college": college["college"],

            "location": college["location"],

            "state": college["state"],

            "branch": college["branch"],

            "fees": college["fees"],

            "cutoff": college["cutoff"],

            "avg_package": college["avg_package"],

            "placement_rate": college["placement_rate"],

            "college_type": college["college_type"],

            "rating": college["rating"],

            "description": college["description"],

            "academic_score": round(academic, 2),

            "affordability_score": round(
                affordability,
                2
            ),

            "location_score": round(
                location,
                2
            ),

            "placement_score": round(
                placement,
                2
            ),

            "preference_score": round(
                preference,
                2
            ),

            "career_score": round(
                career,
                2
            ),

            "final_score": final_score
        })

    result = pd.DataFrame(
        recommendations
    )

    if result.empty:
        return result

    result = result.sort_values(
        by="final_score",
        ascending=False
    ).reset_index(drop=True)

    result["rank"] = (
        result.index + 1
    )

    return result