import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load resources
try:
    model = joblib.load(r"C:\Users\Tejas\OneDrive\Desktop\ckd-prediction-project\model\ckd_model_v3.pkl")
    features = joblib.load(r"C:\Users\Tejas\OneDrive\Desktop\ckd-prediction-project\model\ckd_features_v3.pkl")
    label_encoders = joblib.load(r"C:\Users\Tejas\OneDrive\Desktop\ckd-prediction-project\model\ckd_label_encoders_v3.pkl")
except Exception as e:
    st.error(f"Error loading resources: {e}")
    st.stop()

# Feature name mapping
FEATURE_NAMES = {
    'age': 'Age (years)*',
    'bp_(diastolic)': 'Diastolic BP (mmHg)*',
    'bp_limit': 'BP Category*',
    'sg': 'Specific Gravity*',
    'al': 'Albumin Level (0-5)*',
    'rbc': 'Red Blood Cells*',
    'su': 'Sugar Level*',
    'pc': 'Pus Cells*',
    'pcc': 'Pus Cell Clumps*',
    'ba': 'Bacteria*',
    'bgr': 'Blood Glucose (mg/dL)*',
    'bu': 'Blood Urea (mg/dL)*',
    'sod': 'Sodium (mEq/L)*',
    'sc': 'Serum Creatinine (mg/dL)*',
    'pot': 'Potassium (mEq/L)*',
    'hemo': 'Hemoglobin (g/dL)*',
    'pcv': 'Packed Cell Volume (%)*',
    'rbcc': 'RBC Count (millions/mm3)*',
    'wbcc': 'WBC Count (cells/mm3)*',
    'htn': 'Hypertension*',
    'dm': 'Diabetes*',
    'cad': 'Coronary Artery Disease*',
    'appet': 'Appetite*',
    'pe': 'Pedal Edema*',
    'ane': 'Anemia*',
    'grf': 'GFR (mL/min/1.73m²)*',
    'stage': 'Kidney Disease Stage*'
}

# Configuration for inputs
input_config = {
    'age': {'type': 'number', 'min': 0, 'max': 100, 'value': 35},
    'bp_(diastolic)': {'type': 'number', 'min': 50, 'max': 180, 'value': 80},
    'sg': {'type': 'number', 'min': 1.000, 'max': 1.025, 'value': 1.015, 'step': 0.001},
    'al': {'type': 'number', 'min': 0, 'max': 5, 'value': 0, 'step': 1},
    'su': {'type': 'number', 'min': 0, 'max': 5, 'value': 0, 'step': 1},
    'bgr': {'type': 'number', 'min': 70, 'max': 500, 'value': 100},
    'bu': {'type': 'number', 'min': 1, 'max': 200, 'value': 30},
    'sc': {'type': 'number', 'min': 0.1, 'max': 15.0, 'value': 0.9, 'step': 0.1},
    'sod': {'type': 'number', 'min': 100, 'max': 160, 'value': 140},
    'pot': {'type': 'number', 'min': 2.5, 'max': 7.0, 'value': 4.0, 'step': 0.1},
    'hemo': {'type': 'number', 'min': 3.0, 'max': 18.0, 'value': 14.0, 'step': 0.1},
    'pcv': {'type': 'number', 'min': 10, 'max': 55, 'value': 42},
    'wbcc': {'type': 'number', 'min': 2000, 'max': 20000, 'value': 7000, 'step': 100},
    'rbcc': {'type': 'number', 'min': 2.0, 'max': 7.0, 'value': 5.0, 'step': 0.1},
    'grf': {'type': 'number', 'min': 15, 'max': 200, 'value': 90},
    'bp_limit': {'type': 'categorical', 'options': ['Low', 'Normal', 'High']},
    'rbc': {'type': 'categorical', 'options': ['Normal', 'Abnormal']},
    'pc': {'type': 'categorical', 'options': ['Absent', 'Present']},
    'pcc': {'type': 'categorical', 'options': ['Absent', 'Present']},
    'ba': {'type': 'categorical', 'options': ['Absent', 'Present']},
    'htn': {'type': 'categorical', 'options': ['No', 'Yes']},
    'dm': {'type': 'categorical', 'options': ['No', 'Yes']},
    'cad': {'type': 'categorical', 'options': ['No', 'Yes']},
    'appet': {'type': 'categorical', 'options': ['Good', 'Poor']},
    'pe': {'type': 'categorical', 'options': ['No', 'Yes']},
    'ane': {'type': 'categorical', 'options': ['No', 'Yes']},
    'stage': {'type': 'categorical', 'options': ['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4', 'Stage 5']}
}

