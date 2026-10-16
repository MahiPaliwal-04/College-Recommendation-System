import streamlit as st
import pandas as pd

from modules.recommender import (
    recommend_colleges
)

from modules.ml_model import (
    add_ml_score
)

from modules.explanations import (
    generate_explanation
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI College Recommendation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .score-box {
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #ddd;
    }

    .college-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "colleges.csv"
    )


try:

    df = load_data()

except Exception as error:

    st.error(
        f"Dataset loading error: {error}"
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎓 AI-Powered College Recommendation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Find colleges based on your academic profile, budget,
    branch, location, career goal and placement preferences.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "👨‍🎓 Student Profile"
)

st.sidebar.caption(
    "Enter your preferences to generate personalized recommendations."
)


academic_score = st.sidebar.slider(
    "📚 Academic Score / Percentage",
    min_value=0,
    max_value=100,
    value=80
)


budget = st.sidebar.number_input(
    "💰 Maximum Annual Budget (₹)",
    min_value=20000,
    max_value=1000000,
    value=100000,
    step=10000
)


branch_options = sorted(
    df["branch"].dropna().unique()
)


branch = st.sidebar.selectbox(
    "🎓 Preferred Branch",
    branch_options
)


location_options = sorted(
    df["location"].dropna().unique()
)


location = st.sidebar.selectbox(
    "📍 Preferred Location",
    ["Any"] + location_options
)


career_goal = st.sidebar.selectbox(
    "🚀 Career Goal",
    [
        "Software Development",
        "Artificial Intelligence",
        "Data Science",
        "Core Engineering",
        "Higher Studies"
    ]
)


top_k = st.sidebar.slider(
    "🏆 Number of Recommendations",
    min_value=3,
    max_value=10,
    value=5
)


# ============================================================
# STUDENT PROFILE
# ============================================================

student = {

    "academic_score":
        academic_score,

    "budget":
        budget,

    "branch":
        branch,

    "location":
        location,

    "career_goal":
        career_goal
}


# ============================================================
# PROFILE SUMMARY
# ============================================================

st.subheader(
    "👤 Your Profile"
)

profile_col1, profile_col2, profile_col3, profile_col4 = (
    st.columns(4)
)


with profile_col1:

    st.metric(
        "Academic Score",
        f"{academic_score}%"
    )


with profile_col2:

    st.metric(
        "Budget",
        f"₹{budget:,}"
    )


with profile_col3:

    st.metric(
        "Branch",
        branch
    )


with profile_col4:

    st.metric(
        "Career Goal",
        career_goal
    )


st.divider()


# ============================================================
# RECOMMENDATION BUTTON
# ============================================================

recommend_button = st.button(
    "🔍 Generate My College Recommendations",
    type="primary",
    use_container_width=True
)


