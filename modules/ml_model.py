import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def prepare_college_text(df):

    df = df.copy()

    df["combined_features"] = (
        df["branch"].fillna("").astype(str)
        + " "
        + df["location"].fillna("").astype(str)
        + " "
        + df["state"].fillna("").astype(str)
        + " "
        + df["college_type"].fillna("").astype(str)
        + " "
        + df["description"].fillna("").astype(str)
    )

    return df


def content_based_similarity(df, student):

    df = prepare_college_text(df)

    student_text = (
        str(student["branch"])
        + " "
        + str(student["location"])
        + " "
        + str(student["career_goal"])
    )

    documents = (
        df["combined_features"].tolist()
        + [student_text]
    )

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(
        documents
    )

    college_vectors = matrix[:-1]

    student_vector = matrix[-1]

    similarities = cosine_similarity(
        student_vector,
        college_vectors
    ).flatten()

    df["content_similarity"] = (
        similarities * 100
    ).round(2)

    return df


def add_ml_score(
    recommendation_df,
    original_df,
    student
):

    if recommendation_df.empty:
        return recommendation_df

    ml_df = content_based_similarity(
        original_df,
        student
    )

    similarity_map = dict(
        zip(
            ml_df["college"],
            ml_df["content_similarity"]
        )
    )

    recommendation_df = (
        recommendation_df.copy()
    )

    recommendation_df["content_similarity"] = (
        recommendation_df["college"]
        .map(similarity_map)
        .fillna(0)
    )

    # 85% hybrid business score
    # 15% ML content similarity

    recommendation_df["final_ml_score"] = (
        recommendation_df["final_score"] * 0.85
        + recommendation_df["content_similarity"] * 0.15
    ).round(2)

    recommendation_df = recommendation_df.sort_values(
        by="final_ml_score",
        ascending=False
    ).reset_index(drop=True)

    recommendation_df["rank"] = (
        recommendation_df.index + 1
    )

    return recommendation_df