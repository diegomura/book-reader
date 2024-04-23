import os
import epub
import orchestrator
import tts
import attacher
from db import db
from pydispatch import dispatcher

dependencies = { "db": db, "dispatcher": dispatcher }

epub.start(dependencies)
orchestrator.start(dependencies)
tts.start(dependencies)
attacher.start(dependencies)

dispatcher.send(signal='epub', data=os.path.join(os.path.dirname(__file__), "test.epub"))
