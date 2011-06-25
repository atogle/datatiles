#!/usr/bin/env python
import mapnik2
import globalmaptiles
import psycopg2
import json
import sys
import os

merc = globalmaptiles.GlobalMercator()
zoom = 4

def rgbify(num):
    r = num & 0xff
    g = (num >> 8) & 0xff
    b = (num >> 16) & 0xff
    return r, g, b

def get_style(data_col, config, geography):
    style = mapnik2.Style()
    conn = psycopg2.connect(host=config["db"]["host"],user=config["db"]["user"],password=config["db"]["password"],database=config["db"]["database"])
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT %s FROM %s;" % (config[geography]["id_col"], config[geography]["table"]))
    results = cur.fetchall()
    
    for vals in results:
        rule = mapnik2.Rule()
        val = int(vals[0])
        
        ex = "[%s] = %d" % (config[geography]["id_col"], val)
        
        rule.filter = mapnik2.Expression(str(ex))
        rule.symbols.append(mapnik2.PolygonSymbolizer(mapnik2.Color(0, 0, val)))
        style.rules.append(rule)
    
    cur.close
    conn.close
    return style

def create_tile(tile_x, tile_y, zoom, style, config, geography):
    m = mapnik2.Map(256, 256)
    m.append_style('data_style', style)
    lyr = mapnik2.Layer('Geometry from PostGIS')
    
    bounds = merc.TileBounds(tile_x, tile_y, zoom)
    
    params = dict(
        host=str(config["db"]["host"]),
        user=str(config["db"]["user"]),
        password=str(config["db"]["password"]),
        dbname=str(config["db"]["database"]),
        table=str(config[geography]["table"]),
        estimate_extent=False,
        extent=','.join(map(str, bounds)) #'-20037508,-19929239,20037508,19929239'
    ) 
    
    lyr.datasource = mapnik2.PostGIS(**params)

    lyr.styles.append('data_style')
    m.layers.append(lyr)
    m.zoom_to_box(lyr.envelope())
    
    goog_x, goog_y = merc.GoogleTile(tile_x, tile_y, zoom)
    
    file_name = '../tiles/%d_%d_%d.png' % (zoom, goog_x, goog_y)
    mapnik2.render_to_file(m, file_name, 'png')

def get_tile_bounds(config, zoom):
    tl_x, tl_y = merc.MetersToTile(config["extent"]["left"], config["extent"]["top"], zoom)
    br_x, br_y = merc.MetersToTile(config["extent"]["right"], config["extent"]["bottom"], zoom)
    
    return (tl_x, tl_y, br_x, br_y)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        geography = sys.argv[2]
        if os.path.exists(config_file):
            config = json.load(open(config_file))
            
            style = get_style(config[geography]["table"], config, geography)
            tl_x, tl_y, br_x, br_y = get_tile_bounds(config, zoom)
            
            print tl_x, tl_y, br_x, br_y
            
            for x in range(tl_x, br_x+1):
                for y in range(br_y, tl_y+1):
                    print x, y
                    create_tile(x, y, zoom, style, config, geography)