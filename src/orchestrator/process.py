from pydispatch import dispatcher

def orchestrate_book(sender, data):
  print(f'orchestrating book')

  script = [element for chapter in data["content"] for element in chapter]

  id = 0

  for item in script:
    item["id"] = id
    dispatcher.send(signal='tts', data=item)
    id += 1


  print(f'book orchestrated')


dispatcher.connect(
  orchestrate_book,
  signal='book_data',
  sender=dispatcher.Any,
)
