import time
from whisper_transcriber import WhisperTranscriber
import tempfile
import streamlit as st
import os
from transcript_processor import TranscriptProcessor

st.set_page_config(layout="wide")

# initialize flags
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'page' not in st.session_state:
    st.session_state.page = "Step 1: Process"

# app logo in top left
st.image("../assets/logo.png", width=240)

# sidebar pages synced to session state
page = st.sidebar.radio(
    "Stages",
    ["Step 1: Process", "Step 2: Export"],
    index=0 if st.session_state.page == "Step 1: Process" else 1
)
if page != st.session_state.page:
    st.session_state.page = page

if st.session_state.page == "Step 1: Process":
    # page title and description
    st.subheader("Mind Maps That Write Themselves")
    st.write(
        "Brainstorm freely. We’ll transform your audio entries into a structured map of ideas.")
    st.divider()

    # thought tree name input
    tree_name = st.text_input("Thought Tree Name")
    audio_files = st.file_uploader(
        "Select a minimum of five audio journal entries",
        type=['wav', 'mp3', 'm4a'],
        accept_multiple_files=True
    )

    # only enable when both tree_name and at least one file are provided
    can_process = bool(tree_name and audio_files)
    if st.button("Process Files", disabled=not can_process):
        progress_text = st.empty()
        progress_bar = st.empty()

        # ---- TRANSCRIBING ----
        progress_text.text("Transcribing Files...")
        bar = progress_bar.progress(0)

        def update_progress_transcribe(current, total):
            percent = int(current / total * 100)
            bar.progress(percent)

        with tempfile.TemporaryDirectory() as tmp_dir:
            for upload in audio_files:
                dest = os.path.join(tmp_dir, upload.name)
                with open(dest, "wb") as f:
                    f.write(upload.getbuffer())

            transcriber = WhisperTranscriber(
                progress_callback=update_progress_transcribe)
            transcripts = transcriber.process(tmp_dir)

        # ---- PROCESSING ----
        progress_text.text("Processing Text...")
        bar.progress(0)  # reset progress bar to 0

        def update_progress_process(current, total):
            percent = int(current / total * 100)
            bar.progress(percent)

        processor = TranscriptProcessor(
            transcripts, progress_callback=update_progress_process)

        processor.process_files()

        # store results in session state
        st.session_state.processed = True
        st.session_state.tree_name = tree_name
        st.session_state.transcripts = transcripts
        st.session_state.page = "Step 2: Export"
        st.rerun()

elif st.session_state.page == "Step 2: Export":
    if not st.session_state.processed:
        st.error("Please complete Step 1: Process first")
    else:
        st.title("Export Mind Map")
        st.write(f"thought tree: {st.session_state.tree_name}")
        # display transcripts or export logic here
        for name, text in st.session_state.transcripts.items():
            st.markdown(f"**{name}**")
            st.write(text)
