import io
import typing

import binfile

def test_split():
    buff = io.BytesIO(b'a;b')
    parts = [slice.read() for slice in binfile.split(binfile.File(buff), b';')]
    assert parts == buff.getvalue().split(b';')

    buff = io.BytesIO(b';')
    parts = [slice.read() for slice in binfile.split(binfile.File(buff), b';')]
    assert parts == buff.getvalue().split(b';')

    buff = io.BytesIO(b';;')
    parts = [slice.read() for slice in binfile.split(binfile.File(buff), b';')]
    assert parts == buff.getvalue().split(b';')

    buff = io.BytesIO(b'hello world, this.is.a test ')
    parts = [slice.read() for slice in binfile.split(binfile.File(buff), b" ")]
    assert parts == buff.getvalue().split(b' ')

    buff = io.BytesIO(b'bananabread')
    parts = [slice.read() for slice in binfile.split(binfile.File(buff), b'an')]
    assert parts == buff.getvalue().split(b'an')

def test_split_long_delimiter():
    # delimiter's longer than the file
    buff = io.BytesIO(b'abc')
    parts = [slice.read() for slice in binfile.split(binfile.File(buff), b'thisislongerthanbuff')]
    assert parts == []

    buff = io.BytesIO(b'')
    parts = [slice.read() for slice in binfile.split(binfile.File(buff), b';')]
    assert parts == []
