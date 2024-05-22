import re
import time
from termcolor import cprint
from .model import model

model.register_speaker('diego', './voices/diego')

def compose (*functions):
  def inner(arg):
    for f in reversed(functions):
      arg = f(arg)
    return arg
  return inner

# For some reason TTS model does not like this
def remove_quotations(text):
  pattern = re.compile(r'["\'](.*?)["\']')
  return pattern.sub(r'\1', text)
   
def remove_dobule_shifts(text):
  result = text.replace('<<', '')
  result = result.replace('>>', '')
  return result

prepare_string = compose(
  remove_dobule_shifts,
  remove_quotations
)

def generate(text, language, file_path):
    start_time = time.time()

    # Apply any text correction needed
    text = prepare_string(text)

    #  Split text into sentences
    sens = model.split_into_sentences(text)
    cprint(f'    Sentence: {sens}')

    wavs = []
    for sen in sens:
      waveform = model.synthesize(sen, language, 'diego')
      wavs += waveform
      wavs += [0] * 10000

    process_time = time.time() - start_time
    audio_time = len(wavs) / model.sample_rate

    cprint(f"    Real-time factor: {process_time / audio_time}")

    model.save_wav(wav=wavs, path=file_path)