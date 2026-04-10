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

## Results

### Workload g21 — Graph Statistics (`read_graphs_results_v2.txt`)

Produced by running `read_graphs.py` against the two aggregated g21 edge files.

```
Graph, num nodes, undirected edges, directed edges, port-differentiated-directed edges
g21    318        1700              3028             11489
```

| Metric | Value |
|---|---|
| Nodes | 318 |
| Undirected edges | 1,700 |
| Directed edges | 3,028 |
| Port-differentiated directed edges | 11,489 |
| Nodes with undirected degree ≥ 2 | 107 |
| Median undirected degree | 1 |
| Max undirected degree | 112 |
| Unique service ports | 2,382 |
| Ports appearing on ≥ 2 edges | 1,407 |
| Nodes acting as provider (server) | 233 (70 offering ≥ 2 ports, median 1, max 694) |
| Nodes acting as client (consumer) | 149 (112 consuming ≥ 2 ports, median 2, max 1,161) |
| Nodes with both positive in- and out-degree | 64 |
| Self-arcs | 10 |
| Directed 2-cycles | 2,656 |

**Interpretation.** g21 is a moderately small workload (318 nodes) but exhibits rich port
diversity — 2,382 unique ports across only 1,700 edges. The high number of directed 2-cycles
(2,656 out of 3,028 directed edges) means most connections are bidirectional at the service
level. A small core of 64 nodes acts as both providers and consumers, while the majority of
nodes fill one role exclusively. The very high max client-port count (1,161 ports consumed by
one node) and max server-port count (694 ports offered by one node) suggest a few hub nodes
dominate service interaction.

---

### 20-Workload Dataset — Summary Table (`read_graphs_dir_20_full_output.txt`)

Produced by running `read_graphs.py` across all 27 snapshot files in `dir_20_graphs/`
(4 days of hourly data covering 20 de-identified workloads).

| Graph | Nodes | Undirected edges | Directed edges | Port-diff. directed edges |
|---|---:|---:|---:|---:|
| g4  | 278,739 | 302,034   | 302,108   | 302,595    |
| g2  | 157,489 | 1,864,574 | 2,158,346 | 12,377,439 |
| g15 |  70,172 | 113,082   | 145,369   | 158,807    |
| g5  |  46,298 |  56,047   |  56,773   |  68,140    |
| g6  |  28,329 | 106,667   | 117,865   | 380,640    |
| g10 |  18,414 |  37,702   |  38,675   | 148,184    |
| g9  |  13,717 |  26,651   |  30,398   |  83,179    |
| g3  |  11,555 |  43,996   |  50,447   | 173,499    |
| g13 |   5,290 |  20,889   |  27,383   | 100,932    |
| g8  |   3,389 |  14,081   |  14,227   |  42,611    |
| g12 |   2,454 |   4,505   |   5,223   |  67,948    |
| g20 |   1,487 |   2,214   |   2,287   |   2,717    |
| g1  |   1,447 | 106,617   | 118,691   | 1,926,968  |
| g17 |     596 |     997   |   1,058   |   1,475    |
| g14 |     575 |     880   |     944   |  26,687    |
| g7  |     290 |     732   |     763   |   1,080    |
| g18 |     289 |     501   |     505   |     918    |
| g16 |     238 |     314   |     324   |     465    |
| g11 |     207 |   1,557   |   1,587   |   1,781    |
| g19 |      86 |     150   |     155   |     325    |

#### Per-graph detailed statistics

<details>
<summary>Click to expand</summary>

**g4** — 278,739 nodes, 302,034 undirected edges  
Degree 2+: 20,361 nodes · median 1 · max 245,785  
Ports: 384 unique (57 on 2+ edges) · 885 providers (44 with 2+, max 292) · 277,923 clients (3,643 with 2+, max 322)  
Nodes with in- & out-degree: 69 · Self-arcs: 0 · Directed 2-cycles: 148

**g2** — 157,489 nodes, 1,864,574 undirected edges  
Degree 2+: 70,068 nodes · median 1 · max 26,235  
Ports: 103,907 unique (94,392 on 2+ edges) · 101,592 providers (30,010 with 2+, max 61,470) · 105,607 clients (54,994 with 2+, max 20,154)  
Nodes with in- & out-degree: 49,710 · Self-arcs: 0 · Directed 2-cycles: 587,544

**g15** — 70,172 nodes, 113,082 undirected edges  
Degree 2+: 41,016 nodes · median 2 · max 43,420  
Ports: 1,413 unique (1,311 on 2+ edges) · 23,729 providers (185 with 2+, max 1,324) · 68,059 clients (6,232 with 2+, max 1,224)  
Nodes with in- & out-degree: 21,616 · Self-arcs: 0 · Directed 2-cycles: 64,574

