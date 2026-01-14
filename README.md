# Cisco Secure Networks Analysis

## Overview
This repository contains tools for analyzing Cisco network data, including graph analysis and ground truth processing.

## Data Directories
The main data directory is `dir_g21_small_workload_with_gt`, which contains:
- `dir_no_packets_etc/` - Edge files without packet nodes
- `dir_includes_packets_and_other_nodes/` - Edge files with packet nodes
- `groupings.gt.txt` - Ground truth groupings
- `groupings.gt.viaPrefix5.txt` - Alternative ground truth groupings
- `prefix_codes.txt` - Prefix code mappings

## Using Path Utilities in Jupyter Notebooks

To reliably access the data directory from Jupyter notebooks (or any Python script), use the `path_utils` module:

```python
# Import the path utility functions
from path_utils import get_g21_small_workload_path, get_g21_subdirectory, get_g21_file_path

# Get the path to the main data directory
data_dir = get_g21_small_workload_path()
print(f"Data directory: {data_dir}")

# Get path to a specific subdirectory
no_packets_dir = get_g21_subdirectory('dir_no_packets_etc')
print(f"No packets directory: {no_packets_dir}")

# Get path to a specific file
gt_file = get_g21_file_path('groupings.gt.txt')
print(f"Ground truth file: {gt_file}")
```

These functions work regardless of where your notebook or script is located in the filesystem.

## Example Scripts

### Reading Ground Truth
```bash
python read_gt.py dir_g21_small_workload_with_gt/groupings.gt.txt
```

Or in a notebook:
```python
from path_utils import get_g21_file_path
import read_gt

gt_file = get_g21_file_path('groupings.gt.txt')
node_gt, gt_nodes = read_gt.read_gt(gt_file)
```

### Reading Graphs
```bash
python read_graphs.py dir_g21_small_workload_with_gt/dir_no_packets_etc/
```

Or in a notebook:
```python
from path_utils import get_g21_subdirectory
import read_graphs

data_dir = get_g21_subdirectory('dir_no_packets_etc')
graphs, stats, longevity = read_graphs.read_edges_with_ports_to_stats_multiple_files(data_dir)
```
