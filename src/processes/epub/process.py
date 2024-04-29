import ebooklib
from unidecode import unidecode
from bs4 import BeautifulSoup
from ebooklib import epub

METADATA_FIELDS = ["title", "creator", "identifier", "date", "description"]

VALID_ELEMENTS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

ELEMENT_TYPES = {
  "h1": "title",
  "h2": "title",
  "h3": "title",
  "h4": "title",
  "h5": "title",
  "h6": "title",
  "p": "paragraph"
}

def get_metadata(book):
  metadata = {}

  for field in METADATA_FIELDS:
    data = book.get_metadata('DC', field)

    if data:
      metadata[field] = data[0][0]
    else:
      metadata[field] = ""

  return metadata

def get_content(book):
  chapters = []

  items = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)

  for item in items:
    chapter = []

    content = item.get_content().decode("utf-8")

    soup = BeautifulSoup(content, "html.parser")

    for element in soup.html.descendants:
      if element.name in VALID_ELEMENTS:
        value = unidecode(element.get_text()).replace("\n", " ").strip()

        if not value: continue

        chapter.append({
          "value": value,
          "type": ELEMENT_TYPES[element.name]
        })

    if len(chapter) == 0: continue

    chapters.append(chapter)

  return chapters

def start(dependencies):
  db = dependencies["db"]
  dispatcher = dependencies["dispatcher"]

  def process(sender, data):
    book = epub.read_epub(data, {"ignore_ncx": True})
    metadata = get_metadata(book)
    content = get_content(book)

    # for testing
    content = content[3:4]
    book = { "metadata": metadata, "content": content }
    book_id = db.upsert_book(book)

    dispatcher.send(signal='orchestrate', data=book_id)

  dispatcher.connect(process, signal='epub', weak=False)
