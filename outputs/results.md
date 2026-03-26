# Flexible Graph Construction Prototype Report

| scenario | strategy | nodes | edges | isolated | weak_components | out_deg_p95 | runtime (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular_grid_32x32 | knn | 1024 | 8192 | 0 | 1 | 8.00 | 0.0962 |
| regular_grid_32x32 | radius | 1024 | 19092 | 0 | 1 | 20.00 | 0.1371 |
| regular_grid_32x32 | hybrid | 1024 | 11652 | 0 | 1 | 12.00 | 0.1017 |
| jittered_grid_32x32 | knn | 1024 | 8192 | 0 | 1 | 8.00 | 0.0565 |
| jittered_grid_32x32 | radius | 1024 | 17714 | 0 | 1 | 21.00 | 0.1975 |
| jittered_grid_32x32 | hybrid | 1024 | 13504 | 0 | 1 | 17.00 | 0.1576 |
| sparse_clusters | knn | 320 | 2560 | 0 | 7 | 8.00 | 0.0206 |
| sparse_clusters | radius | 320 | 7334 | 0 | 7 | 23.00 | 0.0993 |
| sparse_clusters | hybrid | 320 | 7258 | 0 | 7 | 23.00 | 0.1193 |

## Key observations

- jittered_grid_32x32: best connectivity is `knn` (isolated=0, weak_components=1, runtime=0.057s). Denser graphs (max edges) come from `radius` (n_edges=17714); radius has n_edges=17714.
- regular_grid_32x32: best connectivity is `knn` (isolated=0, weak_components=1, runtime=0.096s). Denser graphs (max edges) come from `radius` (n_edges=19092); radius has n_edges=19092.
- sparse_clusters: best connectivity is `knn` (isolated=0, weak_components=7, runtime=0.021s). Denser graphs (max edges) come from `radius` (n_edges=7334); radius has n_edges=7334.
- Overall: `knn` is the fastest strategy on average runtime across scenarios.
