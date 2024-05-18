from termcolor import cprint

def start(dependencies):
  db = dependencies["db"]
  validator = dependencies["validator"]
  dispatcher = dependencies["dispatcher"]

  def process(sender, data):
    cprint('  Validating Audio', 'yellow')

    fragment_id = data
    fragment = db.get_fragment(fragment_id)
    is_valid = validator.validate(audio_file=fragment["file"], text=fragment["value"], language="en")

    if not is_valid :
      cprint(f'    Regenerating')
      dispatcher.send(signal='tts', data={ "fragment_id": fragment.doc_id })

  dispatcher.connect(process, signal='validate', weak=False)
