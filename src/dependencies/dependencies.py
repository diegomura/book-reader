from .db import db
from .fs import fs
from .tts import tts
from pydispatch import dispatcher

dependencies = { "db": db, "fs": fs, "tts": tts, "dispatcher": dispatcher }