**g5** — 46,298 nodes, 56,047 undirected edges  
Degree 2+: 3,435 nodes · median 1 · max 34,868  
Ports: 4,912 unique (906 on 2+ edges) · 44,505 providers (733 with 2+, max 2,180) · 3,115 clients (1,413 with 2+, max 2,339)  
Nodes with in- & out-degree: 1,322 · Self-arcs: 5 · Directed 2-cycles: 1,452

**g6** — 28,329 nodes, 106,667 undirected edges  
Degree 2+: 17,319 nodes · median 2 · max 16,383  
Ports: 7,452 unique (1,619 on 2+ edges) · 19,972 providers (9,452 with 2+, max 452) · 21,383 clients (10,960 with 2+, max 5,812)  
Nodes with in- & out-degree: 13,026 · Self-arcs: 0 · Directed 2-cycles: 22,396

**g10** — 18,414 nodes, 37,702 undirected edges  
Degree 2+: 9,476 nodes · median 2 · max 9,032  
Ports: 6,329 unique (4,361 on 2+ edges) · 2,885 providers (1,328 with 2+, max 4,120) · 16,289 clients (1,708 with 2+, max 4,139)  
Nodes with in- & out-degree: 760 · Self-arcs: 0 · Directed 2-cycles: 1,946

**g9** — 13,717 nodes, 26,651 undirected edges  
Degree 2+: 3,089 nodes · median 1 · max 7,537  
Ports: 2,749 unique (2,029 on 2+ edges) · 5,438 providers (998 with 2+, max 146) · 9,480 clients (3,252 with 2+, max 854)  
Nodes with in- & out-degree: 1,201 · Self-arcs: 0 · Directed 2-cycles: 7,494

**g3** — 11,555 nodes, 43,996 undirected edges  
Degree 2+: 7,561 nodes · median 2 · max 7,825  
Ports: 14,754 unique (10,210 on 2+ edges) · 9,683 providers (3,057 with 2+, max 2,870) · 8,382 clients (4,708 with 2+, max 8,917)  
Nodes with in- & out-degree: 6,510 · Self-arcs: 3 · Directed 2-cycles: 12,902

**g13** — 5,290 nodes, 20,889 undirected edges  
Degree 2+: 3,997 nodes · median 3 · max 3,557  
Ports: 3,313 unique (769 on 2+ edges) · 3,202 providers (2,615 with 2+, max 90) · 4,784 clients (3,621 with 2+, max 863)  
Nodes with in- & out-degree: 2,696 · Self-arcs: 0 · Directed 2-cycles: 12,988

**g8** — 3,389 nodes, 14,081 undirected edges  
Degree 2+: 2,581 nodes · median 5 · max 2,465  
Ports: 449 unique (151 on 2+ edges) · 565 providers (139 with 2+, max 122) · 3,029 clients (2,325 with 2+, max 97)  
Nodes with in- & out-degree: 205 · Self-arcs: 0 · Directed 2-cycles: 292

**g12** — 2,454 nodes, 4,505 undirected edges  
Degree 2+: 986 nodes · median 1 · max 733  
Ports: 16,969 unique (15,768 on 2+ edges) · 1,614 providers (499 with 2+, max 11,866) · 1,526 clients (629 with 2+, max 15,036)  
Nodes with in- & out-degree: 686 · Self-arcs: 2 · Directed 2-cycles: 1,436

**g20** — 1,487 nodes, 2,214 undirected edges  
Degree 2+: 242 nodes · median 1 · max 1,199  
Ports: 99 unique (62 on 2+ edges) · 1,336 providers (58 with 2+, max 19) · 207 clients (167 with 2+, max 27)  
Nodes with in- & out-degree: 56 · Self-arcs: 0 · Directed 2-cycles: 146

**g1** — 1,447 nodes, 106,617 undirected edges  
Degree 2+: 1,087 nodes · median 19 · max 599  
Ports: 16,409 unique (15,039 on 2+ edges) · 1,041 providers (745 with 2+, max 1,202) · 946 clients (745 with 2+, max 9,854)  
Nodes with in- & out-degree: 540 · Self-arcs: 0 · Directed 2-cycles: 24,148

**g17** — 596 nodes, 997 undirected edges  
Degree 2+: 275 nodes · median 1 · max 284  
Ports: 116 unique (55 on 2+ edges) · 161 providers (50 with 2+, max 64) · 499 clients (166 with 2+, max 56)  
Nodes with in- & out-degree: 64 · Self-arcs: 0 · Directed 2-cycles: 122

**g14** — 575 nodes, 880 undirected edges  
Degree 2+: 217 nodes · median 1 · max 67  
Ports: 24,896 unique (905 on 2+ edges) · 198 providers (55 with 2+, max 23,246) · 468 clients (125 with 2+, max 23,246)  
Nodes with in- & out-degree: 91 · Self-arcs: 0 · Directed 2-cycles: 128

**g7** — 290 nodes, 732 undirected edges  
Degree 2+: 213 nodes · median 3 · max 111  
Ports: 156 unique (33 on 2+ edges) · 246 providers (118 with 2+, max 34) · 60 clients (24 with 2+, max 116)  
Nodes with in- & out-degree: 16 · Self-arcs: 0 · Directed 2-cycles: 62

