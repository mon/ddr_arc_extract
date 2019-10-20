#!/usr/bin/env python3

import sys
import os
import errno
from struct import pack, unpack, calcsize

import glob

from tqdm import tqdm

from lz77 import decompress

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def unpack_f(fmt, f):
    size = calcsize(fmt)
    blob = f.read(size)
    return unpack(fmt, blob)

def grab_string(f):
    res = b''
    tmp = f.read(1)
    while tmp != b'\x00':
        res += tmp
        tmp = f.read(1)
    return res.decode('utf8')

def extract(path, out = None):
    if out is None:
        out = path.replace('.','_')
        if out == path:
            out += '_arc'

    with open(path, 'rb') as f:
        _magic, _version_maybe, filecount, _compression_maybe = \
            unpack_f('IIII', f)

        files = []
        for _ in range(filecount):
            str_offset, file_offset, unpacked_size, packed_size = \
                unpack_f('IIII', f)
            files.append([str_offset, file_offset, unpacked_size, packed_size])
        for entry in files:
            f.seek(entry[0])
            entry[0] = grab_string(f)

        for name, file_offset, unpacked_size, packed_size in tqdm(files):
            tqdm.write(name)
            file = os.path.join(out, name)
            folder = os.path.dirname(file)
            mkdir_p(folder)
            with open(file, 'wb') as f_out:
                f.seek(file_offset)
                data = f.read(packed_size)
                if unpacked_size != packed_size:
                    data = decompress(data)
                if len(data) != unpacked_size:
                    tqdm.write('{} : {:08X}'.format(name, file_offset))
                    tqdm.write('MISMATCH: {0} ({0:02x}) {1} ({1:02x})'.format(len(data),unpacked_size))
                f_out.write(data)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('arc_extract file.arc [file2.arc]')
        exit(1)

    for f in sys.argv[1:]:
        extract(f)
