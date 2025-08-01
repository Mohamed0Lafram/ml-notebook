import streamlit as st
import joblib
import pandas as pd
from preprocessing import Preprocessing
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- Email Configuration ---
sender_email = "mohamedlafram500@gmail.com"
password = "lieb quyj cbjw ziol"  

receiver_email = "mohamedlafram004@gmail.com"

subject = 'Waze'
body  = """Vous avez utilisé Waze pour vos trajets, et nous vous remercions de votre confiance.

Waze est bien plus qu’un simple outil de navigation. En l’utilisant régulièrement, vous bénéficiez de nombreux avantages concrets :

Des itinéraires optimisés en temps réel selon les conditions de circulation

Des alertes précises sur les incidents, les ralentissements ou les zones de danger

Une communauté active qui partage ses informations pour améliorer vos trajets

En continuant à utiliser Waze, vous gagnez du temps, améliorez votre confort de conduite, et contribuez à une meilleure expérience pour tous.

Nous espérons vous accompagner encore longtemps sur la route.

Cordialement,
L’équipe Waze"""


def send_email(recipient,subject,body):
    try:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject

        message.attach(MIMEText(body,'plain'))

        with smtplib.SMTP('smtp.gmail.com',587) as server:
            server.starttls()
            server.login(sender_email,password)
            server.sendmail(sender_email,recipient,message.as_string())
        print('email sended')
    except Exception as e:
        print(f'erreur {e}')



# --- Load Model ---
model = joblib.load('pipeline.pkl')

# --- App Title ---
st.title("📊 User Retention Prediction App")

st.markdown("Use the sliders below to enter user activity data and predict whether the user will continue using the app.")

# --- Input Form ---
st.header("📥 User Activity Inputs")

col1, col2 = st.columns(2)

with col1:
    session = st.slider("🖥️ Sessions", 0, 300, 50)
    Drives = st.slider("🚗 Drives", 0, 300, 50)
    total_sessions = st.slider("📈 Total Sessions", 0.0, 300.0, 5.0)
    n_days_after_onboarding = st.slider("📅 Days After Onboarding", 0, 4000, 120)
    total_navigations_fav1 = st.slider("📍 Navigations Favorite 1", 0, 300, 50)
    total_navigations_fav2 = st.slider("📍 Navigations Favorite 2", 0.0, 300.0, 5.0)

with col2:
    driven_km_drives = st.slider("🛣️ Driven KM (Drives)", 0.0, 7000.0, 500.0)
    duration_minutes_drives = st.slider("⏱️ Duration (Minutes, Drives)", 0.0, 7000.0, 500.0)
    activity_days = st.slider("📆 Activity Days", 0, 100, 5)
    driving_days = st.slider("🚘 Driving Days", 0, 100, 5)
    device = st.selectbox("📱 Device Type", ["android", "iphone"])

# --- Prepare Data ---
X = pd.DataFrame({
    "ID": [0],
    "sessions": [session],
    "drives": [Drives],
    "total_sessions": [total_sessions],
    "n_days_after_onboarding": [n_days_after_onboarding],
    "total_navigations_fav1": [total_navigations_fav1],
    "total_navigations_fav2": [total_navigations_fav2],
    "driven_km_drives": [driven_km_drives],
    "duration_minutes_drives": [duration_minutes_drives],
    "activity_days": [activity_days],
    "driving_days": [driving_days],
    "device": [0 if device == 'android' else 1]
})

# --- Prediction Section ---
st.header("🔍 Prediction")

if st.button("📤 Predict"):
    prediction = model.predict(X)
    
    if prediction[0] == 0:
        st.error("🚨 Result: The user is likely to stop using the app.")
    else:
        st.success("✅ Result: The user is likely to continue using the app.")
    
        # Nested button for sending email
    if st.button("📧 Send Result via Email"):
            send_email(receiver_email,subject,body)
            print('cheack email')
# For debugging / development