**g18** — 289 nodes, 501 undirected edges  
Degree 2+: 216 nodes · median 2 · max 216  
Ports: 154 unique (28 on 2+ edges) · 58 providers (16 with 2+, max 118) · 239 clients (207 with 2+, max 116)  
Nodes with in- & out-degree: 8 · Self-arcs: 0 · Directed 2-cycles: 8

**g16** — 238 nodes, 314 undirected edges  
Degree 2+: 65 nodes · median 1 · max 116  
Ports: 63 unique (44 on 2+ edges) · 110 providers (28 with 2+, max 27) · 140 clients (71 with 2+, max 23)  
Nodes with in- & out-degree: 12 · Self-arcs: 0 · Directed 2-cycles: 20

**g11** — 207 nodes, 1,557 undirected edges  
Degree 2+: 202 nodes · median 7 · max 98  
Ports: 68 unique (38 on 2+ edges) · 154 providers (34 with 2+, max 14) · 93 clients (68 with 2+, max 23)  
Nodes with in- & out-degree: 40 · Self-arcs: 0 · Directed 2-cycles: 60

**g19** — 86 nodes, 150 undirected edges  
Degree 2+: 39 nodes · median 1 · max 51  
Ports: 34 unique (25 on 2+ edges) · 72 providers (19 with 2+, max 12) · 21 clients (8 with 2+, max 23)  
Nodes with in- & out-degree: 7 · Self-arcs: 0 · Directed 2-cycles: 10

</details>

**Interpretation.** The 20 workloads span nearly four orders of magnitude in scale (86 to
278,739 nodes). Key observations:

- **Highly skewed degree distributions.** Every workload has a median undirected degree of 1 or 2
  yet maximum degrees in the hundreds to hundreds-of-thousands, consistent with a hub-and-spoke
  or power-law topology common in enterprise networks.
- **g4 vs g2** illustrate two extremes: g4 is the largest by node count (~279 K) but has very
  few edges per node (302 K edges, one dominant hub with degree 245,785 — a likely gateway or
  DNS server). g2 has fewer nodes (~157 K) but nearly six times as many edges (1.86 M undirected)
  with 587 K directed 2-cycles, indicating dense peer-to-peer or east-west traffic.
- **Port diversity is not correlated with size.** g14 (575 nodes) has 24,896 unique ports — far
  more than g4 (384 ports with 278 K nodes) — suggesting workloads with many ephemeral or
  dynamic-range ports. g1 (1,447 nodes) has 1.93 M port-differentiated edges, implying a small
  but extremely port-heavy workload.
- **Bidirectional communication (2-cycles).** Ranges from near-zero in g4 (148 2-cycles out of
  302 K directed edges, ~0.05 %) to >27 % in g2 and g13, reflecting very different communication
  patterns between workloads.
- **Self-arcs** appear in g5 (5), g3 (3), g12 (2) and g21 (10), representing nodes that
  communicate with themselves — possibly localhost/loopback traffic captured in the sensor data.

---

### Workload g21 — Ground-Truth Groupings (`read_gt.py`)

#### `groupings.gt.txt` (primary ground truth)

```
# num gt sets=23  size(node_to_gt)=59
# gt sizes histo: Counter({2: 8, 3: 8, 1: 4, 4: 2, 7: 1})
# group sizes descending: [7, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1]
```

| Metric | Value |
|---|---|
| Number of ground-truth groups | 23 |
| Nodes covered by any group | 59 (out of 318 total) |
| Most common group sizes | 2 (×8) and 3 (×8) |
| Largest group | 7 nodes |

#### `groupings.gt.viaPrefix5.txt` (alternative prefix-derived grouping)

```
# num gt sets=18  size(node_to_gt)=52
# gt sizes histo: Counter({3: 8, 1: 3, 2: 3, 4: 2, 5: 1, 6: 1})
# group sizes descending: [6, 5, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1]
```

| Metric | Value |
|---|---|
| Number of groups | 18 |
| Nodes covered | 52 |
| Most common group size | 3 (×8) |
| Largest group | 6 nodes |

**Interpretation.** Only 59 of the 318 nodes in g21 carry a ground-truth workload label, which
is typical of lightly annotated enterprise datasets. The majority of labelled nodes belong to
small groups of 2–3 (16 out of 23 groups), with one larger cluster of 7 nodes. The
prefix-derived alternative grouping (`viaPrefix5`) is slightly more compact (18 groups, 52
nodes), collapsing some pairs into triples by matching on IP-prefix codes, and can serve as a
weaker but automatically generated baseline for evaluation.

---

## Requirements

- Python 3.6+
- [NumPy](https://numpy.org/) (`pip install numpy`)

All other dependencies (`gzip`, `hashlib`, `collections`, `argparse`) are part of the
Python standard library.

