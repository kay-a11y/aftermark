#!/usr/bin/env bash

# Usage: bash bit_planes.sh /path/to/image [outdir]
set -e

in="$1"
if [ -z "$in" ]; then
    echo "Usage: $0 /path/to/image [output_dir]"
    exit 1
fi

# Use 2nd arg as output dir, or default
outdir="${2:-$(dirname "$0")/../artifacts/lsb}"

mkdir -p "$outdir"

channels=(R G B)
for c in {0..2}; do
  for b in {0..7}; do
    convert "$in" -channel ${channels[$c]} -separate +channel  \
      -fx "(((u*255)>>$b)&1)*255"                              \
      "$outdir/$(basename "${in%.*}")_${channels[$c]}_bit${b}.png"
  done
done

echo "Bit-plane images saved in $outdir"
