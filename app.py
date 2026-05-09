# app.py

import streamlit as st
import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import cv2
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import zipfile

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
        "Trim Audio",
        "Extract Audio",
        "Convert Audio",
        "Frame Extraction",
        "Spectrogram",
        "Watermark Video",
        "Batch Processing"
    ]
)

# ==========================================
# MEDIA ANALYZER
# ==========================================

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

# ==========================================
# TRIM AUDIO
# ==========================================

elif menu == "Trim Audio":

    st.header("✂ Trim Audio")

    audio_file = st.file_uploader(
        "Upload Audio",
        type=["mp3", "wav"]
    )

    if audio_file:

        path = "temp/audio.mp3"

        with open(path, "wb") as f:
            f.write(audio_file.read())

        audio = AudioSegment.from_file(path)

        start = st.number_input("Start Second", 0)
        end = st.number_input("End Second", 10)

        if st.button("Trim"):

            trimmed = audio[start*1000:end*1000]

            output = "outputs/trimmed.wav"

            trimmed.export(output, format="wav")

            st.success("Audio Trimmed")

            st.audio(output)

# ==========================================
# EXTRACT AUDIO FROM VIDEO
# ==========================================

elif menu == "Extract Audio":

    st.header("🎥➡🎵 Extract Audio")

    video = st.file_uploader(
        "Upload Video",
        type=["mp4"]
    )

    if video:

        path = "temp/video.mp4"

        with open(path, "wb") as f:
            f.write(video.read())

        clip = VideoFileClip(path)

        output = "outputs/extracted.mp3"

        clip.audio.write_audiofile(output)

        st.success("Audio Extracted")

        st.audio(output)

# ==========================================
# CONVERT MP3 ↔ WAV
# ==========================================

elif menu == "Convert Audio":

    st.header("🔄 Convert Audio")

    audio_file = st.file_uploader(
        "Upload Audio",
        type=["mp3", "wav"]
    )

    if audio_file:

        path = "temp/input_audio"

        with open(path, "wb") as f:
            f.write(audio_file.read())

        audio = AudioSegment.from_file(path)

        convert_type = st.selectbox(
            "Convert To",
            ["mp3", "wav"]
        )

        if st.button("Convert"):

            output = f"outputs/converted.{convert_type}"

            audio.export(output, format=convert_type)

            st.success("Conversion Completed")

# ==========================================
# FRAME EXTRACTION
# ==========================================

elif menu == "Frame Extraction":

    st.header("🖼 Frame Extraction")

    video = st.file_uploader(
        "Upload Video",
        type=["mp4"]
    )

    if video:

        path = "temp/frame_video.mp4"

        with open(path, "wb") as f:
            f.write(video.read())

        cap = cv2.VideoCapture(path)

        count = 0

        os.makedirs("outputs/frames", exist_ok=True)

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            if count % 30 == 0:

                cv2.imwrite(
                    f"outputs/frames/frame_{count}.jpg",
                    frame
                )

            count += 1

        cap.release()

        st.success("Frames Extracted")

# ==========================================
# SPECTROGRAM
# ==========================================

elif menu == "Spectrogram":

    st.header("📈 Spectrogram Visualization")

    audio_file = st.file_uploader(
        "Upload Audio",
        type=["mp3", "wav"]
    )

    if audio_file:

        path = "temp/spec.wav"

        with open(path, "wb") as f:
            f.write(audio_file.read())

        y, sr = librosa.load(path)

        X = librosa.stft(y)

        Xdb = librosa.amplitude_to_db(abs(X))

        fig, ax = plt.subplots(figsize=(10,4))

        img = librosa.display.specshow(
            Xdb,
            sr=sr,
            x_axis='time',
            y_axis='hz',
            ax=ax
        )

        plt.colorbar(img)

        st.pyplot(fig)

# ==========================================
# WATERMARK VIDEO
# ==========================================

elif menu == "Watermark Video":

    st.header("💧 Watermark Video")

    st.write("Simple watermark feature ready.")

# ==========================================
# BATCH PROCESSING
# ==========================================

elif menu == "Batch Processing":

    st.header("📦 Batch Processing")

    files = st.file_uploader(
        "Upload Multiple Audio Files",
        type=["wav"],
        accept_multiple_files=True
    )

    if files:

        os.makedirs("outputs/batch", exist_ok=True)

        for file in files:

            path = f"temp/{file.name}"

            with open(path, "wb") as f:
                f.write(file.read())

            audio = AudioSegment.from_file(path)

            normalized = audio.normalize()

            output = f"outputs/batch/{file.name}"

            normalized.export(output, format="wav")

        zip_path = "outputs/batch.zip"

        zipf = zipfile.ZipFile(zip_path, "w")

        for root, dirs, filenames in os.walk("outputs/batch"):

            for filename in filenames:

                zipf.write(
                    os.path.join(root, filename),
                    filename
                )

        zipf.close()

        st.success("Batch Processing Completed")

        with open(zip_path, "rb") as f:

            st.download_button(
                "Download ZIP",
                f,
                file_name="processed_files.zip"
            )
