import io
import os

import binfile

def test_seek():
    slice = binfile.Slice(binfile.fromBytes(b'hello, my dear world'), offset=7, size=7) # "my dear"
    assert slice.read() == b'my dear'
    assert slice.read() == b''

    slice.seek(0, os.SEEK_SET)
    assert slice.read(2) == b'my'
    assert slice.read(1) == b' '
    assert slice.read(6) == b'dear'

    slice.seek(-99, os.SEEK_SET)
    #assert slice.tell() == 0 # TODO

def test_split():
    data = b'a;b'
    parts = [slice.read() for slice in binfile.split(binfile.fromBytes(data), b';')]
    assert parts == data.split(b';')

    data = b';'
    parts = [slice.read() for slice in binfile.split(binfile.fromBytes(data), b';')]
    assert parts == data.split(b';')

    data = b';;'
    parts = [slice.read() for slice in binfile.split(binfile.fromBytes(data), b';')]
    assert parts == data.split(b';')

    data = b'hello world, this.is.a test '
    parts = [slice.read() for slice in binfile.split(binfile.fromBytes(data), b" ")]
    assert parts == data.split(b' ')

    data = b'bananabread'
    parts = [slice.read() for slice in binfile.split(binfile.fromBytes(data), b'an')]
    assert parts == data.split(b'an')

def test_split_long_delimiter():
    # delimiter's longer than the file
    data = b'abc'
    parts = [slice.read() for slice in binfile.split(binfile.fromBytes(data), b'thisislongerthanbuff')]
    assert parts == [b'abc']

    data = b''
    parts = [slice.read() for slice in binfile.split(binfile.fromBytes(data), b';')]
    assert parts == [b'']

def test_splitAfter():
    data = b'hello\nworld\n'
    parts = [slice.read() for slice in binfile.splitAfter(binfile.fromBytes(data), b'\n')]
    assert parts == [b'hello\n', b'world\n'] # TODO I think the last item should be omitted for splitAfter() - 

#def test_splitBefore():
#    assert False, "todo"
