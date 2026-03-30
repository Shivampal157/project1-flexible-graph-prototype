# Flexible Graph Construction Prototype Report

| scenario | strategy | nodes | edges | isolated | weak_components | out_deg_p95 | runtime (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular_grid_32x32 | knn | 1024 | 8192 | 0 | 1 | 8.00 | 0.0493 |
| regular_grid_32x32 | radius | 1024 | 19092 | 0 | 1 | 20.00 | 0.0968 |
| regular_grid_32x32 | hybrid | 1024 | 11652 | 0 | 1 | 12.00 | 0.0695 |
| jittered_grid_32x32 | knn | 1024 | 8192 | 0 | 1 | 8.00 | 0.0413 |
| jittered_grid_32x32 | radius | 1024 | 17714 | 0 | 1 | 21.00 | 0.1135 |
| jittered_grid_32x32 | hybrid | 1024 | 13504 | 0 | 1 | 17.00 | 0.0800 |
| sparse_clusters | knn | 320 | 2560 | 0 | 7 | 8.00 | 0.0168 |
| sparse_clusters | radius | 320 | 7334 | 0 | 7 | 23.00 | 0.0699 |
| sparse_clusters | hybrid | 320 | 7270 | 0 | 1 | 23.00 | 0.0781 |

## Key observations

- jittered_grid_32x32: best connectivity is `knn` (isolated=0, weak_components=1, runtime=0.041s). Denser graphs (max edges) come from `radius` (n_edges=17714); radius has n_edges=17714.
- regular_grid_32x32: best connectivity is `knn` (isolated=0, weak_components=1, runtime=0.049s). Denser graphs (max edges) come from `radius` (n_edges=19092); radius has n_edges=19092.
- sparse_clusters: best connectivity is `hybrid` (isolated=0, weak_components=1, runtime=0.078s). Denser graphs (max edges) come from `radius` (n_edges=7334); radius has n_edges=7334.
- Overall: `knn` is the fastest strategy on average runtime across scenarios.
