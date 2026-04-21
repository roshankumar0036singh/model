import streamlit as st
import pickle
import pandas as pd

# --- Load the Model ---
# Ensure best_model.pkl is in the same directory or provide the full path
model_filename = 'best_model.pkl'
try:
    with open(model_filename, 'rb') as file:
        loaded_model = pickle.load(file)
    st.success(f"Model '{model_filename}' loaded successfully.")
except FileNotFoundError:
    st.error(f"Error: Model file '{model_filename}' not found. Please ensure it's in the correct directory.")
    st.stop() # Stop the app if model is not found

# --- Hardcoded Mappings for Categorical Features (based on training data encoding) ---
gender_options = {'Female': 0, 'Male': 1}
education_options = {"Bachelor's": 0, "Master's": 1, "PhD": 2}

# For 'Job Title', we'll assume direct numeric input for simplicity,
# as the full mapping is extensive and not saved.

# --- Streamlit App Layout ---
st.title('Salary Prediction App')
st.write('Enter the details below to predict salary:')

# Input fields
age = st.slider('Age', min_value=18, max_value=65, value=30)
gender_str = st.selectbox('Gender', list(gender_options.keys()))
education_str = st.selectbox('Education Level', list(education_options.keys()))
job_title_encoded = st.number_input('Job Title (Encoded Numeric Value, e.g., 159 for Software Engineer)', min_value=0, max_value=200, value=100) # Max value is an estimate
years_of_experience = st.slider('Years of Experience', min_value=0.0, max_value=40.0, value=5.0, step=0.5)

# Map selected strings to their encoded integer values
gender = gender_options[gender_str]
education_level = education_options[education_str]

# Create a DataFrame for prediction
input_data = pd.DataFrame([[age, gender, education_level, job_title_encoded, years_of_experience]],
                          columns=['Age', 'Gender', 'Education Level', 'Job Title', 'Years of Experience'])

if st.button('Predict Salary'):
    # Make prediction
    prediction = loaded_model.predict(input_data)
    st.success(f"### Predicted Salary: ${prediction[0]:,.2f}")
