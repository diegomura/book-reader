import os
import whisper

model = whisper.load_model("base")
file = os.path.join(os.path.dirname(__file__), './hallucination.m4a')
print(file)
result = model.transcribe(file)
print(result['text'])
