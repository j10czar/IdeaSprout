from mistral_model import format_prompt_summary, format_prompt_master, call_mistral


class TranscriptProcessor:
    def __init__(self, transcripts, progress_callback) -> None:
        self.transcripts = transcripts
        self.transcript_list = list(transcripts.values())
        self.progress_callback = progress_callback
        self.summary_list = []

    def process_files(self):
        total = len(self.transcript_list)
        for i, file in enumerate(self.transcript_list):
            prompt = format_prompt_summary(file)
            response = call_mistral(prompt)
            self.summary_list.append(response.strip())
            if self.progress_callback:
                self.progress_callback(i + 1, total)
        print(self.summary_list)
