#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import getsizeof

sumoHeader = "S"
noCompression = "0"
withGzipCompression = "1"

class SumoError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def toGzip (x):
  import StringIO
  import gzip
  out = StringIO.StringIO()
  with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(x)
  return out.getvalue()

def fromGzip (x):
  import zlib
  unzipped = zlib.decompress(x, 16+zlib.MAX_WBITS)
  return unzipped

def verifySumoHeader(s):
  sHeader = s[:2]
  if sHeader == (sumoHeader + noCompression):
    return True
  elif sHeader == (sumoHeader + withGzipCompression):
    return True
  else:
    return False

def removeSumoHeader(s):
  out = s[2:]
  return out

def toPuny (x):
  x = x.encode('punycode')
  return x

def fromPuny (x):
  x = x.decode('punycode')
  return x

def toHex (x):
  x = x.encode('hex')
  return x

def fromHex (x):
  x = x.decode('hex')
  return x

def noCompress (x):
  d = sumoHeader + noCompression + x
  o = toHex (toPuny(d))
  return o

def compressGzip (x):
  d = sumoHeader + withGzipCompression + x
  o = toHex (toGzip (toPuny(d)))
  return o

def toSumo (x):
  uncompressedX = noCompress (x)
  compressedX   = compressGzip (x)
  if ( (getsizeof(compressedX)) < (getsizeof(uncompressedX)) ):
    return compressedX
  else:
    return uncompressedX

def fromHexToText (x):
  r = fromPuny(fromHex(x))
  return r
  
def fromGzipHexToText (x):
  r = fromPuny (fromGzip (fromHex(x)))
  return r

def fromSumo (x):
  output = ""
  try:
    output = fromHexToText(x)
  except:
      try:
        output = fromGzipHexToText(x)
      except:
        raise SumoError("Error decoding SUMO input")
  # verify sumo header
  isVerified = verifySumoHeader (output)
  if isVerified:
    return (removeSumoHeader (output))
  else:
    raise SumoError("Invalid Sumo Header")

print "Example of a short (uncompressable) string:"

# This input data should not be compressed after encoding to sumo.
d = u"こんにちは"

# Encode our 'd' utf8 data to sumo encoding
# output should be: 53302d71383361376236627a613377
e = toSumo (d)
print "Data encoded with SUMO:"
print e

# Decode our sumo encoded data back to utf8
print "Data decoded from SUMO:"
x = fromSumo(e)
print x  

print ""
  
print "Example of a long (compressable) string"

# This input data should be compressed after encoding to sumo.
d = u"こんにちはこんにちはこんにちはこんにちはこんにちはこんにちはこんにちはこんにちはこんにちは"

# Encode our 'd' utf8 data to sumo encoding
# depending on your compression settings, data might be: 1f8b08004d58675c02ff0b36d42db4304e840193bc2428302f4c8602c38c142830b6c84e4d4c850000c2e5d1ad39000000
e = toSumo (d)
print "Data encoded with SUMO:"
print e

# Decode our sumo encoded data back to utf8
x = fromSumo(e)
print "Data decoded from SUMO:"
print x
