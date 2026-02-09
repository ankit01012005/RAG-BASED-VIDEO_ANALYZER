import whisper
import json
import os

model = whisper.load_model("large-v2")

audios = os.listdir("tedx_audios")

for audio in audios: 
        number = audio.split("_")[0]
        title = audio.split("_")[1][:-4]
        print(number, title)
        result = model.transcribe(audio = f"tedx_audios/{audio}", 
        # result = model.transcribe(audio = f"tedx_audios/10_modern-connections-dalia-al-otaibi-tedxyouth-bbskuwait-128-ytshorts.savetube.me.mp3", 
                              language="hi",
                              task="translate",
                              word_timestamps=False )
        
        chunks = []
        for segment in result["segments"]:
            chunks.append({"number": number, "title":title, "start": segment["start"], "end": segment["end"], "text": segment["text"]})
        
        chunks_with_metadata = {"chunks": chunks, "text": result["text"]}

        with open(f"jsons/{audio}.json", "w") as f:
            json.dump(chunks_with_metadata,f)