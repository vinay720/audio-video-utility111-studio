# app.py

import streamlit as st
import os
import moviepy.editor as mp

# Create folders
os.makedirs("temp", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Streamlit config
st.set_page_config(page_title="Audio + Video Utility Studio")

st.title("🎵🎥 Audio + Video Utility Studio")

menu = st.sidebar.selectbox(
    "Select Tool",
    [
        "Media Analyzer",
        "Extract Audio"
    ]
)

# ====================================
# MEDIA ANALYZER
# ====================================

if menu == "Media Analyzer":

    st.header("📊 Media Analyzer")

    file = st.file_uploader(
        "Upload Audio or Video",
        type=["mp3", "wav", "mp4"]
    )

    if file:

        st.success("File Uploaded Successfully")

        st.write("Filename:", file.name)
        st.write("Type:", file.type)
        st.write("Size:", round(file.size/1024, 2), "KB")

        if "audio" in file.type:
            st.audio(file)

        elif "video" in file.type:
            st.video(file)

# ====================================
# EXTRACT AUDIO
# ====================================

elif menu == "Extract Audio":

    st.header("🎥➡🎵 Extract Audio")

    video = st.file_uploader(
        "Upload Video",
        type=["mp4"]
    )

    if video:

        video_path = "temp/video.mp4"

        with open(video_path, "wb") as f:
            f.write(video.read())

        clip = mp.VideoFileClip(video_path)

        output_audio = "outputs/audio.mp3"

        clip.audio.write_audiofile(output_audio)

        st.success("Audio Extracted Successfully")

        st.audio(output_audio)
