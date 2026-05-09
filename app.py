import streamlit as st
import os
import zipfile
import cv2
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import moviepy.editor as mp

from pydub import AudioSegment
from pydub.silence import detect_silence

# Create folders
os.makedirs("temp", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Streamlit config
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

# ==================================================
# AUDIO TOOLKIT
# ==================================================

if menu == "Audio Toolkit":

    st.header("🎵 Audio Toolkit")

    audio_file = st.file_uploader(
        "Upload Audio",
        type=["mp3", "wav"]
    )

    if audio_file:

        path = f"temp/{audio_file.name}"

        with open(path, "wb") as f:
            f.write(audio_file.read())

        st.audio(path)

        audio = AudioSegment.from_file(path)

        # Trim Audio
        start = st.number_input("Start", 0)
        end = st.number_input("End", 10)

        if st.button("Trim Audio"):

            trimmed = audio[start*1000:end*1000]

            output = "outputs/trimmed.wav"

            trimmed.export(output, format="wav")

            st.audio(output)

        # Convert Format
        convert_type = st.selectbox(
            "Convert To",
            ["mp3", "wav"]
        )

        if st.button("Convert"):

            output = f"outputs/converted.{convert_type}"

            audio.export(output, format=convert_type)

            st.success("Converted Successfully")

        # Normalize
        if st.button("Normalize Audio"):

            normalized = audio.normalize()

            output = "outputs/normalized.wav"

            normalized.export(output, format="wav")

            st.audio(output)

        # Silence Detection
        silence = detect_silence(
            audio,
            min_silence_len=1000,
            silence_thresh=-40
        )

        st.write("Silence Parts:", silence)

# ==================================================
# VIDEO TOOLKIT
# ==================================================

elif menu == "Video Toolkit":

    st.header("🎥 Video Toolkit")

    video = st.file_uploader(
        "Upload Video",
        type=["mp4"]
    )

    if video:

        path = f"temp/{video.name}"

        with open(path, "wb") as f:
            f.write(video.read())

        st.video(path)

        clip = mp.VideoFileClip(path)

        # Extract Audio
        if st.button("Extract Audio"):

            output = "outputs/audio.mp3"

            clip.audio.write_audiofile(output)

            st.audio(output)

        # Resize
        if st.button("Resize 480p"):

            resized = clip.resize(height=480)

            output = "outputs/resized.mp4"

            resized.write_videofile(output)

            st.video(output)

# ==================================================
# MEDIA ANALYZER
# ==================================================

elif menu == "Media Analyzer":

    st.header("📊 Media Analyzer")

    file = st.file_uploader(
        "Upload Media",
        type=["mp3", "wav", "mp4"]
    )

    if file:

        st.write("Filename:", file.name)
        st.write("Size:", round(file.size/1024, 2), "KB")

        if "audio" in file.type:
            st.audio(file)

        elif "video" in file.type:
            st.video(file)

# ==================================================
# FRAME PROCESSOR
# ==================================================

elif menu == "Frame Processor":

    st.header("🖼 Frame Processor")

    video = st.file_uploader(
        "Upload Video",
        type=["mp4"]
    )

    if video:

        path = f"temp/{video.name}"

        with open(path, "wb") as f:
            f.write(video.read())

        cap = cv2.VideoCapture(path)

        count = 0

        os.makedirs("frames", exist_ok=True)

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            if count % 30 == 0:

                gray = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2GRAY
                )

                edges = cv2.Canny(
                    gray,
                    100,
                    200
                )

                cv2.imwrite(
                    f"frames/frame_{count}.jpg",
                    edges
                )

            count += 1

        cap.release()

        st.success("Frames Extracted")

# ==================================================
# AUDIO VISUALIZER
# ==================================================

elif menu == "Audio Visualizer":

    st.header("📈 Audio Visualizer")

    audio_file = st.file_uploader(
        "Upload Audio",
        type=["mp3", "wav"]
    )

    if audio_file:

        path = f"temp/{audio_file.name}"

        with open(path, "wb") as f:
            f.write(audio_file.read())

        y, sr = librosa.load(path)

        # Waveform
        fig, ax = plt.subplots()

        librosa.display.waveshow(
            y,
            sr=sr,
            ax=ax
        )

        st.pyplot(fig)

# ==================================================
# BATCH PROCESSING
# ==================================================

elif menu == "Batch Processing":

    st.header("📦 Batch Processing")

    files = st.file_uploader(
        "Upload Multiple Files",
        type=["wav", "mp3", "ogg", "flac", "m4a", "aac"],
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

            output_name = file.name.split(".")[0] + ".wav"

            output_path = f"outputs/batch/{output_name}"

            normalized.export(
                output_path,
                format="wav"
            )

        zip_path = "outputs/batch.zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for root, dirs, filenames in os.walk("outputs/batch"):

                for filename in filenames:

                    file_path = os.path.join(root, filename)

                    zipf.write(
                        file_path,
                        filename
                    )

        st.success("Batch Processing Completed")

        with open(zip_path, "rb") as f:

            st.download_button(
                "Download ZIP",
                f,
                file_name="processed_files.zip"
            )
