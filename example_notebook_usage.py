#!/usr/bin/env python3
"""
Example demonstrating how to use path_utils in a Jupyter notebook.

This file shows the recommended way to access the dir_g21_small_workload_with_gt
directory and its contents from a Jupyter notebook or any Python script.

Copy the code snippets below into your Jupyter notebook cells.
"""

import os

# Cell 1: Import the path utilities
print("=" * 60)
print("Example 1: Importing path utilities")
print("=" * 60)

from path_utils import (
    get_g21_small_workload_path,
    get_g21_subdirectory,
    get_g21_file_path
)

# Cell 2: Get the main data directory
print("\n" + "=" * 60)
print("Example 2: Get the main data directory")
print("=" * 60)

data_dir = get_g21_small_workload_path()
print(f"Data directory path: {data_dir}")
print(f"Directory exists: {os.path.exists(data_dir)}")

# Cell 3: List contents of the data directory
print("\n" + "=" * 60)
print("Example 3: List contents of the data directory")
print("=" * 60)

contents = os.listdir(data_dir)
print(f"Contents of {os.path.basename(data_dir)}:")
for item in sorted(contents):
    item_path = os.path.join(data_dir, item)
    item_type = "DIR " if os.path.isdir(item_path) else "FILE"
    print(f"  [{item_type}] {item}")

# Cell 4: Get path to a subdirectory
print("\n" + "=" * 60)
print("Example 4: Get path to a subdirectory")
print("=" * 60)

no_packets_dir = get_g21_subdirectory('dir_no_packets_etc')
print(f"Subdirectory path: {no_packets_dir}")

# List edge files in the subdirectory
edge_files = [f for f in os.listdir(no_packets_dir) if f.endswith('.gz')]
print(f"\nFound {len(edge_files)} edge files:")
for i, fname in enumerate(sorted(edge_files)[:5], 1):
    print(f"  {i}. {fname}")
if len(edge_files) > 5:
    print(f"  ... and {len(edge_files) - 5} more")

# Cell 5: Get path to a specific file
print("\n" + "=" * 60)
print("Example 5: Get path to a specific file")
print("=" * 60)

gt_file = get_g21_file_path('groupings.gt.txt')
print(f"Ground truth file path: {gt_file}")

# Read a few lines from the file
with open(gt_file, 'r') as f:
    lines = [line.strip() for line in f.readlines()[:5]]
    print(f"\nFirst 5 lines of {os.path.basename(gt_file)}:")
    for i, line in enumerate(lines, 1):
        print(f"  {i}. {line}")

# Cell 6: Use with existing analysis functions
print("\n" + "=" * 60)
print("Example 6: Use with existing analysis functions")
print("=" * 60)

# Example: Reading ground truth data
try:
    from read_gt import read_gt
    
    gt_file_path = get_g21_file_path('groupings.gt.txt')
    node_gt, gt_nodes = read_gt(gt_file_path)
    print("Successfully loaded ground truth data!")
    print(f"Number of ground truth groups: {len(gt_nodes)}")
    print(f"Number of nodes with ground truth: {len(node_gt)}")
except Exception as e:
    print(f"Note: read_gt module not available or error occurred: {e}")

# Cell 7: Summary
print("\n" + "=" * 60)
print("Summary: Key Functions")
print("=" * 60)

summary = """
Key functions in path_utils:

1. get_g21_small_workload_path()
   - Returns the absolute path to dir_g21_small_workload_with_gt
   - Works from any working directory

2. get_g21_subdirectory(subdir_name)
   - Returns the absolute path to a subdirectory
   - Example: get_g21_subdirectory('dir_no_packets_etc')

3. get_g21_file_path(filename)
   - Returns the absolute path to a file in the data directory
   - Example: get_g21_file_path('groupings.gt.txt')

All functions return absolute paths, so they work reliably regardless
of where your Jupyter notebook or Python script is located!
"""

print(summary)

print("\n" + "=" * 60)
print("All examples completed successfully!")
print("=" * 60)
