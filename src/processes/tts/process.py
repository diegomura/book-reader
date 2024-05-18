import os
import time
from termcolor import cprint
from pydispatch import dispatcher
from .model import model

def start(dependencies):
  db = dependencies["db"]

  model.register_speaker('phil', './voices/phil')

  def process(sender, data):
    force = data["force"]
    fragment_id = data["fragment_id"]
    fragment = db.get_fragment(fragment_id)

    # If fragment was processed, skip it
    if not force and "file" in fragment: 
      cprint('  Skipped')
      return
    
    cprint('  Generating Audio', 'yellow')

    file_name = f'{fragment["book_id"]}_{fragment["chapter_id"]}_{fragment["index"]}.wav'
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    text = fragment['value']

    language = 'en'
    start_time = time.time()

    #  Split text into sentences
    sens = model.split_into_sentences(text)
    cprint(f'    Sentence: {sens}')

    wavs = []
    for sen in sens:
      try:
        waveform = model.synthesize(sen, language, 'phil')
      except:
        cprint(f"    Error synthesizing sentence", 'red')
        return

      wavs += waveform
      wavs += [0] * 10000

    process_time = time.time() - start_time
    audio_time = len(wavs) / model.sample_rate

    cprint(f"    Real-time factor: {process_time / audio_time}")

    model.save_wav(wav=wavs, path=file_path)

    db.update_fragment(fragment_id, file=file_path)

    dispatcher.send(signal='validate', data=fragment_id)

  dispatcher.connect(process, signal='tts', weak=False)
