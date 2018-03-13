weight=24
height=24

opencv_traincascade -data output_data -vec positives.vec -bg bg_neg.txt -npos $1 -nneg $2 -nstate $3 -w $weight -h $height -precalcValBufSize 2048 -precalcIdxBufSize 2048


# $1 number of positive image
# $2 number of negative image
# $1 number of state

