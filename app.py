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

def predict(male, age, diagnosis, segment):
    y = INTERCEPT
    y += COEFFICIENTS["male"] if male else 0
    y += COEFFICIENTS["skeletal_age"] * age
    y += COEFFICIENTS["diagnosis"][diagnosis]
    y += COEFFICIENTS["bone_segment"][segment]
    return y

st.title("GuideGrowth Predict")
st.caption("Linear regression prediction tool")

sex = st.selectbox("Sex", ["Female", "Male"])
age = st.number_input("Skeletal age", 0.0, 30.0, 10.0)
diagnosis = st.selectbox("Diagnosis", list(COEFFICIENTS["diagnosis"].keys()))
segment = st.selectbox("Bone segment", list(COEFFICIENTS["bone_segment"].keys()))

pred = predict(sex == "Male", age, diagnosis, segment)

st.metric("Predicted value", f"{pred:.2f}")

df = pd.DataFrame({
    "Component": ["Intercept", "Sex", "Age", "Diagnosis", "Segment"],
    "Value": [
        INTERCEPT,
        COEFFICIENTS["male"] if sex == "Male" else 0,
        COEFFICIENTS["skeletal_age"] * age,
        COEFFICIENTS["diagnosis"][diagnosis],
        COEFFICIENTS["bone_segment"][segment]
    ]
})

st.dataframe(df, use_container_width=True)
