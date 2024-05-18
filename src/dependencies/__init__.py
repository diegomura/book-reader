from .db import db
from pydispatch import dispatcher

dependencies = { "db": db, "dispatcher": dispatcher }
