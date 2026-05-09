# app.py

import streamlit as st
import os
import zipfile
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import cv2
import moviepy.editor as mp

from pydub import AudioSegment
from pydub.silence import detect_silence

# =========================
# CREATE FOLDERS
# =========================

os.makedirs("temp", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("frames", exist_ok=True)

# =========================
# STREAMLIT CONFIG
# =========================

st.set_page_config(page_title="Audio + Video Utility Studio")

st.title("🎵🎥 Audio + Video Utility Studio")

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Audio Toolkit",
        "Video Toolkit",
        "Media Analyzer",
        "Frame Processor",
        "Audio Visualizer",
        "Batch Processing"
    ]
)

# =====================================================
# 1. AUDIO TOOLKIT
# =====================================================

if menu == "Audio Toolkit":

    st.header("🎵 Audio Toolkit")

    audio_file = st.file_uploader(
        "Upload Audio",
        type=["mp3", "wav"]
    )

    if audio_file:

        path = "temp/audio"

        with open(path, "wb") as f:
            f.write(audio_file.read())

        st.audio(audio_file)

        audio = AudioSegment.from_file(path)

        # Trim
        st.subheader("✂ Trim Audio")

        start = st.number_input("Start", 0)
        end = st.number_input("End", 10)

        if st.button("Trim"):

            trimmed = audio[start*1000:end*1000]

            output = "outputs/trimmed.wav"

            trimmed.export(output, format="wav")

            st.audio(output)

        # Convert
        st.subheader("🔄 Convert Format")

        convert_type = st.selectbox(
            "Convert To",
            ["mp3", "wav"]
        )

        if st.button("Convert"):

            output = f"outputs/converted.{convert_type}"

            audio.export(output, format=convert_type)

            st.success("Converted Successfully")

        # Normalize
        st.subheader("🔊 Normalize Volume")

        if st.button("Normalize"):

            normalized = audio.normalize()

            output = "outputs/normalized.wav"

            normalized.export(output, format="wav")

            st.audio(output)

        # Silence Detection
        st.subheader("🔇 Silence Detection")

        silence = detect_silence(
            audio,
            min_silence_len=1000,
            silence_thresh=-40
        )

        st.write(silence)

# =====================================================
# 2. VIDEO TOOLKIT
# =====================================================

elif menu == "Video Toolkit":

    st.header("🎥 Video Toolkit")

    video = st.file_uploader(
        "Upload Video",
        type=["mp4"]
    )

    if video:

        video_path = "temp/video.mp4"

        with open(video_path, "wb") as f:
            f.write(video.read())

        st.video(video)

        clip = mp.VideoFileClip(video_path)

        # Trim Video
        st.subheader("✂ Trim Video")

        start = st.number_input("Start Second", 0)
        end = st.number_input("End Second", 10)

        if st.button("Trim Video"):

            trimmed = clip.subclip(start, end)

            output = "outputs/trimmed_video.mp4"

            trimmed.write_videofile(output)

            st.video(output)

        # Extract Audio
        st.subheader("🎵 Extract Audio")

        if st.button("Extract"):

            output = "outputs/audio.mp3"

            clip.audio.write_audiofile(output)

            st.audio(output)

        # Resize
        st.subheader("📉 Resize Video")

        if st.button("Resize 480p"):

            resized = clip.resize(height=480)

            output = "outputs/resized.mp4"

            resized.write_videofile(output)

            st.video(output)

# =====================================================
# 3. MEDIA ANALYZER
# =====================================================

elif menu == "Media Analyzer":

    st.header("📊 Media Analyzer")

    media = st.file_uploader(
        "Upload Media",
        type=["mp3", "wav", "mp4"]
    )

    if media:

        st.write("Filename:", media.name)
        st.write("Size:", round(media.size/1024, 2), "KB")

# =====================================================
# 4. FRAME PROCESSOR
# =====================================================

elif menu == "Frame Processor":

    st.header("🖼 Frame Processor")

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

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            if count % 30 == 0:

                gray = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2GRAY
                )

                edges = cv2.Canny(gray, 100, 200)

                cv2.imwrite(
                    f"frames/frame_{count}.jpg",
                    edges
                )

            count += 1

        cap.release()

        st.success("Frames Saved")

# =====================================================
# 5. AUDIO VISUALIZER
# =====================================================

elif menu == "Audio Visualizer":

    st.header("📈 Audio Visualizer")

    audio_file = st.file_uploader(
        "Upload Audio",
        type=["mp3", "wav"]
    )

    if audio_file:

        path = "temp/audio.wav"

        with open(path, "wb") as f:
            f.write(audio_file.read())

        y, sr = librosa.load(path)

        # Waveform
        st.subheader("Waveform")

        fig, ax = plt.subplots()

        librosa.display.waveshow(
            y,
            sr=sr,
            ax=ax
        )

        st.pyplot(fig)

        # Spectrogram
        st.subheader("Spectrogram")

        X = librosa.stft(y)

        Xdb = librosa.amplitude_to_db(abs(X))

        fig2, ax2 = plt.subplots()

        librosa.display.specshow(
            Xdb,
            sr=sr,
            x_axis='time',
            y_axis='hz',
            ax=ax2
        )

        st.pyplot(fig2)

# =====================================================
# 6. BATCH PROCESSING
# =====================================================

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
