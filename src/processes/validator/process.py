import whisper
from unidecode import unidecode
from Levenshtein import distance

model = whisper.load_model("base")

chars_to_remove = set(['¡', '!', '.', ',', ':', '…', '—', '-', '¿', '?', '"', "'"])

distance_threshold = 10

def get_distance_threshold(string):
  return max(len(string) // 10, 10)

def remove_punctuation(string):
  return ''.join([c for c in string if c not in chars_to_remove])

def remove_consecutive_spaces(string):
  return ' '.join(string.split())

def prepare_string(string):
  return remove_consecutive_spaces(remove_punctuation(unidecode(string).lower().rstrip().lstrip()))

def start(dependencies):
  db = dependencies["db"]
  dispatcher = dependencies["dispatcher"]

  def process(sender, data):
    print('validate', data)

    fragment_id = data
    fragment = db.get_fragment(fragment_id)

    transcription = model.transcribe(fragment["file"], language="en", fp16=False)

    source = prepare_string(fragment["value"])
    target = prepare_string(transcription["text"])

    dist = distance(source, target)

    if dist > get_distance_threshold(source):
       print('regenerating', data)
       print(source)
       print(target)
       print(dist)
       dispatcher.send(signal='tts', data={ "fragment_id": fragment.doc_id, "force": True })



  dispatcher.connect(process, signal='validate', weak=False)
