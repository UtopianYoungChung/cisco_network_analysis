# Cisco Secure Networks Analysis

Tools for analysing de-identified Cisco network-traffic edge data. The repository
includes scripts to ingest hourly edge snapshots, compute graph statistics (node/edge
counts, degree distributions, service-port usage, edge longevity), and read ground-truth
workload-grouping files for evaluation.

---

## Repository Structure

```
.
├── read_graphs.py                         # Main analysis script – reads edge files and reports graph statistics
├── read_gt.py                             # Reads ground-truth grouping files and reports statistics
├── aggregate_g21_edges.py                 # Aggregates many small edge files into one gzipped file
├── test_sample.py                         # Minimal placeholder test
│
├── dir_20_graphs/                         # 20 de-identified workload graphs, organised by day
│   ├── dir_day1/   (out1_*.txt.gz …)
│   ├── dir_day2/
│   ├── dir_day3/
│   └── dir_day4/
│
├── dir_g21_small_workload_with_gt/        # Workload g21 with ground-truth groupings
│   ├── dir_includes_packets_and_other_nodes/   # Hourly edge snapshots (anon.txt.gz)
│   ├── dir_no_packets_etc/                     # Aggregated multi-hour / multi-day edge files
│   ├── groupings.gt.txt                        # Ground-truth workload groupings
│   ├── groupings.gt.viaPrefix5.txt             # Alternative groupings derived via IP prefix matching
│   └── prefix_codes.txt                        # Encoded node prefix codes
│
├── dir_g21_all_edges_aggregated.txt.gz    # Aggregated edge file for g21 (v1)
├── dir_g21_all_edges_aggregated_v2.txt.gz # Aggregated edge file for g21 (v2, with manifest)
├── aggregate_manifest_v2.json             # Manifest produced by aggregate_g21_edges.py (v2 run)
│
├── read_graphs_results.txt                # Sample output of read_graphs.py on g21 aggregated data
├── read_graphs_results_v2.txt             # Updated output of read_graphs.py
└── read_graphs_dir_20_full_output.txt     # Output of read_graphs.py on dir_20_graphs
```

---

## Data Format

### Edge files (`.txt.gz` / `.gz`)

Gzip-compressed text files. Each non-comment line is whitespace-separated:

```
<workload_id>  <node1>  <node2>  <port_csv>
```

| Field | Description |
|---|---|
| `workload_id` | Graph/workload identifier, e.g. `g21` |
| `node1` | Source node (consumer / client) – de-identified |
| `node2` | Destination node (provider / server) – de-identified |
| `port_csv` | Comma-separated port tuples, e.g. `p443-3,p80-1`. Each tuple starts with `p<port>`. |

Lines beginning with `#` are comments and are skipped.

### Ground-truth files (`.gt.txt`)

Plain-text files where each line is a comma-separated list of node IDs that belong to
the same logical workload group:

```
node_a,node_b,node_c
node_d,node_e
```

---

## Scripts

### `read_graphs.py` – Graph Statistics

Reads one or more edge files from a directory and reports:

- Number of nodes, undirected edges, directed edges, and port-differentiated directed edges per workload.
- Degree distribution (median / max undirected degree).
- Service-port statistics (unique ports, nodes providing / consuming ports).
- Edge longevity (how many snapshot files each directed edge appears in).

**Usage**

```bash
# Read 2 edge files from dir_20_graphs
python read_graphs.py dir_20_graphs 2

# Read all edge files in a directory
python read_graphs.py dir_20_graphs

# Read from a specific sub-directory
python read_graphs.py dir_g21_small_workload_with_gt/dir_no_packets_etc/
```

Results are written to `read_graphs_results.txt` in the working directory.

**Example output**

```
Graph, num nodes, undirected edges, directed edges, port-differentiated-directed edges
g21 318 1700 3028 11489

Graph=g21 num nodes=318, num undirected edges=1700
(undirected) num nodes with degree 2+=107, median degree=1, max degree=112
Num. of (unique service) ports in graph =2382, on 2+ edges=1407
Num. nodes providing a port=233, 2+ ports=70 median=1 max=694
Num. nodes client of a port=149, 2+ ports=112 median=2 max=1161
Num. nodes with positive indegree and outdegree = 64
Num. of self-arcs: 10
Num. directed edges: 3028
Num. of directed 2-cycles: 2656
```

---

### `read_gt.py` – Ground-Truth Statistics

Reads a ground-truth grouping file and prints the number of groups, group-size histogram,
and a descending list of group sizes.

**Usage**

```bash
python read_gt.py dir_g21_small_workload_with_gt/groupings.gt.txt
```

**Example output**

```
# num gt sets=23  size(node_to_gt)=59
# gt sizes histo: Counter({2: 8, 3: 8, 1: 4, 4: 2, 7: 1})
# group sizes descending: [7, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1]
```

---

### `aggregate_g21_edges.py` – Edge File Aggregation

Recursively walks a directory, finds all `.gz` / `.txt` / `.txt.gz` edge files, and
concatenates their decompressed content into a single output gzip file. Optionally
writes a JSON manifest with per-file SHA-256 checksums.

**Usage**

```bash
python aggregate_g21_edges.py <input_dir> <output_gz> [--manifest FILE] [--compresslevel N] [--dry-run]
```

| Argument | Description |
|---|---|
| `input_dir` | Root directory to search for edge files |
| `output_gz` | Path for the aggregated gzip output file |
| `--manifest` | Path for the JSON manifest (default: `aggregate_manifest.json`) |
| `--compresslevel` | Gzip compression level 1–9 (default: `6`) |
| `--dry-run` | Scan and report files without writing output |

**Example**

```bash
python aggregate_g21_edges.py dir_g21_small_workload_with_gt \
    dir_g21_all_edges_aggregated_v2.txt.gz \
    --manifest aggregate_manifest_v2.json
```

---

## Requirements

- Python 3.6+
- [NumPy](https://numpy.org/) (`pip install numpy`)

All other dependencies (`gzip`, `hashlib`, `collections`, `argparse`) are part of the
Python standard library.

