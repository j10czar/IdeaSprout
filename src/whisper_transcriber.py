import whisper
import tempfile
import os
from pathlib import Path
import torch
# Clears torch path so it doesnt conflict with streamlit
torch.classes.__path__ = []


class WhisperTranscriber:

    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.model = whisper.load_model("base")

    def process(self, folder_path):
        files = list(Path(folder_path).glob("*"))
        total = len(files)
        transcripts = {}
        for idx, f in enumerate(files, start=1):
            # transcribe audio file
            result = self.model.transcribe(str(f))
            transcripts[f.name] = result.get("text", "")
            # update streamlit progress
            if self.progress_callback:
                self.progress_callback(idx, total)
        return transcripts
