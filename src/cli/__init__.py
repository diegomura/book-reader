import click
from dependencies.db import db

@click.group()
def main():
    pass

@main.command(help="List all books")
# @click.option("--a", prompt=" Enter the first number", type=int)
# @click.option("--b", prompt=" Enter the second number", type=int)
def ls():
    books = db.get_all_books()

    for book in books:
        id = click.style(book.doc_id, fg='green')
        title = click.style(book["title"], fg='yellow')
        creator = click.style(book["creator"])
        progress_stats = db.get_book_progress(book.doc_id)
        progress = f'({progress_stats["completed"]}/{progress_stats["total"]} - {progress_stats["progress"]:.0%})'

        click.echo(f'{id}  {title} - {creator} {progress}')

@main.command(help="Remove a book")
@click.option("--id", prompt="Enter book id", type=int)
def rm(id):
    book = db.get_book(id)

    if not book:
        click.echo(f"Book with id {id} found")
        return

    if click.confirm('Do you want to continue?'):
        db.remove_book(id)
        click.echo("Book removed")

@main.command(help="Remove a chapter")
@click.option("--id", prompt="Enter chapter id", type=int)
def rmc(id):
    chapter = db.get_chapter(id)

    if not chapter:
        click.echo(f"Chapter with id {id} found")
        return

    if click.confirm('Do you want to continue?'):
        db.remove_chapter(id)
        click.echo("Chapter removed")

if __name__ == "__main__":
    main()
