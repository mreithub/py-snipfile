import io
import logging
import typing

import binfile

def test_split():
    buff = io.BytesIO(b'hello world, this.is.a test ')
    f = binfile.File(buff)

    parts:typing.List[bytes] = []
    for slice in binfile.split(f, b" "):
        parts.append(slice.read())
        logging.error(slice)
    assert parts == buff.getvalue().split(b' ')

