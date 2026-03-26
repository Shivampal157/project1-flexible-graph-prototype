# Flexible Graph Construction Prototype Report

| scenario | strategy | nodes | edges | isolated | weak_components | out_deg_p95 | runtime (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| regular_grid_32x32 | knn | 1024 | 8192 | 0 | 1 | 8.00 | 0.1130 |
| regular_grid_32x32 | radius | 1024 | 19092 | 0 | 1 | 20.00 | 0.2128 |
| regular_grid_32x32 | hybrid | 1024 | 11652 | 0 | 1 | 12.00 | 0.1092 |
| jittered_grid_32x32 | knn | 1024 | 8192 | 0 | 1 | 8.00 | 0.0669 |
| jittered_grid_32x32 | radius | 1024 | 17714 | 0 | 1 | 21.00 | 0.1615 |
| jittered_grid_32x32 | hybrid | 1024 | 13504 | 0 | 1 | 17.00 | 0.0903 |
| sparse_clusters | knn | 320 | 2560 | 0 | 7 | 8.00 | 0.0156 |
| sparse_clusters | radius | 320 | 7334 | 0 | 7 | 23.00 | 0.0967 |
| sparse_clusters | hybrid | 320 | 7258 | 0 | 7 | 23.00 | 0.0990 |
