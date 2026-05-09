# app.py

import streamlit as st

st.set_page_config(page_title="Audio + Video Utility Studio")

st.title("🎵🎥 Audio + Video Utility Studio")

menu = st.sidebar.selectbox(
    "Select Tool",
    [
        "Audio",
        "Video",
        "Analyzer"
    ]
)

# AUDIO TOOLKIT
# =========================

if menu == "Audio":

    st.header("🎵 Audio Toolkit")

    audio = st.file_uploader(
        "Upload Audio",
        type=["mp3", "wav"]
    )

    if audio:

        st.audio(audio)

        st.success("Audio Uploaded Successfully")

# =========================
# VIDEO TOOLKIT
# =========================

elif menu == "Video":

    st.header("🎥 Video Toolkit")

    video = st.file_uploader(
        "Upload Video",
        type=["mp4", "avi", "mov"]
    )

    if video:

        st.video(video)

        st.success("Video Uploaded Successfully")

# =========================
# MEDIA ANALYZER
# =========================

elif menu == "Analyzer":

    st.header("📊 Media Analyzer")

    st.write("Audio + Video Analysis Ready")
