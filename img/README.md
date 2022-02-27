# images

## create an circle image 100x100 yellow with opacity 0.7 and text "42"
./make-circle.sh "42" 100 yellow 0.7


## create yellow images with numbers 1..99
for i in {1..99};do ./make-circle.sh "$i" 80 yellow 0.7;done
