import streamlit as st

from speech import start_recording
from speech import stop_recording

from transcriber import transcribe
from translator import translate_to_english

st.set_page_config(
    page_title="Forthright AI",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 Forthright AI")
st.write("Multilingual Speech-to-Text and English Translation")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎙️ Start Recording"):
        start_recording()
        st.success("Recording Started")

with col2:
    if st.button("⏹️ Stop Recording"):

        st.info("Stopping Recording...")

        audio_path = stop_recording()

        st.info("Transcribing Audio...")

        original_text = transcribe(audio_path)

        st.success("Transcription Completed")

        st.subheader("Original Transcript")

        st.text_area(
            "Original Transcript",
            original_text,
            height=150
        )

        st.info("Translating To English...")

        english_text = translate_to_english(
            original_text
        )

        st.success("Translation Completed")

        st.subheader("English Translation")

        st.text_area(
            "English Translation",
            english_text,
            height=150
        )