"""
crud.py
Database CRUD operations required elsewhere in the application. This isn't
just about keeping the logic neat and tidy, but also to enable in-memory
caching of relatively time consuming database queries.

I'll briefly note here that I'd probably use Redis or Memcached in place of
Python's built-in `functools.lru_cache` decorator if this were a production
application, but those three simple lines of code are functionally equivalent.
"""
from functools import lru_cache


@lru_cache(maxsize=2**8)
def fetch_single_entity(**kwargs):
    """Return an ORM object from the database matching the given criteria."""
    # don't import the db model at the top of the file, it's a circular import
    from urlshorten.models import Url

    return Url.query.filter_by(**kwargs).first()


@lru_cache(maxsize=2**8)
def get_short_url(long_url):
    """Return the short URL for the given long URL. It is *strongly* recommended
    to normalize the URL before passing it in, because URLs are always normalized
    before they are stored.

    In production, I might even create a lightweight, user-defined subclass of `str` called
    NormalizedUrl to earmark URLs that have passed this step, and explicitly
    canonicalize arguments that aren't instances of that class."""
    entity = fetch_single_entity(canonical=long_url)
    return entity.key if entity else None


@lru_cache(maxsize=2**8)
def get_long_url(short_url):
    """Return the long URL for the given short URL."""
    entity = fetch_single_entity(key=short_url)
    return entity.canonical if entity else None
