def start(dependencies):
  db = dependencies["db"]
  dispatcher = dependencies["dispatcher"]

  def process(sender, data):
    book_id = data
    fragments = db.get_fragments(book_id=book_id)

    for fragment in fragments:
      dispatcher.send(signal='tts', data=fragment.doc_id)

    dispatcher.send(signal='attach', data=book_id)

  dispatcher.connect(process, signal='orchestrate', weak=False)
