#!/bin/bash
socat /dev/science,raw,echo=0 \
SYSTEM:'tee ~/sci_in.txt |socat - "PTY,link=/tmp/sciClone,raw,echo=0,waitslave" |tee ~/sci_out.txt'
