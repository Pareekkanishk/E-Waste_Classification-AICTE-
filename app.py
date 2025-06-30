import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json


with open("info.json", "r") as f:
    treatment_info = json.load(f)

class_names = list(treatment_info.keys())


@st.cache_resource
def load_model():
    model = tf.keras.models.load_model(r"week 2\Best_model.keras")  
    return model

model = load_model()


if 'predicted_class' not in st.session_state:
    st.session_state['predicted_class'] = None
if 'uploaded_image' not in st.session_state:
    st.session_state['uploaded_image'] = None


page = st.sidebar.selectbox("📂 Choose Page", ["Upload & Predict", "Treatment Info"])


if page == "Upload & Predict":
    st.title("📤 E-Waste Classifier")

    uploaded_file = st.file_uploader("Upload an image of an e-waste item", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, caption="Uploaded Image", width=300)
        st.session_state['uploaded_image'] = image

        if st.button("🔍 Predict E-Waste Type"):
        
            resized_image = image.resize((128, 128))
            img_array = np.expand_dims(np.array(resized_image) / 255.0, axis=0)

            
            prediction = model.predict(img_array)
            predicted_index = np.argmax(prediction)
            predicted_label = class_names[predicted_index]

            
            st.session_state['predicted_class'] = predicted_label

            
            st.success(f"✅ Prediction: **{predicted_label}**")
            st.info("➡️ Go to 'Treatment Info' from the sidebar to see disposal instructions.")


elif page == "Treatment Info":
    st.title("♻️ How to Treat This E-Waste")

    if st.session_state['predicted_class']:
        label = st.session_state['predicted_class']
        treatment = treatment_info.get(label, "No treatment info available.")

        st.subheader(f"🖼️ Identified Item: **{label}**")
        st.markdown(f"🔧 **Treatment Instructions:** {treatment}")

        if st.session_state['uploaded_image']:
            st.image(st.session_state['uploaded_image'], caption="Previously Uploaded Image", width=300)
    else:
        st.warning("Please upload and predict an image first from the 'Upload & Predict' page.")
