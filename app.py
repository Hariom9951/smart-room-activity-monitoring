import streamlit as st
import numpy as np
import pickle
import pandas as pd

# LOAD MODELS
with open("models/all_models.pkl", "rb") as f:
    models, le, model_scores, room_model, le_room, temp_model, hum_model, light_model = pickle.load(f)

st.title("🏠 Smart Activity Prediction (Auto Environment)")

# INPUT
time_input = st.text_input("Enter Time (HH:MM)", "22:30")
model_choice = st.selectbox("Select Model", list(models.keys()))

# FEATURE FUNCTION
def get_features(time_str):
    h, m = map(int, time_str.split(":"))
    t = h + m/60
    
    sin_t = np.sin(2*np.pi*t/24)
    cos_t = np.cos(2*np.pi*t/24)
    
    # AUTO ENV PREDICTION
    temp = temp_model.predict([[sin_t, cos_t]])[0]
    hum = hum_model.predict([[sin_t, cos_t]])[0]
    light = light_model.predict([[sin_t, cos_t]])[0]
    
    return [[sin_t, cos_t, temp, hum, light]], temp, hum, light

# PREDICTION
if st.button("Predict"):
    try:
        X_input, temp, hum, light = get_features(time_input)
        
        model = models[model_choice]
        pred = model.predict(X_input)
        location = le.inverse_transform(pred)[0]
        
        st.success(f"📍 Location: {location}")
        
        # SHOW AUTO ENV
        st.subheader("🌍 Predicted Environment")
        st.write(f"🌡 Temperature: {round(temp,2)} °C")
        st.write(f"💧 Humidity: {round(hum,2)} %")
        st.write(f"💡 Light: {round(light,2)}")
        
        # ROOM TYPE
        if location == "Room":
            room_pred = room_model.predict(X_input)
            room_type = le_room.inverse_transform(room_pred)[0]
            st.info(f"🛏 Room Type: {room_type}")
        
        # PROBABILITY
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_input)[0]
            prob_df = pd.DataFrame({
                "Class": le.classes_,
                "Probability": probs
            })
            st.bar_chart(prob_df.set_index("Class"))
    
    except:
        st.error("Invalid input format!")

# MODEL COMPARISON
st.subheader("📊 Model Accuracy Comparison")

score_df = pd.DataFrame({
    "Model": list(model_scores.keys()),
    "Accuracy": list(model_scores.values())
})

st.bar_chart(score_df.set_index("Model"))




# streamlit run c:\Users\HP\Desktop\project\app.py 