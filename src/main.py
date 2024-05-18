import os
from db import db
from pydispatch import dispatcher
from processes import epub, orchestrator, tts, attacher, validator

dependencies = { "db": db, "dispatcher": dispatcher }

epub.start(dependencies)
orchestrator.start(dependencies)
tts.start(dependencies)
attacher.start(dependencies)
validator.start(dependencies)

dispatcher.send(signal='epub', data=os.path.join(os.path.dirname(__file__), "hq.epub"))