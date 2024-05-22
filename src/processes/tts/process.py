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
    chapter_id = fragment["chapter_id"]
    chapter = db.get_chapter(chapter_id)

    if iteration >= ITERATION_THRESHOLD: return

    cprint('  Generating Audio', 'yellow')

    file_path = fs.get_path_for(f'{fragment["book_id"]}_{chapter["index"]}_{fragment["index"]}.wav')

    try:
      tts.generate(text=fragment['value'], language="es", file_path=file_path)
    except Exception as error:
      cprint(f"    Error synthesizing sentence: {error}", 'red')
      return

    db.update_fragment(fragment_id, file=file_path)

    dispatcher.send(signal='validate', data={ "fragment_id": fragment_id, "iteration": iteration })

  dispatcher.connect(process, signal='tts', weak=False)
