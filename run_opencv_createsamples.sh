weight=24
height=24
# opencv_createsamples -img main_img/$1* -bg bg_pos.txt -info info/info.lst -pngoutput info -maxxangle 0.1 -maxyangle 0.1 -maxzangle 0.1 -num $2
echo "generate positive info.lst done"
# opencv_createsamples -info info/info.lst -num $2 -w $weight -h $height -vec positives.vec 
opencv_createsamples -img main_img/$1* -bg bg_pos.txt -vec positives.vec -maxxangle 0.1 -maxyangle 0.1 -maxzangle 0.1 -num $2
# opencv_createsamples -info bg_pos.txt -bg bg_pos.txt -vec positives.vec -maxxangle 0.1 -maxyangle 0.1 -maxzangle 0.1 -num $2
echo "generate vector done"

# $1 selected main image
# $2 positive number 