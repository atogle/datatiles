#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage - $0 /path/to/data"
    exit 1
fi
    out=load_school_districts.sql
    if [ -f $out ];
    then
        echo "Removing [$out]"
        rm $out
    fi

    FILES=$1/*.shp
    for f in $FILES
    do
        echo "Processing [`basename $f`]"
        shp2pgsql -a -s 4269 -i -D -W LATIN1 $f school_districts >> $out
    done