import re
import time
from termcolor import cprint
from .model import model

model.register_speaker('phil', './voices/phil')

# For some reason TTS model does not like this
def remove_quotations(text):
  pattern = re.compile(r'["\'](.*?)["\']')
  return pattern.sub(r'\1', text)
   

def generate(text, language, file_path):
    start_time = time.time()

    # Apply any text correction needed
    text = remove_quotations(text)

    #  Split text into sentences
    sens = model.split_into_sentences(text)
    cprint(f'    Sentence: {sens}')

    wavs = []
    for sen in sens:
      waveform = model.synthesize(sen, language, 'phil')
      wavs += waveform
      wavs += [0] * 10000

    process_time = time.time() - start_time
    audio_time = len(wavs) / model.sample_rate

    cprint(f"    Real-time factor: {process_time / audio_time}")

    model.save_wav(wav=wavs, path=file_path)