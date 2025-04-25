import streamlit as st
from agents.patient_agent import ask_patientgpt
from agents.translation_agent import translate_to_english
from agents.report_agent import generate_report
from agents.email_agent import send_email
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="PatientGPT Multilingual Assistant")
st.title("🩺 PatientGPT - Multilingual Feedback Assistant")

# Sidebar
st.sidebar.header("Optional Settings")
email = st.sidebar.text_input("Email to send report (optional)")
translate = st.sidebar.checkbox("Translate input to English", value=True)

# Input question
input_text = st.text_area("Enter patient question or feedback:", "Tengo dolor después del tratamiento.")

if st.button("Ask PatientGPT"):
    if translate:
        translated_text = translate_to_english(input_text)
        st.markdown("**Translated to English:**")
        st.success(translated_text)
    else:
        translated_text = input_text

    with st.spinner("Retrieving patient insights..."):
        answer = ask_patientgpt(translated_text)
        st.markdown("**PatientGPT Answer:**")
        st.info(answer)

        report_path = generate_report(translated_text, answer)
        st.download_button("Download Report", open(report_path, "rb"), file_name="patientgpt_report.md")

        if email:
            send_email("Your PatientGPT Report", "Attached is your patient insight report.", email, report_path)
            st.success(f"Report sent to {email}")
