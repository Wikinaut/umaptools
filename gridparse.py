#!/usr/bin/env python3

#    Utility program for umaps
#    on https://umap.openstreemap.fr
#
#
#    0. Download an existing umap
#
#    1. Bounding box function
#
#    calculate a bounding area to bound all features in a map
#
#
#    2. Grid function
#
#    draw a grid n by m polygon rectangles (sectors)
#    number each sector with a char-digit combination like A1..D4
#    create a json file comprising the grid and the sector identifiers
#
#
#    3. Text function
#
#    extract all feature names and texts
#    order the features by their position, number them and write a text file
#
#    20220217 init

import json
import urllib.request
import numpy as np
from datetime import datetime
import sys
import re
import argparse

def setup_parser():

    my_parser = argparse.ArgumentParser( prog = re.sub( '.py$', '', sys.argv[0] ),
        usage = '%(prog)s umapnumber [-h] [-x] [-y] [-c|--color] [-w|weight] [-o|opacity]',
        description = 'Umap parser adds a grid and extract, sorts, numbers texts according to coordinates'
    )

    my_parser.add_argument('umapnumber', action='store', type=int, help='number of the umap you want to process')
    my_parser.add_argument('-x', action='store', default='2', type=int, choices=range(1, 11), help='number of x tiles')
    my_parser.add_argument('-y', action='store', default='2', type=int, choices=range(1, 11), help='number of y tiles')
    my_parser.add_argument('-c','--color', action='store', default='black', type=str, help='color of the grid lines')
    my_parser.add_argument('-w','--weight', action='store', default='2', type=int, help='weight (width) of the grid lines')
    my_parser.add_argument('-o','--opacity', action='store', default='0.3', type=float, help='opacity of the grid lines')

    args = my_parser.parse_args()

    return args

args = setup_parser()
print(args)

umapnumber = args.umapnumber
gridtileslon = args.x
gridtileslat = args.y
gridxsize = "{0}x{1}".format(gridtileslon,gridtileslat)
gridcolor = args.color
gridweight = args.weight
gridopacity = args.opacity

url = "https://urban.to/projects/radnetz/umap/export/{0}".format(umapnumber)
req = urllib.request.Request(url)
r = urllib.request.urlopen(req).read()
data = json.loads(r.decode('utf-8'))

umapname = data['properties']['name']
umapdescription = data['properties']['description']

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
basicinfo = "'{0}' (umap {1}) {2}\nhttps://umap.openstreetmap.fr/de/map/map_{1}\n\n{3}". \
  format(umapname.strip(),umapnumber,now,umapdescription.strip())

print(basicinfo)

umapinfile = "umap-original-{0}-{1}.umap".format(umapname,umapnumber)
umapcirclefile = "umap-original-balls-changed-to-circles-{0}-{1}.umap".format(umapname,umapnumber)

with open(umapinfile, 'w') as infile:
    json.dump(data, infile, indent=4)

umapoutfile = "umap-with-grid-{2}-{0}-{1}.umap".format(umapname,umapnumber,gridxsize)
umapgridfile = "umap-only-grid-{1}-{0}.json".format(umapnumber,gridxsize)
umaptextfile = "umap-{0}-{1}.umap.txt".format(umapname,umapnumber)
umappointfile = "umap-only-points-{0}-{1}.json".format(umapname,umapnumber)

outbuf = []

bbox = {
    "minlon": 181.0,
    "maxlon": -181.0,
    "minlat": 91.0,
    "maxlat": -91.0,
}

def boundingbox(coor):
  global bbox
  bbox['minlon'] = min(coor[0],bbox['minlon'])
  bbox['maxlon'] = max(coor[0],bbox['maxlon'])
  bbox['minlat'] = min(coor[1],bbox['minlat'])
  bbox['maxlat'] = max(coor[1],bbox['maxlat'])


# Pass 1: Determine a boundingbox: where are features present?

for i in data['layers']:

  for j in i['features']:

    coor = [0,0] # [lon,lat]

    try:
      geometrietyp = j['geometry']['type']

      if geometrietyp == "Point":
         coor = [j['geometry']['coordinates'][0],j['geometry']['coordinates'][1]]
         boundingbox(coor)

      if (geometrietyp == "LineString") and (len(j['properties']) > 0):

         lat = []
         lon = []

         for each in j['geometry']['coordinates']:
           lon.append(each[0])
           lat.append(each[1])
           boundingbox([each[0],each[1]])

         coor = [np.median(lon),np.median(lat)]

      if geometrietyp == "Polygon":

         lat = []
         lon = []

         for each in j['geometry']['coordinates'][0]:
           lon.append(each[0])
           lat.append(each[1])
           boundingbox([each[0],each[1]])

         coor = [np.median(lon),np.median(lat)]

    except:
      None

    # loop through all layers ends


