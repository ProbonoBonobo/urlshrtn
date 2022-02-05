"""
utils.py
A collection of utility functions for the urlshorten application. Notably this contains generator functions related to the shortening
process, and also contains the logic for interpolating those codes into the current app's url structure.

"""
import random
import string
import typing
import collections
import warnings
from typing import Generator


def lcg(
    modulus: int = 2**48 - 69,
    a: int = 49235258628958,
    c: int = 253087341916107,
    seed: int = 42,
) -> Generator[int, None, None]:
    """
    Generate a pseudorandom integer using the LCG algorithm. This is literally copy/pasted from Wikipedia [1] with parameter values
    chosen from this table [2] published by the American Mathematical Society. Specifically these values ensure a maximum decimal
    length of 48 digits, which we can then pad to generate a bytearray of exactly 8 6-bit integers.

    The motivation for this is that we want to generate a unique, random, URL key without having to worry about collisions. LCG
    promises outputs similar to `random.sample` without replacement -- but without the overhead of storing hundreds of trillions
    of digits in memory. Thanks, numerical analysis!

    [1] https://en.wikipedia.org/wiki/Linear_congruential_generator
    [2] https://www.ams.org/journals/mcom/1999-68-225/S0025-5718-99-00996-5/S0025-5718-99-00996-5.pdf

    :param m: modulus
    :param a: multiplier
    :param c: increment
    :param seed: random seed value
    :return: iterator of unique (!) pseudorandom integers

    """
    while True:
        seed = (a * seed + c) % modulus
        yield seed


def gen_str(it, length=8):
    """
    Generate a random string of length characters
    """
    # define an alphabet of 64 characters with valid URL-safe characters. This is a pretty unique subset of printable ASCII
    html_safe = string.ascii_letters + string.digits
    # i don't love these extra punctuation characters, but they get us to 64 which is highly desirable
    html_safe += "-_"
    transtable = {i: ch for i, ch in enumerate(html_safe)}
    while True:
        seed = next(it)
        # 6 relates to the upper bound of the decimal output range, which in this case is `2**6` or `64`
        binstr = bin(seed)[2:].zfill(length * 6)[: length * 6]
        yield seed, "".join(
            # I vaguely remember reading that it's better to use the `str.translate` methods here because something
            # something they interface directly with ctypes, but I don't remember how to use that
            transtable[int(binstr[i : i + 6], 2)]
            for i in range(0, len(binstr), 6)
        )


def rsg(length=8, seed=42):
    """
    Putting the previous functions together, generate a random string of length characters
    :param length: int length of the string
    :param seed: int seed value, ideally the
    :return:
    """
    it = gen_str(lcg(seed=seed), length=8)
    while True:
        yield next(it)


def urlify(url_key: str) -> str:
    """
    Convert a URL key to a valid URL.
    """
    from routes import app

    return f"{app.config['SCHEME'].rstrip(':/')}://{app.config['HOSTNAME']}/{url_key}"
