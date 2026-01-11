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

#!/usr/bin/env python3
"""
Aggregate edge files into one gzipped file with manifest and checksums.
"""
import argparse
import gzip
import hashlib
import json
import os
import sys
from datetime import datetime


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def open_input(path):
    if path.endswith('.gz'):
        return gzip.open(path, 'rb')
    return open(path, 'rb')


def aggregate(input_dir, output_gz, manifest_path=None, compresslevel=9, dry_run=False):
    candidates = []
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.endswith('.gz') or f.endswith('.txt') or f.endswith('.txt.gz'):
                candidates.append(os.path.join(root, f))

    candidates.sort()
    if len(candidates) == 0:
        print('No candidate files found under', input_dir)
        return 1

    print(f'Found {len(candidates)} files to aggregate.')
    for i, p in enumerate(candidates, start=1):
        if i <= 10 or i % 50 == 0:
            print(f'  [{i}/{len(candidates)}] {p}')
        elif i == 11:
            print('  ...')

    manifest = {
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'input_dir': input_dir,
        'output': output_gz,
        'files': []
    }

    if dry_run:
        print('Dry-run mode; not writing output')
        for p in candidates:
            try:
                sz = os.path.getsize(p)
            except Exception:
                sz = None
            manifest['files'].append({'path': p, 'size': sz})
        if manifest_path:
            with open(manifest_path, 'w') as mf:
                json.dump(manifest, mf, indent=2)
        return 0

    tmp_out = output_gz + '.tmp'
    total_uncompressed = 0
    files_processed = 0
    per_file_info = []

    with gzip.open(tmp_out, 'wb', compresslevel=compresslevel) as outf:
        for path in candidates:
            try:
                # compute input checksum on raw file
                try:
                    in_sz = os.path.getsize(path)
                except Exception:
                    in_sz = None
                sha = None
                try:
                    sha = sha256_of_file(path)
                except Exception:
                    sha = None

                with open_input(path) as inf:
                    while True:
                        chunk = inf.read(1 << 20)
                        if not chunk:
                            break
                        outf.write(chunk)
                        total_uncompressed += len(chunk)

                files_processed += 1
                per_file_info.append({'path': path, 'size': in_sz, 'sha256': sha})
            except Exception as e:
                print('Warning: failed to read', path, '->', e)

    # atomically move
    try:
        os.replace(tmp_out, output_gz)
    except Exception:
        os.rename(tmp_out, output_gz)

    try:
        compressed_size = os.path.getsize(output_gz)
    except Exception:
        compressed_size = None

    manifest.update({
        'files_processed': files_processed,
        'total_uncompressed_bytes': total_uncompressed,
        'compressed_size_bytes': compressed_size,
        'per_file': per_file_info,
    })

    if manifest_path:
        with open(manifest_path, 'w', encoding='utf-8') as mf:
            json.dump(manifest, mf, indent=2)

    print('Wrote aggregated gz to', output_gz)
    print('Total uncompressed bytes written:', total_uncompressed)
    print('Compressed output size (bytes):', compressed_size)
    if manifest_path:
        print('Wrote manifest to', manifest_path)
    return 0


def main():
    parser = argparse.ArgumentParser(description='Aggregate edge files into one gz')
    parser.add_argument('input_dir')
    parser.add_argument('output_gz')
    parser.add_argument('--manifest', default='aggregate_manifest.json')
    parser.add_argument('--compresslevel', type=int, default=6)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    return aggregate(args.input_dir, args.output_gz, manifest_path=args.manifest,
                     compresslevel=args.compresslevel, dry_run=args.dry_run)


if __name__ == '__main__':
    sys.exit(main())
