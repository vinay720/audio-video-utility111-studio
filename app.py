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

        path = f"temp/{file.name}"

        with open(path, "wb") as f:
            f.write(file.read())

        st.success("File Uploaded Successfully")

        # =========================================
        # COMMON DETAILS
        # =========================================

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

            # OpenCV analysis
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

        # Create ZIP
        zip_path = "outputs/frames.zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for file in os.listdir("frames"):

                zipf.write(
                    f"frames/{file}",
                    file
                )

        st.success("Frames Extracted")

        with open(zip_path, "rb") as f:

            st.download_button(
                "⬇ Download Frames ZIP",
                f,
                file_name="frames.zip"
            )
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

        # Save file
        path = f"temp/{audio_file.name}"

        with open(path, "wb") as f:
            f.write(audio_file.read())

        st.audio(path)

        try:

            # Load audio
            y, sr = librosa.load(path, sr=None)

            # =================================
            # WAVEFORM
            # =================================

            st.subheader("🎵 Waveform")

            fig, ax = plt.subplots(figsize=(10, 4))

            librosa.display.waveshow(
                y,
                sr=sr,
                ax=ax
            )

            ax.set_title("Waveform")

            st.pyplot(fig)

            # =================================
            # SPECTROGRAM
            # =================================

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

            fig2.colorbar(img, ax=ax2, format="%+2.0f dB")

            st.pyplot(fig2)

        except Exception as e:

            st.error(f"Error: {e}")

# ==================================================
# AUDIO TO WAV CONVERTER
# ==================================================

elif menu == "Audio to WAV Converter":

    st.header("🎵 Audio to WAV Converter")

    files = st.file_uploader(
        "Upload Multiple Audio Files",
        type=["wav", "mp3", "ogg", "flac", "m4a", "aac"],
        accept_multiple_files=True
    )

    if files:

        os.makedirs("outputs/batch", exist_ok=True)

        for file in files:

            # Save file
            path = f"temp/{file.name}"

            with open(path, "wb") as f:
                f.write(file.read())

            # =====================================
            # SHOW AUDIO PLAYER
            # =====================================

            st.subheader(f"🎵 {file.name}")

            st.audio(path)

            # =====================================
            # WAVEFORM VISUALIZATION
            # =====================================

            y, sr = librosa.load(path, sr=None)

            fig, ax = plt.subplots(figsize=(10, 3))

            librosa.display.waveshow(
                y,
                sr=sr,
                ax=ax
            )

            ax.set_title("Waveform")

            st.pyplot(fig)

            # =====================================
            # CONVERT TO WAV
            # =====================================

            audio = AudioSegment.from_file(path)

            output_name = file.name.split(".")[0] + ".wav"

            output_path = f"outputs/batch/{output_name}"

            audio.export(
                output_path,
                format="wav"
            )

        # =====================================
        # CREATE ZIP
        # =====================================

        zip_path = "outputs/audio_wav_files.zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for root, dirs, filenames in os.walk("outputs/batch"):

                for filename in filenames:

                    file_path = os.path.join(root, filename)

                    zipf.write(
                        file_path,
                        filename
                    )

        st.success("✅ Conversion Completed")

        # =====================================
        # DOWNLOAD BUTTON
        # =====================================

        with open(zip_path, "rb") as f:

            st.download_button(
                "⬇ Download WAV ZIP",
                f,
                file_name="audio_wav_files.zip"
            )
