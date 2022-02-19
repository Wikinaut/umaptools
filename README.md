# umaptools
Collection of utility scripts for umaps on https://umap.openstreemap.fr

## gridparse.py

1. Download an existing umap
2. Bounding box function

   calculate a bounding area to bound all features in a map
2. Grid function

   draw a grid n by m polygon rectangles (sectors)   
   number each sector with a char-digit combination like A1..D4   
   create a json file comprising the grid and the sector identifiers   
   
3. Text function
   extract all feature names and texts   
   order the features by their position, number them and write a text file   

<img src="https://raw.githubusercontent.com/Wikinaut/umaptools/documentation/testumap-with-3x3-grid.png" width=1200>

```
usage: ./gridparse umapnumber [-h] [-x] [-y] [-c|--color] [-w|weight] [-o|opacity]

Umap parser adds a grid and extract, sorts, numbers texts according to coordinates

positional arguments:
  umapnumber            number of the umap you want to process

optional arguments:
  -h, --help            show this help message and exit
  -x {1,2,3,4,5,6,7,8,9}
                        number of x tiles
  -y {1,2,3,4,5,6,7,8,9}
                        number of y tiles
  -c COLOR, --color COLOR
                        color of the grid lines
  -w WEIGHT, --weight WEIGHT
                        weight (width) of the grid lines
  -o OPACITY, --opacity OPACITY
                        opacity of the grid lines
```
