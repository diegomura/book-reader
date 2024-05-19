from tinydb import TinyDB, Query

# This entire db layer is shit. Who cares

db = TinyDB('db.json')

books_table = db.table('books')

chapters_table = db.table('chapters')

fragments_table = db.table('fragments')

def get_all_books():
    return books_table.all()

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

def get_book(id):
    return books_table.get(doc_id=id)

def remove_book(id):
    fragments_table.remove(Query().book_id == id)
    chapters_table.remove(Query().book_id == id)
    books_table.remove(doc_ids=[id])

def get_book_progress(id):
    fragments = list(get_fragments(book_id=id))
    completed = [fragment for fragment in fragments if "file" in fragment]
    progress = len(completed) / len(fragments)
    return { "progress": progress, "completed": len(completed), "total": len(fragments) }

def get_chapter(id):
    return chapters_table.get(doc_id=id)

def get_chapters(book_id):
    return chapters_table.search(Query().book_id == book_id)

def get_chapter_contents(id):
    fragments = get_fragments(chapter_id=id)
    return '\n'.join([fragment["value"] for fragment in fragments])

def update_chapter(id, file):
    return chapters_table.update({ "file": file }, doc_ids=[id])

def remove_chapter(id):
    fragments_table.remove(Query().chapter_id == id)
    chapters_table.remove(doc_ids=[id])

def get_all_fragments():
    return fragments_table.all()

def get_fragments(book_id=None, chapter_id=None):
    conditions = {}

    if book_id is not None: conditions['book_id']=book_id
    if chapter_id is not None: conditions['chapter_id']=chapter_id

    return fragments_table.search(Query().fragment(conditions))

def get_fragment(id):
    return fragments_table.get(doc_id=id)

def update_fragment(id, file):
    return fragments_table.update({ "file": file }, doc_ids=[id])
