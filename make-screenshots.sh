#!/usr/bin/bash
# 20220224
# Parameter für die Screenshots der Übersichtspläne und die Teilpläne

# RIAS
node screenshot.js https://umap.openstreetmap.fr/de/map/__705676#18/52.4820/13.3383 4050 2800 umap-overview-705676.png
./gridparse.py 705676 -x 3 -y 3 -c magenta -w 2 -o 0.9
node make-tiled-screenshots.js "umap-only-grid-3x3-705676.json" 2000 1800

# UML
node screenshot.js https://umap.openstreetmap.fr/de/map/__716884#19/52.47720/13.3310 2500 2250 umap-overview-716884.png
./gridparse.py 716884 -x 3 -y 3 -c magenta -w 2 -o 0.9
node make-tiled-screenshots.js "umap-only-grid-3x3-716884.json" 900 900
