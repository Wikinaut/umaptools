#!/usr/bin/bash
# create a semi-transparent circle image with an annotation text

echo "circle <text> <circlesize> <fillcolor> <opacity>"

magick -size "$2"x"$2" \
	xc:none -fill "$3" \
	-draw 'circle %[fx:w/2],%[fx:h/2] %[fx:w/2],%[fx:h]' \
        -alpha set -channel A -evaluate Multiply "$4" +channel \
        -set pt %[fx:h/1.4] \
	-set ofs %[fx:h/18] \
	-pointsize %[pt] -gravity center -stroke black -strokewidth 2 -fill black -annotate +0+%[ofs] "$1" \
	"circle-${1}.png"
