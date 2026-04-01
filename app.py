import streamlit as st

st.set_page_config(page_title="GuideGrowth Predict", layout="centered")

INTERCEPT = 4.658909

COEFFICIENTS = {
    "male": 0.5701791 ,
    "skeletal_age": -0.1057164,
    "diagnosis": {
        "Skeletal dysplasia": 0.0,
        "Idiopathic": -3.394905 ,
        "Physeal causes": -3.628057 ,
        "Metabolic causes": -3.773683 ,
    },
    "bone_segment": {
        "Proximal tibia": 0.0,
        "Distal femur": 0.9431412 ,
    },
}


def predict_outcome(male: bool, skeletal_age: float, diagnosis: str, bone_segment: str) -> float:
    score = INTERCEPT
    score += COEFFICIENTS["male"] if male else 0.0
    score += COEFFICIENTS["skeletal_age"] * skeletal_age
    score += COEFFICIENTS["diagnosis"][diagnosis]
    score += COEFFICIENTS["bone_segment"][bone_segment]
    return score


st.title("GuideGrowth Predict")
st.caption("Prediction tool for correction rate after hemiepiphysiodesis by Department of Orthopaedic Surgery, Faculty of Medicine Siriraj Hospital, Mahidol university")

st.subheader("Enter predictor values")

col1, col2 = st.columns(2)

with col1:
    sex = st.selectbox("Sex", ["Female", "Male"])
    skeletal_age = st.number_input(
        "Skeletal age (years)",
        min_value=0.0,
        max_value=30.0,
        value=10.0,
        step=0.1,
    )

with col2:
    diagnosis = st.selectbox(
        "Diagnosis",
        list(COEFFICIENTS["diagnosis"].keys()),
    )
    bone_segment = st.selectbox(
        "Bone segment",
        list(COEFFICIENTS["bone_segment"].keys()),
    )

male = sex == "Male"
prediction = predict_outcome(
    male=male,
    skeletal_age=skeletal_age,
    diagnosis=diagnosis,
    bone_segment=bone_segment,
)

st.subheader("Predicted correction rate")
st.metric("Correction rate", f"{prediction:.2f} °/month")

st.info(
    "Categorical variables (e.g., diagnosis) are modeled by selecting a category, not as continuous values."
)


