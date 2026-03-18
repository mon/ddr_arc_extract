#!/usr/bin/env python3

import sys
import os
from struct import pack

from tqdm import tqdm

from lz77 import compress

def get_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath.replace(os.sep, '/'))
    return file_paths

def create(files, output, store_only=False):
    file_count = len(files)

    with open(output, 'wb') as f_out:
        f_out.write(b'\x20\x11\x75\x19')
        f_out.write(pack('<III', 1, file_count, 2))

        name_offset = 0x10 + (file_count * 0x10)
        file_offset = name_offset + sum([len(x) for x in files]) + file_count
        initial_pad = -file_offset % 64
        file_offset += initial_pad

        all_files_content = bytearray(b'')

        for file in tqdm(files):
            tqdm.write(file)

            with open (file, 'rb') as f:
                uncompressed = f.read()
                uncompressed_size = len(uncompressed)
                if store_only:
                    compressed = uncompressed
                    compressed_size = uncompressed_size
                else:
                    compressed = compress(uncompressed)
                    compressed_size = len(compressed)
                all_files_content.extend(compressed)
                pad = -len(compressed) % 64
                all_files_content.extend(b'\x00' * pad)

            f_out.write(pack('<IIII', name_offset, file_offset, uncompressed_size, compressed_size))

            name_offset += len(file) + 1
            file_offset += compressed_size + pad

        for file in files:
            f_out.write(file.encode('utf-8') + b'\x00')
        f_out.write(b'\x00' * initial_pad)
        f_out.write(all_files_content)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('arc_create input_folder_arc output_file.arc')
        exit(1)

    create(get_filepaths(sys.argv[1]), sys.argv[2])
    # create(get_filepaths(sys.argv[1]), sys.argv[2], store_only=True)
