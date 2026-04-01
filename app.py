import streamlit as st
import pandas as pd

st.set_page_config(page_title="GuideGrowth Predict", layout="centered")

INTERCEPT = 4.658909

COEFFICIENTS = {
    "male": 0.57,
    "skeletal_age": -0.11,
    "diagnosis": {
        "Skeletal dysplasia": 0.0,
        "Idiopathic": -3.39,
        "Physeal causes": -3.63,
        "Metabolic causes": -3.77,
    },
    "bone_segment": {
        "Proximal tibia": 0.0,
        "Distal femur": 0.94,
    },
}

def predict(male: bool, age: float, diagnosis: str, segment: str) -> float:
    y = INTERCEPT
    y += COEFFICIENTS["male"] if male else 0.0
    y += COEFFICIENTS["skeletal_age"] * age
    y += COEFFICIENTS["diagnosis"][diagnosis]
    y += COEFFICIENTS["bone_segment"][segment]
    return y

st.markdown(
    """
    <style>
    .main > div {
        max-width: 850px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .gg-card {
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 1rem 1.1rem;
        background: #ffffff;
        margin-bottom: 1rem;
    }
    div[data-testid="stMetric"] {
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 0.8rem 1rem;
        background: #fafafa;
    }
    .gg-small {
        color: #4b5563;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("GuideGrowth Predict")
st.caption("Prediction tool for correction rate based on the final multivariable linear regression model")

st.markdown('<div class="gg-card">', unsafe_allow_html=True)
st.markdown("### Patient inputs")

col1, col2 = st.columns(2)

with col1:
    sex = st.selectbox(
        "Sex",
        ["Female", "Male"],
        help="Biologic sex used in the model.",
    )
    age = st.number_input(
        "Skeletal age (years)",
        min_value=0.0,
        max_value=30.0,
        value=10.0,
        step=0.1,
        help="Enter skeletal age in years.",
    )

with col2:
    diagnosis = st.selectbox(
        "Diagnosis category",
        list(COEFFICIENTS["diagnosis"].keys()),
        help="Categorical diagnosis is handled with indicator variables, not as a continuous number.",
    )
    segment = st.selectbox(
        "Bone segment",
        list(COEFFICIENTS["bone_segment"].keys()),
        help="Anatomic segment used in the model.",
    )

st.markdown("</div>", unsafe_allow_html=True)

pred = predict(sex == "Male", age, diagnosis, segment)

st.markdown('<div class="gg-card">', unsafe_allow_html=True)
st.markdown("### Predicted outcome")
st.metric("Correction rate", f"{pred:.2f}°")
st.markdown('<div class="gg-small">Outcome unit = degrees</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="gg-card">', unsafe_allow_html=True)
st.markdown("### Model equation")
st.latex(
    r"\hat{Y} = 4.6589 + 0.57(Male) - 0.11(Skeletal\ Age) - 3.39(Idiopathic) - 3.63(Physeal) - 3.77(Metabolic) + 0.94(Distal\ Femur)"
)
st.markdown(
    """
- **Outcome** = correction rate (degrees)  
- **Skeletal age** = years  
- **Reference diagnosis** = Skeletal dysplasia  
- **Reference bone segment** = Proximal tibia  
"""
)
st.markdown("</div>", unsafe_allow_html=True)

contrib_df = pd.DataFrame(
    {
        "Component": [
            "Intercept",
            "Male sex",
            "Skeletal age (years)",
            f"Diagnosis: {diagnosis}",
            f"Bone segment: {segment}",
        ],
        "Contribution to prediction (degrees)": [
            INTERCEPT,
            COEFFICIENTS["male"] if sex == "Male" else 0.0,
            COEFFICIENTS["skeletal_age"] * age,
            COEFFICIENTS["diagnosis"][diagnosis],
            COEFFICIENTS["bone_segment"][segment],
        ],
    }
)

st.markdown('<div class="gg-card">', unsafe_allow_html=True)
st.markdown("### Contribution of each model term")
st.dataframe(contrib_df, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

st.info(
    "Categorical predictors are modeled by selecting a category and applying its coefficient relative to the reference group."
)
