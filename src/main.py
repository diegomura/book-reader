import os
from dependencies import dependencies
from processes import epub, orchestrator, tts, attacher, validator

epub.start(dependencies)
orchestrator.start(dependencies)
tts.start(dependencies)
attacher.start(dependencies)
validator.start(dependencies)

dependencies['dispatcher'].send(signal='epub', data=os.path.join(os.path.dirname(__file__), "hq.epub"))