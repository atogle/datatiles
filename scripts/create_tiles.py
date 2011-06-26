#!/usr/bin/env python
import mapnik2
import globalmaptiles
import datatiles
import psycopg2
import json
import sys
import os

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        geography = sys.argv[2]
        
        if os.path.exists(config_file):
            config = json.load(open(config_file))

            dt = datatiles.DataTiles(config, geography)
            dt.create_tiles()