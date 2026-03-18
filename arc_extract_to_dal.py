#!/usr/bin/env python3

import sys
import arc_extract as e

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('arc_extract file.arc [file2.arc]')
        exit(1)

    for f in sys.argv[1:]:
        e.extract(f, out_root='dal')