# App UI
st.set_page_config(page_title="CKD Predictor", layout="centered")
st.title("🩺 Chronic Kidney Disease Predictor")
st.markdown("### Enter Patient Data Below:")

input_data = {}
cols = st.columns(2)

for i, col in enumerate(features):
    config = input_config.get(col, {'type': 'number'})
    label = FEATURE_NAMES.get(col, col.replace('_', ' ').title())
    current_col = cols[i % 2]
    
    with current_col:
        if config.get('type') == 'categorical':
            # Get meaningful options from config
            options = config.get('options', [])
            # Add "Select..." as first option
            display_options = ["Select..."] + options
            input_data[col] = st.selectbox(
                label, 
                display_options,
                key=f"{col}_select"
            )
        else:
            # Handle numerical inputs
            min_val = config.get('min', 0)
            max_val = config.get('max', 100)
            value = config.get('value', (min_val + max_val) / 2)
            step = config.get('step', 1)
            
            input_data[col] = st.number_input(
                label, 
                min_value=min_val,
                max_value=max_val,
                value=value,
                step=step,
                key=f"{col}_number"
            )

# Prediction
st.divider()
if st.button("Predict CKD Status", use_container_width=True, type="primary"):
    try:
        # Check for missing inputs
        missing = []
        for col in features:
            if col in input_config and input_config[col].get('type') == 'categorical':
                if input_data[col] == "Select...":
                    missing.append(FEATURE_NAMES.get(col, col))
        
        if missing:
            st.error(f"❌ Please complete these fields: {', '.join(missing)}")
            st.stop()
            
        # Prepare input data
        input_df = pd.DataFrame([input_data])
        
        # Create reverse mapping for categorical features
        categorical_mapping = {
            'rbc': {'Normal': 0, 'Abnormal': 1},
            'pc': {'Absent': 0, 'Present': 1},
            'pcc': {'Absent': 0, 'Present': 1},
            'ba': {'Absent': 0, 'Present': 1},
            'htn': {'No': 0, 'Yes': 1},
            'dm': {'No': 0, 'Yes': 1},
            'cad': {'No': 0, 'Yes': 1},
            'appet': {'Good': 0, 'Poor': 1},
            'pe': {'No': 0, 'Yes': 1},
            'ane': {'No': 0, 'Yes': 1},
            'bp_limit': {'Low': 0, 'Normal': 1, 'High': 2},
            'stage': {
                'Stage 1': 0, 
                'Stage 2': 1, 
                'Stage 3': 2, 
                'Stage 4': 3, 
                'Stage 5': 4
            }
        }
        
        # Convert categorical selections to encoded values
        for col in categorical_mapping:
            if col in input_df.columns:
                selection = input_data[col]
                input_df[col] = categorical_mapping[col][selection]
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        
        # Display results
        if prediction == 1:
            st.error("## 🚨 High Risk of Chronic Kidney Disease")
            st.metric("Risk Probability", f"{probability:.1%}")
            st.warning("""
            **Recommendations:**
            - Consult a nephrologist immediately
            - Get comprehensive blood and urine tests
            - Monitor blood pressure daily
            - Reduce salt and protein intake
            """)
        else:
            st.success("## ✅ Low Risk of Chronic Kidney Disease")
            st.metric("Risk Probability", f"{probability:.1%}")
            st.info("""
            **Recommendations:**
            - Maintain annual kidney function tests
            - Stay hydrated (8 glasses of water/day)
            - Control blood sugar and blood pressure
            - Avoid NSAIDs and nephrotoxic medications
            """)
                
    except Exception as e:
        st.error(f"⚠️ Prediction error: {str(e)}")

# Footer
st.divider()
st.caption("""
**Medical Disclaimer:** 
This tool provides preliminary risk assessment only. It is not a substitute for professional medical advice. 
Always consult with a qualified healthcare provider for diagnosis and treatment.
""")