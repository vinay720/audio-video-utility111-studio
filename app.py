# =========================================================
# 🎵🎥 AUDIO + VIDEO UTILITY STUDIO
# =========================================================

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

# =========================================================
# CREATE FOLDERS
# =========================================================

os.makedirs("temp", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("frames", exist_ok=True)

# =========================================================
# STREAMLIT CONFIG
# =========================================================

st.set_page_config(
    page_title="Audio + Video Utility Studio",
    layout="wide"
)

st.title("🎵🎥 Audio + Video Utility Studio")

# =========================================================
# SIDEBAR MENU
# =========================================================

menu = st.sidebar.selectbox(
    "Select Module",
    [
        "Audio Toolkit",
        "Video Toolkit",
        "Media Analyzer",
        "Frame Processor",
        "Audio Visualizer",
        "Audio converter"
    ]
)

# =========================================================
# 1. AUDIO TOOLKIT
# =========================================================

if menu == "Audio Toolkit":

    st.header("🎵 Audio Toolkit")

    audio_file = st.file_uploader(
        "Upload Audio",
        type=["mp3", "wav", "ogg", "flac", "aac", "m4a"]
    )

    if audio_file:

        path = f"temp/{audio_file.name}"

        with open(path, "wb") as f:
            f.write(audio_file.read())

        st.audio(path)

        audio = AudioSegment.from_file(path)

        # =========================================
        # TRIM AUDIO
        # =========================================

        st.subheader("✂ Trim Audio")

        start = st.number_input("Start Time (sec)", 0)
        end = st.number_input("End Time (sec)", 10)

        if st.button("Trim Audio"):

            trimmed = audio[start*1000:end*1000]

            output = "outputs/trimmed.wav"

            trimmed.export(output, format="wav")

            st.success("Audio Trimmed")

            st.audio(output)

        # =========================================
        # CONVERT FORMAT
        # =========================================

        st.subheader("🔄 Convert Format")

        convert_type = st.selectbox(
            "Convert To",
            ["mp3", "wav"]
        )

        if st.button("Convert Audio"):

            output = f"outputs/converted.{convert_type}"

            audio.export(output, format=convert_type)

            st.success("Conversion Completed")

        # =========================================
        # NORMALIZE AUDIO
        # =========================================

        st.subheader("🔊 Normalize Volume")

        if st.button("Normalize Audio"):

            normalized = audio.normalize()

            output = "outputs/normalized.wav"

            normalized.export(output, format="wav")

            st.audio(output)

        # =========================================
        # SILENCE DETECTION
        # =========================================

        st.subheader("🔇 Silence Detection")

        silence = detect_silence(
            audio,
            min_silence_len=1000,
            silence_thresh=-40
        )

        st.write("Silent Regions:", silence)

# =========================================================
# 2. VIDEO TOOLKIT
# =========================================================

elif menu == "Video Toolkit":

    st.header("🎥 Video Toolkit")

    video = st.file_uploader(
        "Upload Video",
        type=["mp4", "avi", "mov"]
    )

    if video:

        path = f"temp/{video.name}"

        with open(path, "wb") as f:
            f.write(video.read())

        st.video(path)

        clip = mp.VideoFileClip(path)

        # =========================================
        # TRIM VIDEO
        # =========================================

        st.subheader("✂ Trim Video")

        start = st.number_input("Start Second", 0)
        end = st.number_input("End Second", 10)

        if st.button("Trim Video"):

            trimmed = clip.subclip(start, end)

            output = "outputs/trimmed_video.mp4"

            trimmed.write_videofile(output)

            st.video(output)

        # =========================================
        # EXTRACT AUDIO
        # =========================================

        st.subheader("🎵 Extract Audio")

        if st.button("Extract Audio"):

            output = "outputs/extracted_audio.mp3"

            clip.audio.write_audiofile(output)

            st.audio(output)

        # =========================================
        # RESIZE VIDEO
        # =========================================

        st.subheader("📉 Resize Video")

        if st.button("Resize to 480p"):

            resized = clip.resize(height=480)

            output = "outputs/resized_video.mp4"

            resized.write_videofile(output)

            st.video(output)

# =========================================================
# 3. MEDIA ANALYZER
# =========================================================

elif menu == "Media Analyzer":

    st.header("📊 Media Analyzer")

    file = st.file_uploader(
        "Upload Media",
        type=["mp3", "wav", "mp4"]
    )

    if file:

        path = f"temp/{file.name}"

        with open(path, "wb") as f:
            f.write(file.read())

        st.success("File Uploaded Successfully")

        st.write("📁 Filename:", file.name)

        st.write("📦 File Size:", round(file.size / 1024, 2), "KB")

        # =========================================
        # AUDIO ANALYSIS
        # =========================================

        if "audio" in file.type:

            audio = AudioSegment.from_file(path)

            st.subheader("🎵 Audio Information")

            duration = len(audio) / 1000

            st.write("⏱ Duration:", duration, "Seconds")

            st.write("🔊 Channels:", audio.channels)

            st.write("🎚 Sample Rate:", audio.frame_rate, "Hz")

            st.write("💾 Bit Depth:", audio.sample_width * 8, "bits")

            st.audio(path)

        # =========================================
        # VIDEO ANALYSIS
        # =========================================

        elif "video" in file.type:

            clip = mp.VideoFileClip(path)

            st.subheader("🎥 Video Information")

            st.write("⏱ Duration:", round(clip.duration, 2), "Seconds")

            st.write("🎞 FPS (Frames Per Second):", clip.fps)

            st.write("📺 Resolution:", clip.size)

            cap = cv2.VideoCapture(path)

            frame_count = int(
                cap.get(cv2.CAP_PROP_FRAME_COUNT)
            )

            bitrate = int(
                cap.get(cv2.CAP_PROP_BITRATE)
            )

            st.write("🖼 Total Frames:", frame_count)

            st.write("💾 Bitrate:", bitrate, "bps")

            cap.release()

            st.video(path)

# =========================================================
# 4. FRAME PROCESSOR
# =========================================================

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

        # ZIP FRAMES
        zip_path = "outputs/frames.zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for file_name in os.listdir("frames"):

                zipf.write(
                    f"frames/{file_name}",
                    file_name
                )

        st.success("Frames Extracted")

        with open(zip_path, "rb") as f:

            st.download_button(
                "⬇ Download Frames ZIP",
                f,
                file_name="frames.zip"
            )

# =========================================================
# 5. AUDIO VISUALIZER
# =========================================================

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

        st.audio(path)

        try:

            y, sr = librosa.load(path, sr=None)

            # =========================================
            # WAVEFORM
            # =========================================

            st.subheader("🎵 Waveform")

            fig, ax = plt.subplots(figsize=(10, 4))

            librosa.display.waveshow(
                y,
                sr=sr,
                ax=ax
            )

            ax.set_title("Waveform")

            st.pyplot(fig)

            # =========================================
            # SPECTROGRAM
            # =========================================

            st.subheader("📊 Spectrogram")

            D = librosa.stft(y)

            S_db = librosa.amplitude_to_db(
                np.abs(D),
                ref=np.max
            )

            fig2, ax2 = plt.subplots(figsize=(10, 4))

            img = librosa.display.specshow(
                S_db,
                sr=sr,
                x_axis='time',
                y_axis='log',
                ax=ax2
            )

            ax2.set_title("Spectrogram")

            fig2.colorbar(img, ax=ax2)

            st.pyplot(fig2)

        except Exception as e:

            st.error(f"Error: {e}")

# =========================================================
# 6. BATCH PROCESSING
# =========================================================

elif menu == "Audio converter":

    st.header("📦 Batch Processing")

    files = st.file_uploader(
        "Upload Multiple Audio Files",
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

        # CREATE ZIP
        zip_path = "outputs/batch.zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for root, dirs, filenames in os.walk("outputs/batch"):

                for filename in filenames:

                    file_path = os.path.join(root, filename)

                    zipf.write(
                        file_path,
                        filename
                    )

        st.success("✅ Batch Processing Completed")

        with open(zip_path, "rb") as f:

            st.download_button(
                "⬇ Download Processed ZIP",
                f,
                file_name="processed_files.zip"
            )
