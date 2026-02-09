# RAG AI Video Converter — Full Pipeline Overview

This project turns raw videos into searchable, semantically relevant text chunks using a simple Retrieval-Augmented approach. It converts videos to audio, transcribes speech into text, chunks the text, embeds those chunks, and lets you query to find the most relevant parts.

## Overview

- Convert videos to MP3 with FFmpeg.
- Transcribe audio to text with Whisper (`large-v2`), producing segments (chunks) and full text.
- Create embeddings for each chunk using Ollama (`bge-m3`).
- Retrieve top-matching chunks for a user question via cosine similarity.

## Concepts Used

- **Speech-to-Text (STT):** Whisper transcribes spoken audio. In this repo, Whisper runs with `language="hi"` and `task="translate"`, which tells Whisper to transcribe Hindi speech and translate it to English output.
- **Chunking:** The transcript is split into time-stamped segments (start/end/text) that become the unit for retrieval.
- **Embeddings:** Each chunk is converted into a dense vector using Ollama’s embedding API (`bge-m3`). These vectors capture semantic meaning.
- **Retrieval (RAG-style):** A question is embedded, then cosine similarity finds the closest chunk vectors. The top results are shown. (This repo retrieves only; it does not generate an answer from a model.)

## Repository Structure

- [process_video.py](process_video.py): Converts videos in `videos/` to MP3 files in `audios/` using FFmpeg.
- [create_chunks.py](create_chunks.py): Transcribes audio files in `tedx_audios/` with Whisper and writes chunked JSONs to `jsons/`.
- [read_chunks.py](read_chunks.py): Builds embeddings for chunks using Ollama, embeds the user’s question, and returns the most similar chunks.
- [jsons/](jsons): Output JSONs containing `chunks` and full `text` for each audio file.

## Prerequisites (Windows)

- Python 3.10+ recommended
- FFmpeg installed and on PATH (verify with `ffmpeg -version`)
- Ollama installed and running (for embeddings)
- Python packages: `openai-whisper`, `requests`, `numpy`, `pandas`, `scikit-learn`

Install Python packages:

```powershell
pip install openai-whisper requests numpy pandas scikit-learn
```

Install Ollama and pull the embedding model:

```powershell
ollama serve
ollama pull bge-m3
```

## Required Folders

- `videos/` — place your input video files here.
- `audios/` — created by `process_video.py` to store MP3s.
- `tedx_audios/` — input audio folder for `create_chunks.py` (you can copy MP3s from `audios/` here, or adjust the script to point to `audios/`).
- `jsons/` — output JSONs from transcription/chunking.

## Usage

1) Convert videos to MP3:

```powershell
python process_video.py
```

2) Transcribe and create chunk JSONs (heavy model, ensure good CPU/GPU and FFmpeg installed):

```powershell
python create_chunks.py
```

Outputs go to `jsons/` with structure:

```json
{
	"chunks": [
		{"number": "4", "title": "...", "start": 0.0, "end": 4.2, "text": "..."},
		{"number": "4", "title": "...", "start": 4.2, "end": 9.7, "text": "..."}
	],
	"text": "Full transcript text here"
}
```

3) Start Ollama (if not already running) and ensure `bge-m3` is available:

```powershell
ollama serve
ollama list
```

You should see `bge-m3`. If not, pull it:

```powershell
ollama pull bge-m3
```

4) Build embeddings and query the chunks:

```powershell
python read_chunks.py
```

Type your question when prompted. The script embeds the question, computes cosine similarity with all chunk embeddings (from the first JSON file it processes), and prints the top 3 matching chunks.

## Workflow Diagram

```mermaid
flowchart LR
	A[Videos (MP4, etc.)] --> B[FFmpeg]
	B --> C[MP3 Audios]
	C --> D[Whisper (large-v2)]
	D --> E[Chunked JSONs]
	E --> F[Ollama Embeddings (bge-m3)]
	G[User Question] --> H[Question Embedding]
	F --> I[Cosine Similarity]
	H --> I
	I --> J[Top Relevant Chunks]
```

## Notes & Limitations

- Folder names: `create_chunks.py` reads from `tedx_audios/`. If your audios are in `audios/`, either copy them to `tedx_audios/` or modify the script accordingly.
- Language/Task: Whisper uses `language="hi"` and `task="translate"`, producing English output from Hindi speech. Change these parameters if your content differs.
- Title parsing: The `title` is derived from the file name and may be simplistic for multi-underscore names.
- Embedding scope: The current `read_chunks.py` has a `break` after processing the first JSON file, so retrieval only considers chunks from one file. Remove the `break` to search across all JSONs.
- Retrieval only: No answer generation step is included; it returns the most relevant chunks.

## Quick Tips

- Verify FFmpeg with `ffmpeg -version`.
- Make sure Ollama is running (`ollama serve`), and `bge-m3` is pulled.
- Large models like Whisper `large-v2` are resource-intensive; consider smaller models if needed.

## Future Improvements

- Unify folder names (`audios/` vs `tedx_audios/`) or make them configurable.
- Process all JSONs in retrieval (remove `break`) and add ranking across the entire corpus.
- Build a simple UI (e.g., Streamlit) to browse results.
- Add an answer-generation step to complete RAG (retrieve + generate).

