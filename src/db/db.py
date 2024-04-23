from tinydb import TinyDB, Query

# This entire db layer is shit. Who cares

db = TinyDB('db.json')

books_table = db.table('books')

chapters_table = db.table('chapters')

fragments_table = db.table('fragments')

def upsert_book(book):
    metadata = book["metadata"]
    content = book["content"]

    existing_book = books_table.get(Query().identifier == metadata["identifier"])

    if existing_book: return existing_book.doc_id

    book_id = books_table.insert(metadata)

    chapter_count = 0

    for chapter in content:
        fragments = []
        chapter_id = chapters_table.insert({ "book_id": book_id, "index": chapter_count })
        fragment_count = 0

        for fragment in chapter:
            fragment["book_id"] = book_id
            fragment["chapter_id"] = chapter_id
            fragment["index"] = fragment_count
            fragment_id = fragments_table.insert(fragment)
            fragments.append(fragment_id)
            fragment_count += 1

        chapter_count += 1

    return book_id

def get_chapters(book_id):
    return chapters_table.search(Query().book_id == book_id)

def get_fragments(book_id=None, chapter_id=None):
    conditions = {}

    if book_id is not None: conditions['book_id']=book_id
    if chapter_id is not None: conditions['chapter_id']=chapter_id
    
    return fragments_table.search(Query().fragment(conditions))

def get_fragment(id):
    return fragments_table.get(doc_id=id)

def update_fragment(id, file):
    return fragments_table.update({ "file": file }, doc_ids=[id])