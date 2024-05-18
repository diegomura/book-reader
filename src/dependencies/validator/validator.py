import re
import whisper
from termcolor import cprint
from num2words import num2words
from unidecode import unidecode
from Levenshtein import distance

model = whisper.load_model("base")

chars_to_remove = set(['¡', '!', '.', ',', ':', '…', '—', '-', '¿', '?', '"', "'", '(', ')'])

distance_threshold = 8

length_threshold = 30

def compose (*functions):
  def inner(arg):
    for f in reversed(functions):
      arg = f(arg)
    return arg
  return inner

def lower(string):
  return string.lower()

def trim(string):
  return string.rstrip().lstrip()

def get_distance_threshold(string):
  return max(len(string) // length_threshold, distance_threshold)

def remove_punctuation(string):
  return ''.join([c for c in string if c not in chars_to_remove])

def remove_consecutive_spaces(string):
  return ' '.join(string.split())

def nums_to_words(string):
  return ' '.join([num2words(word, lang='en') if word.isdigit() else word for word in string.split()])

def override_currency(string):
  pattern = r'\$(\d+(\.\d+)?)'

  def replace_match(match):
    number = match.group(1)
    return f"{number} dollars"

  replaced_text = re.sub(pattern, replace_match, string)

  return replaced_text

prepare_string = compose(
  nums_to_words,
  remove_consecutive_spaces,
  remove_punctuation,
  override_currency,
  trim,
  lower,
  unidecode
)

def validate(audio_file, text, language):
    transcription = model.transcribe(audio_file, language=language, fp16=False)

    source = prepare_string(text)
    target = prepare_string(transcription["text"])
    dist = distance(source, target)
    threshold = get_distance_threshold(source)

    cprint(f'    Fragment:      {source}')
    cprint(f'    Transcription: {target}')
    cprint(f'    Distance:      {dist}/{threshold}')

    return dist < threshold