if recommend_button:

    with st.spinner(
        "Analyzing colleges using hybrid recommendation model..."
    ):

        # --------------------------------------------
        # STEP 1: HARD FILTER + WEIGHTED RECOMMENDER
        # --------------------------------------------

        recommendations = recommend_colleges(
            df,
            student
        )

        # --------------------------------------------
        # STEP 2: ML CONTENT-BASED MODEL
        # --------------------------------------------

        recommendations = add_ml_score(
            recommendations,
            df,
            student
        )


    # ========================================================
    # NO RESULT
    # ========================================================

    if recommendations.empty:

        st.error(
            """
            No suitable colleges were found for the
            current combination of academic score and budget.

            Try increasing your budget or modifying
            your preferences.
            """
        )

        st.stop()


    # ========================================================
    # TOP-K
    # ========================================================

    recommendations = recommendations.head(
        top_k
    ).copy()

    recommendations["rank"] = (
        range(
            1,
            len(recommendations) + 1
        )
    )


    # ========================================================
    # SUCCESS MESSAGE
    # ========================================================

    st.success(
        f"🎯 {len(recommendations)} personalized colleges found!"
    )


    # ========================================================
    # MODEL EXPLANATION
    # ========================================================

    with st.expander(
        "🤖 How does this recommendation system work?"
    ):

        st.markdown(
            """
            ### Hybrid Recommendation Pipeline

            **1. Eligibility Filtering**
            - Academic compatibility
            - Budget compatibility

            **2. Multi-Criteria Scoring**
            - Academic Fit → 25%
            - Affordability → 20%
            - Location → 10%
            - Placement → 20%
            - Branch Preference → 15%
            - Career Goal → 10%

            **3. Machine Learning**
            - TF-IDF feature extraction
            - Cosine similarity
            - Content-based recommendation

            **4. Final Ranking**

            The system combines the weighted recommendation
            score with ML content similarity to generate
            personalized Top-K recommendations.
            """
        )


    # ========================================================
    # TOP COLLEGE
    # ========================================================

    top_college = recommendations.iloc[0]


    st.subheader(
        "🏆 Top Recommendation"
    )


    top_col1, top_col2 = st.columns(
        [2, 1]
    )


    with top_col1:

        st.markdown(
            f"""
            ## 🥇 {top_college['college']}

            **📍 Location:** {top_college['location']}

            **🎓 Branch:** {top_college['branch']}

            **💰 Fees:** ₹{top_college['fees']:,}

            **📊 Cutoff:** {top_college['cutoff']}

            **💼 Average Package:** ₹{top_college['avg_package']:,}

            **📈 Placement Rate:** {top_college['placement_rate']}%

            **⭐ College Rating:** {top_college['rating']}/5
            """
        )


    with top_col2:

        st.metric(
            "Final Recommendation Score",
            f"{top_college['final_ml_score']:.1f}/100"
        )

        st.metric(
            "ML Similarity",
            f"{top_college['content_similarity']:.1f}%"
        )


    st.info(
        top_college["description"]
    )


    # ========================================================
    # WHY TOP COLLEGE?
    # ========================================================

    st.markdown(
        "### 💡 Why is this college recommended?"
    )


    top_reasons = generate_explanation(
        top_college
    )


    for reason in top_reasons:

        st.write(
            f"✅ {reason}"
        )


    st.divider()


    # ========================================================
    # ALL RECOMMENDATIONS
    # ========================================================

    st.subheader(
        "🎓 Personalized College Recommendations"
    )


    for _, row in recommendations.iterrows():

        with st.container():

            st.markdown(
                f"""
                ## #{int(row['rank'])} {row['college']}

                **📍 {row['location']}**

                **🎓 {row['branch']}**

                **💰 Fees:** ₹{row['fees']:,}

                **📊 Cutoff:** {row['cutoff']}

                **💼 Average Package:** ₹{row['avg_package']:,}

                **📈 Placement:** {row['placement_rate']}%

                **⭐ Final Score:** {row['final_ml_score']:.2f}/100
                """
            )


            st.progress(
                min(
                    int(row["final_ml_score"]),
                    100
                )
            )


            with st.expander(
                "🔎 View recommendation details"
            ):

                score_col1, score_col2, score_col3 = (
                    st.columns(3)
                )


                with score_col1:

                    st.metric(
                        "Academic Fit",
                        f"{row['academic_score']:.1f}"
                    )

                    st.metric(
                        "Placement",
                        f"{row['placement_score']:.1f}"
                    )


                with score_col2:

                    st.metric(
                        "Affordability",
                        f"{row['affordability_score']:.1f}"
                    )

                    st.metric(
                        "Branch Match",
                        f"{row['preference_score']:.1f}"
                    )


                with score_col3:

                    st.metric(
                        "Career Match",
                        f"{row['career_score']:.1f}"
                    )

                    st.metric(
                        "ML Similarity",
                        f"{row['content_similarity']:.1f}"
                    )


                st.markdown(
                    "### 💡 Why recommended?"
                )


                reasons = generate_explanation(
                    row
                )


                for reason in reasons:

                    st.write(
                        f"✅ {reason}"
                    )


                st.info(
                    row["description"]
                )


            st.divider()


    # ========================================================
    # COMPARISON TABLE
    # ========================================================

    st.subheader(
        "📊 College Comparison"
    )


    comparison = recommendations[
        [
            "rank",
            "college",
            "location",
            "branch",
            "fees",
            "cutoff",
            "avg_package",
            "placement_rate",
            "content_similarity",
            "final_ml_score"
        ]
    ].copy()


    comparison.columns = [

        "Rank",
        "College",
        "Location",
        "Branch",
        "Fees",
        "Cutoff",
        "Avg Package",
        "Placement %",
        "ML Similarity %",
        "Final Score"
    ]


    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # DOWNLOAD RESULTS
    # ========================================================

    csv_data = recommendations.to_csv(
        index=False
    ).encode(
        "utf-8"
    )


    st.download_button(
        label="⬇️ Download Recommendations as CSV",
        data=csv_data,
        file_name="college_recommendations.csv",
        mime="text/csv",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#777;">
    🎓 College / University Recommendation System |
    AI & Machine Learning Project
    </div>
    """,
    unsafe_allow_html=True
)