import os
import torch
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

def start(dependencies):
  db = dependencies["db"]

  def process(sender, data):
    fragment_id = data
    fragment = db.get_fragment(fragment_id)

    # If fragment was processed, skip it
    if "file" in fragment: return

    # TODO: add voices once supported
    # voice = data['voice']

    voice = "narrator"
    speaker = get_speaker(voice)
    file_name = f'{fragment["book_id"]}_{fragment["chapter_id"]}_{fragment["index"]}.wav'
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    tts.tts_to_file(
      text=fragment['value'],
      speaker_wav=speaker,
      language="es",
      file_path=file_path,
    )

    db.update_fragment(fragment_id, file=file_path)

  dispatcher.connect(process, signal='tts', weak=False)
