from .db import db
from .fs import fs
from .tts import tts
from .validator import validator
from pydispatch import dispatcher

dependencies = { "db": db, "fs": fs, "tts": tts, "validator": validator, "dispatcher": dispatcher }
