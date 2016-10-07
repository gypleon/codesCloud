#!/bin/bash

# filter out unrelated fields and the title
fieldsFilter()
{
    awk -F',' '{print $1,$2,$3}' "$1" > "$2"
    sed -i '1d' "$2"
}

# convert rating into l-like u-unlike
likeOrUnlike()
{
    
    awk '{if($3>=0.5 && $3<=2.5)
             {print $1,$2,"u"}
           else if($3>2.5 && $3<=5)
             {print $1,$2,"l"}
           else
             {print $1,$2,$3 > "./abnormalratings"}}' "$1" > "$2"
    # mv -f "$2" "$1"
}

# merge lines according to users
mergelines()
{
    
}

# split file by userid
# to be applied in Hadoop MapReduce
splitlikefile()
{
    lastuser=`tail -1 $1 | awk '{print $1}'`
    totalround=$(( $lastuser / $2 + 1 ))
    round=1
    for((;round<=totalround;round++))
    do
        startuser=$(( ( $round - 1 ) * $2 + 1 ))
        awk '{if($1<="'$round'"*"'$2'" && $1>("'$round'"-1)*"'$2'"){print}}' "$1" > "$3$startuser"
    done
}

main()
{
    datadir="./ml-20m"
    datasource="$datadir/ratings.csv"
    tempfile="$datadir/tmp"
    likeorunlike="$datadir/likeorunlike"
    splitscale=20000
    fieldsFilter $datasource $tempfile
    likeOrUnlike $tempfile $likeorunlike
    #mergelines $tempfile $likeorunlike
    #splitlikefile $like $splitscale "$datadir/l_"
    #splitlikefile $unlike $splitscale "$datadir/u_"
}
main
