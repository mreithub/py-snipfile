py-snipfile
===========

this python package provides some useful tools edit binary files, e.g.:

- `File(fileobjOrPath)`: simple wrapper around python file-like objects
- `Slice(fileobj, *, offset=0, size=None)`: a class that restricts access to a subset of the given fileobj

all our file-like classes implement the same FileIntf interface

- `split(f:FileIntf, separator:bytes)`: splits a file into Slices, at the given delimiter, omitting the separator
  - e.g. `split(fromBytes(b'hello\nworld\n'), b'\n')` results in three slices: `[Slice(0,5)='hello', Slice(6,5)='world, Slice(12,0)='']`
- `splitAfter(f:FileIntf, separator:bytes)`: same as split(), but keeps the separator as part of the slice preceeding it
  - the above example would then yield: `[Slice(0,6) = 'hello\n', Slice(6,6) = 'world\n'`
- `splitBefore(f:FileIntf, separator:bytes)`: same as split(), but cuts *before* the separator:
  - the above example yields: `[Slice(0,5)='hello', Slice(5,6)='\nworld', Slice(11,1)='\n']`
- `cutAt(f:FileIntf, *positions:int)`: cuts a file at the specified position(s), returning a list of Slices 
