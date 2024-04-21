import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from pydispatch import dispatcher

METADATA_FIELDS = ["title", "creator", "identifier", "date", "description"]

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
      if element.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        section = {}
        value = element.get_text().replace(u'\xa0', u'')

        if not value: continue

        section["type"] = ELEMENT_TYPES[element.name]
        section["value"] = value
 
        chapter.append(section)

    if len(chapter) == 0: continue

    chapters.append(chapter)

  return chapters


def process_epub(sender, data):
  print(f'processing epub, {data}')

  book = epub.read_epub(data)

  metadata = get_metadata(book)
  content = get_content(book)

  # for testing
  content = content[:4]

  story = { "metadata": metadata, "content": content }

  dispatcher.send(signal='book_data', data=story)


dispatcher.connect(
  process_epub,
  signal='epub_file',
  sender=dispatcher.Any
)
