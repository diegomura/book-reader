import os
from pydispatch import dispatcher
from db import connection
from epub import process
from orchestrator import process
# from tts import process

# connection.execute("""
#   INSERT INTO book (name) VALUES ('Test');
# """)

dispatcher.send(signal='epub_file', data=os.path.join(os.path.dirname(__file__), "test.epub"))
