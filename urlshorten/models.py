from collections import UserDict
from . import db
from flask_sqlalchemy import sqlalchemy
from urlshorten.utils import rsg
from url_normalize import url_normalize
from urlshorten.crud import get_short_url, get_long_url
import random

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    BigInteger
)


class Url(db.Model):
    """
    The ORM model for the Url table. I considered storing the `key` property in a separate table linked to the Url table,
    but I couldn't think of a single benefit to doing so since the relationship is one-to-one (thanks to the url norm function).
    """
    __tablename__ = "urls"
    # there's kind of a lot going on here that related to initializing the pseudorandom string generator defined in `utils.py`, but
    # not all of it is strictly necessary. The random string generator can be initialized without a seed, but it's preferable
    # to pass it the most recently generated key since its output is deterministic and a function of the previous output.
    try:
        # if the database is already initialized, we can get the most recently generated key from the database
        most_recent = (
                db.session.execute("SELECT numeric_key FROM urls ORDER BY created DESC LIMIT 1")
                    .fetchone()
                    .key
        )
    except Exception as e:
        print(e.__class__.__name__, e)
        # if the database is not initialized, we can initialize it with a seed of idk, 42?
        most_recent = 42
    seed = most_recent
    rsg = rsg(seed=42) # random string generator.
    id = Column(Integer, primary_key=True, autoincrement=True)
    canonical = Column(String(255), unique=True, index=True, nullable=False)
    key = Column(String(8), unique=True, index=True, nullable=False)
    numeric_key = Column(BigInteger, unique=True, index=True, nullable=False) #definitely gonna need BigInteger for this bad boy
    created = Column(DateTime, default=sqlalchemy.func.now(), nullable=False)

    def __init__(self, url):
        self.canonical = url_normalize(url)
        self.numeric_key, self.key =  next(self.rsg)
