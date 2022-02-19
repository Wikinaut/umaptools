# umaptools
Collection of utility scripts for umaps on https://umap.openstreemap.fr

## gridparse.py

1. Download an existing umap
2. Bounding box function

   calculate a bounding area to bound all features in a map
2. Grid function

   draw a grid n by m polygon rectangles (sectors)   
   number each sector with a char-digit combination like A1..Z20   
   create a json file comprising the grid and the sector identifiers   
   
3. Text function
   extract all feature names and texts   
   order the features by their position, number them and write a text file   
