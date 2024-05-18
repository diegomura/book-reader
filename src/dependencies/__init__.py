from .db import db
from .fs import fs
from pydispatch import dispatcher

dependencies = { "db": db, "fs": fs, "dispatcher": dispatcher }
