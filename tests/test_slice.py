import io

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
    assert parts == [b'abc']

    buff = io.BytesIO(b'')
    parts = [slice.read() for slice in binfile.split(binfile.File(buff), b';')]
    assert parts == [b'']

def test_splitAfter():
    buff = io.BytesIO(b'hello\nworld\n')
    parts = [slice.read() for slice in binfile.splitAfter(binfile.File(buff), b'\n')]
    assert parts == [b'hello\n', b'world\n'] # TODO I think the last item should be omitted for splitAfter() - 

#def test_splitBefore():
#    assert False, "todo"