# Pass 2: Create a grid

difflon = abs(bbox['maxlon']-bbox['minlon'])
difflat = abs(bbox['maxlat']-bbox['minlat'])

deltalon = difflon/gridtileslon
deltalat = difflat/gridtileslat

grid = []

startlon = min(bbox['minlon'],bbox['maxlon'])
stoplon = max(bbox['minlon'],bbox['maxlon'])

startlat = max(bbox['minlat'],bbox['maxlat'])
stoplat = min(bbox['minlat'],bbox['maxlat'])

def uline(line,name=None,color="Black",weight=4,opacity=0.7):
  return {
          "type": "Feature",
          "properties": {
            "_umap_options": {
              "color": color,
              "opacity": opacity,
              "weight": weight,
              "showLabel": None
            },
            "name": name
          },
          "geometry": {
            "type": "LineString",
            "coordinates": line
          }
  }

def upolygon(coordinates,name=None,description=None,color="Black",weight=4,opacity=0.7):
  return {
          "type": "Feature",
          "properties": {
            "_umap_options": {
              "color": color,
              "opacity": opacity,
              "weight": weight,
              "showLabel": True,
              "fillColor": "White",
              "fillOpacity": "0.0",
              "labelDirection": "top", # or "auto",
              "popupTemplate": "Default",
              "popupShape": "Default",
              "labelInteractive": False
            },
            "name": name,
            "description": description
          },
          "geometry": {
            "type": "Polygon",
            "coordinates": [coordinates]
          }
  }


def ulayer(name,features):
  return {
            "type": "FeatureCollection",
            "features": [features],
            "_umap_options": {
                "displayOnLoad": True,
                "browsable": True,
                "remoteData": {},
                "name": name
            }
  }


def upoint(coordinates,number,name="",description=""):
  return {
    "type": "Feature",
    "properties": {
      "_umap_options": {
        "color": "Yellow",
        "showLabel": None, # show label onhover
        "iconClass": "Drop",
        "iconUrl": "https://raw.githubusercontent.com/Wikinaut/images/master/80/circle-{0}.png".format(number)
      },
      "name" : name,
      "description": description
    },
    "geometry": {
      "type": "Point",
      "coordinates": coordinates
    }
  }


blon = []
blat = []

def box(startcoor,stopcoor,sectorlon,sectorlat):
  global blon,blat

  startlon = startcoor[0]
  startlat = startcoor[1]
  stoplon = stopcoor[0]
  stoplat = stopcoor[1]

  blon.append({
    "lon1": min(startlon,stoplon),
    "lon2": max(startlon,stoplon),
    "sectorlon":  sectorlon
  })

  blat.append({
    "lat1": min(startlat,stoplat),
    "lat2": max(startlat,stoplat),
    "sectorlat": sectorlat
  })

  return [
    [startlon,startlat],[stoplon,startlat],[stoplon,stoplat],
    [startlon,stoplat],[startlon,startlat]
  ]

mapchar = range(ord('A'), ord('Z')+1)

gridboxes = []

for ilon in range(0,gridtileslon):

  for ilat in range(0,gridtileslat):

    sectorlon = chr(mapchar[ilon])
    sectorlat = str(ilat+1)

    toplon = min(startlon,stoplon)
    toplat = max(startlat,stoplat)

    gridboxes.append(upolygon(
      box(
        [toplon+ilon*deltalon,toplat-ilat*deltalat],
	[toplon+(ilon+1)*deltalon,toplat-(ilat+1)*deltalat],
        sectorlon, sectorlat
      ),
      sectorlon+sectorlat,
      json.dumps({
	"midlon" : toplon+ilon*deltalon+deltalon/2,
        "deltalon" : deltalon,
	"midlat" : toplat-ilat*deltalat-deltalat/2,
        "deltalat" : deltalat,
        "boundingbox": bbox,
        "umap": umapnumber
      },indent=4),
      gridcolor, gridweight, gridopacity
    ))


def isPresentGrid():
  for layer in data['layers']:
    if layer['_umap_options']['name'] == "Grid":
      return True
      break
  return False

if not isPresentGrid():
  data['layers'].insert(0,ulayer("Grid",gridboxes))
  print("A new grid {0} is created.".format(gridxsize))
