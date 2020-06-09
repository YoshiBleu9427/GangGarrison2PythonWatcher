import struct


def read_byte(s):
    rdata = s.recv(1)
    res = struct.unpack("<b", rdata)[0]
    print("   util read byte", res)
    return res

def read_ubyte(s):
    rdata = s.recv(1)
    res = struct.unpack("<B", rdata)[0]
    print("   util read ubyte", res)
    return res

def read_short(s):
    rdata = s.recv(2)
    res = struct.unpack("h", rdata)[0]
    print("   util read short", res)
    return res

def read_ushort(s):
    rdata = s.recv(2)
    res = struct.unpack("H", rdata)[0]
    print("   util read ushort", res)
    return res

def read_int(s):
    rdata = s.recv(4)
    res = struct.unpack("i", rdata)[0]
    print("   util read int", res)
    return res

def read_uint(s):
    rdata = s.recv(4)
    res = struct.unpack("I", rdata)[0]
    print("   util read uint", res)
    return res

def read_float(s):
    rdata = s.recv(4)
    res = struct.unpack("f", rdata)[0]
    print("   util read float", res)
    return res

def read_double(s):
    rdata = s.recv(8)
    res = struct.unpack("d", rdata)[0]
    return res
    
def receivestring(s, strlenbytes):
    try:
        if (strlenbytes == 1):
            strlen = read_ubyte(s)
        if (strlenbytes == 2):
            strlen = read_ushort(s)
        rdata = s.recv(strlen)
        print("   util read string", rdata.decode("utf-8"))
        return rdata.decode("utf-8")
    except struct.error as e:
        return ""