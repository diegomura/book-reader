from termcolor import cprint

def start(dependencies):
  db = dependencies["db"]
  dispatcher = dependencies["dispatcher"]

  def process(sender, data):
    book_id = data
    chapters = db.get_chapters(book_id=book_id)

    for chapter in chapters:
      chapter_id = chapter.doc_id
      fragments = db.get_fragments(book_id=book_id, chapter_id=chapter_id)

      for fragment in fragments:
        if "file" in fragment: continue

        cprint(f'Book {book_id}, Chapter {chapter_id}, Fragment {fragment["index"]}', "green")

        dispatcher.send(signal='tts', data={ "fragment_id": fragment.doc_id })

        cprint("")

      if "file" in chapter: continue

      dispatcher.send(signal='attach', data=chapter_id)

      cprint("")

  dispatcher.connect(process, signal='orchestrate', weak=False)