else:
  for layer in data['layers']:
    if layer['_umap_options']['name'] == "Grid":
      # The update() method adds element(s) to the dictionary if the key is not in the dictionary.
      # If the key is in the dictionary, it updates the key with the new value.
      # Thus it would be safe to use update() here only and consequently to drop the insert() part above.
      layer.update(ulayer("Grid",gridboxes))
      print("An existing grid is updated by a {0} grid.".format(gridxsize))
      break

with open(umapgridfile, 'w') as gridfile:
    json.dump(ulayer("Grid-{0}".format(gridxsize),gridboxes), gridfile, indent=4)


def findsector(coor):
  global blon,blat

  if coor[0] == 0.0 and coor[1] == 0.0:
    return ["",""]

  for i in range(len(blon)):
    if coor[0] >= blon[i]['lon1'] and coor[0] <= blon[i]['lon2']:
      sectorlon = blon[i]['sectorlon']
      break

  for i in range(len(blat)):
    if coor[1] >= blat[i]['lat1'] and coor[1] <= blat[i]['lat2']:
      sectorlat = blat[i]['sectorlat']
      break

  return [sectorlon,sectorlat]


# Pass 3: Assign sector identifiers

for i in data['layers']:

  if i['_umap_options']['name'] == "Grid":
    continue

  for j in i['features']:

    coor = [0,0] # [lon,lat]

    try:
      description = j['properties']['description'].strip()
    except:
      description = ""

    try:
      if j['properties']['_umap_options']['iconClass'] == "Ball":
        j['properties']['_umap_options']['iconClass'] = "Circle"
        j.update()
    except:
      pass

    try:
      geometrietyp = j['geometry']['type']

      if geometrietyp == "Point":
         coor = [j['geometry']['coordinates'][0],j['geometry']['coordinates'][1]]

      if (geometrietyp == "LineString") and (len(j['properties']) > 0):

         lat = []
         lon = []

         for each in j['geometry']['coordinates']:
           lon.append(each[0])
           lat.append(each[1])

         coor = [np.median(lon),np.median(lat)]

      if geometrietyp == "Polygon":

         lat = []
         lon = []

         for each in j['geometry']['coordinates'][0]:
           lon.append(each[0])
           lat.append(each[1])

         coor = [np.median(lon),np.median(lat)]

    except:
      geometrietyp = ""

    try:
      name = j['properties']['name']
    except:
      name = ""

    sector = findsector(coor)

    if len(name+description) > 0:
       if len(description) != 0:
         outbuf.append([
           coor,
           sector[0],sector[1],
           geometrietyp,
           "[{0}] {1}\n{2}"
           .format(sector[0]+sector[1],name.rstrip('\n'),description.rstrip('\n'))
         ])
       else:
         outbuf.append([
           coor,
           sector[0],sector[1],
           geometrietyp,
           "[{0}] {1}".format(sector[0]+sector[1],name.rstrip('\n'))
         ])

outbuf_sorted = sorted(outbuf, key=lambda x: (x[2],x[1],-x[0][1],x[0][0]))

f = open(umaptextfile, "w")
f.write("{0}\nBoundingbox: {1}\n\n".format(basicinfo,bbox))

bubbles = []

i = 1
for line in outbuf_sorted:
  lon = line[0][0]
  lat = line[0][1]
  f.write("{4:02d}.\n{3}\n[{0:0.6f},{1:0.6f}] ({2})\n\n".format(lon,lat,line[3],line[4],i))
  description=""
  bubbles.append(upoint([lon,lat],i,"{0:02d} {1}".format(i,line[4]),description))
  i += 1

with open(umappointfile, 'w') as pointfile:
  json.dump(ulayer("Points",bubbles), pointfile, indent=4)


"""
# draw the boundingbox in a new layer

data['layers'].append(
  ulayer("Boundingbox",
    upolygon(box([startlon,startlat],[stoplon,stoplat]),
    "BoundingBox","White",4,0.7)
  )
)

# draw horizontal and vertical grid lines in a new layer

gridlines=[]
  for i in grid:
  gridlines.append(uline(i,"Gridline","White",4,0.7))
data['layers'].append(ulayer("Gridlines",gridlines))
"""

# Pass 3: Assign the grid sector labels to each feature

# write new modified json to disk

with open(umapoutfile, 'w') as outfile:
    json.dump(data, outfile, indent=4)

print("Boundingbox: {0}".format(bbox))
print("Downloaded umap written to '{0}'.".format(umapinfile))
print("Umap with grid and sector numbers written to '{0}'.".format(umapoutfile))
print("Grid as single umap layer written to '{0}'.".format(umapgridfile))
print("Text data written to '{0}'.".format(umaptextfile))

with open(umapcirclefile, 'w') as outfile:
    json.dump(data, outfile, indent=4)
