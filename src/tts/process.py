import os
import torch
from os.path import isfile, join
from TTS.api import TTS
from pydispatch import dispatcher

device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

speakers = {
  'narrator': './voices/william',
  'sarah': './voices/emma',
  'david': './voices/geralt',
}

def get_speaker(voice):
  cwd = os.path.dirname(__file__)
  voice_path = os.path.join(cwd, speakers[voice])
  files = os.listdir(voice_path)

  return [os.path.join(voice_path, f) for f in files]

def process_tts(sender, data):
  print(f'tts on {data}')

  id = data['id']
  text = data['text']
  voice = data['voice']
  speaker = get_speaker(voice)
  file_path = os.path.join(os.path.dirname(__file__), f'{id}.wav')

  tts.tts_to_file(
    text=text,
    speaker_wav=speaker,
    language="en",
    file_path=file_path,
  )

dispatcher.connect(
  process_tts,
  signal='tts',
  sender=dispatcher.Any,
)
