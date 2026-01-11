#!/usr/bin/env python3
"""
Aggregate all edge files under dir_g21_small_workload_with_gt into one gzipped file.
Usage: python aggregate_g21_edges.py <input_dir> <output_gz>
"""
import os, sys, gzip

if len(sys.argv) < 3:
    print("Usage: python aggregate_g21_edges.py <input_dir> <output_gz>")
    sys.exit(1)

input_dir = sys.argv[1]
output_gz = sys.argv[2]

candidates = []
for root, dirs, files in os.walk(input_dir):
    for f in files:
        if f.endswith('.gz') or f.endswith('.txt') or f.endswith('.txt.gz'):
            candidates.append(os.path.join(root, f))

candidates.sort()
if len(candidates) == 0:
    print('No candidate files found under', input_dir)
    sys.exit(1)

print(f'Found {len(candidates)} files to aggregate.')

# log each candidate and provide progress updates
for i, p in enumerate(candidates, start=1):
    if i <= 10 or i % 50 == 0:
        print(f'  [{i}/{len(candidates)}] {p}')
    elif i == 11:
        print('  ...')

with gzip.open(output_gz, 'wb') as outf:
    total_in = 0
    for path in candidates:
        try:
            if path.endswith('.gz'):
                with gzip.open(path, 'rb') as inf:
                    while True:
                        chunk = inf.read(1 << 20)
                        if not chunk:
                            break
                        outf.write(chunk)
                        total_in += len(chunk)
            else:
                with open(path, 'rb') as inf:
                    while True:
                        chunk = inf.read(1 << 20)
                        if not chunk:
                            break
                        outf.write(chunk)
                        total_in += len(chunk)
        except Exception as e:
            print('Warning: failed to read', path, '->', e)

print('Wrote aggregated gz to', output_gz)
print('Total uncompressed bytes written:', total_in)

# report compressed size
try:
    cs = os.path.getsize(output_gz)
    print('Compressed output size (bytes):', cs)
except Exception:
    pass
