# umaptools
Collection of utility scripts for umaps on https://umap.openstreemap.fr

## gridparse.py

1. Download an existing umap
2. Bounding box function   
   calculate a bounding area to bound all features in a map
2. Grid function   
   draw a grid n by m polygon rectangles (sectors)   
   number each sector with a char-digit combination like A1..D4   
   create a json file comprising the grid coordinates and the sector identifiers   
3. Text function   
   extract all feature names and texts   
   order the features by their position, number them and write a text file   
4. Change feature "Ball" (needle) to "Circle"
5. Create a new layer "Points" with all existing Features west-east/north-south sorted and small numbered icon class "Drop"
6. Copy name/description of existing Features to the new layer "Points"
7. Set showLabel option to "None", which effectively shows the text when hovering over them

Example for grid generation:  
<img src="https://raw.githubusercontent.com/Wikinaut/umaptools/main/documentation/testumap-with-3x3-grid.png" width=1200>

Example for numbered points ("drops") generation:  
<img src="https://raw.githubusercontent.com/Wikinaut/umaptools/main/documentation/testumap-with-numbered-drops.png" width=400>

* https://twitter.com/Wikinaut/status/1495188916198162439
```
New utility script for umaps: gridparse.py
+ determine bounding box
+ create user-defined Grid*)
+ label sectors with ids "A1"…
+ extract feature texts, add sector ids to the texts
+ sort texts from NW→SE**)
*) manual import→umap
**) text
```

```
usage: ./gridparse umapnumber [-h] [-x] [-y] [-c|--color] [-w|weight] [-o|opacity]

Umap parser adds a grid and extracts, sorts, numbers texts according to coordinates

positional arguments:
  umapnumber            number of the umap you want to process

optional arguments:
  -h, --help            show this help message and exit
  -x {1,2,3,4,5,6,7,8,9,10}
                        number of x tiles
  -y {1,2,3,4,5,6,7,8,9,10}
                        number of y tiles
  -c COLOR, --color COLOR
                        color of the grid lines
  -w WEIGHT, --weight WEIGHT
                        weight (width) of the grid lines
  -o OPACITY, --opacity OPACITY
                        opacity of the grid lines
```

## image tools

## make-circle.sh
create an circle image 80x80 yellow with opacity 1.0 and text "42" 

```./make-circle.sh "42" 100 yellow 1.0```

<img src="https://raw.githubusercontent.com/Wikinaut/umaptools/main/img/80/circle-42.png" />

create yellow 80x80 number 1..99 images with opacity 0.7  

```for i in {1..99};do ./make-circle.sh "$i" 80 yellow 0.7;done```

Result see → https://github.com/Wikinaut/umaptools/tree/main/img/80


## screenshot tools

## screenshot.js
Creates a single screenshot of a umap in possibly a very high resolution (e.g. zoom 19). Requires/uses puppeteer.  

```node screenshot.js umapnumber [width height imageoutputfile]```

## make-tiled-screenshots.js
Creates single screenshots for each of the n x m grid sectors of a umap – the grid added by a previous run and import of gridparse.py – the screenshots have a user-definable high resolution (zoom). The script parses the grid layer of the umap where it finds the precomputed corner coordinates and the sector identifier (like 'A1') of each sector. it then creates separate screenshot image files with the same image width and height. Requires/uses puppeteer.

```node make-tiled-screenshots.js umap-grid.json```
