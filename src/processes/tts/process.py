from termcolor import cprint
from pydispatch import dispatcher

ITERATION_THRESHOLD = 5

def start(dependencies):
  db = dependencies["db"]
  tts = dependencies["tts"]
  fs = dependencies["fs"].namespace('fragments')

  def process(sender, data):
    iteration = data["iteration"]
    fragment_id = data["fragment_id"]
    fragment = db.get_fragment(fragment_id)

    if iteration >= ITERATION_THRESHOLD: return

    cprint('  Generating Audio', 'yellow')

    file_path = fs.get_path_for(f'{fragment["book_id"]}_{fragment["chapter_id"]}_{fragment["index"]}.wav')

    try:
      tts.generate(text=fragment['value'], language="en", file_path=file_path)
    except:
      cprint(f"    Error synthesizing sentence", 'red')
      return

    db.update_fragment(fragment_id, file=file_path)

    dispatcher.send(signal='validate', data={ "fragment_id": fragment_id, "iteration": iteration })

  dispatcher.connect(process, signal='tts', weak=False)
