#!/usr/bin/env python

import mapnik2
import globalmaptiles
import psycopg2

tile_calc = globalmaptiles.GlobalMercator()
zoom = 4
min_tile_x = 2
max_tile_x = 6
min_tile_y = 9
max_tile_y = 11
table = "states_3857"
data_col = "geoid10"
db_pass = "your_password"

def get_style(data_col):
    style = mapnik2.Style()
    conn = psycopg2.connect(host='localhost',user='postgres',password=db_pass,database='donorschoose')
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT %s FROM %s;" % (data_col, table))
    results = cur.fetchall()
    
    for vals in results:
        rule = mapnik2.Rule()
        ex = "[%s] = '%s'" % (data_col, vals[0])
        
        rule.filter = mapnik2.Expression(ex)
        rule.symbols.append(mapnik2.PolygonSymbolizer(mapnik2.Color(0, 0, int(vals[0]))))
        style.rules.append(rule)
    
    cur.close
    conn.close
    return style

def create_tile(tile_x, tile_y, zoom, style):
    m = mapnik2.Map(256, 256)
    m.append_style('data_style', style)
    lyr = mapnik2.Layer('Geometry from PostGIS')
    
    bounds = tile_calc.TileBounds(tile_x, tile_y, zoom)
    
    params = dict(host='localhost', user='postgres', password=db_pass, dbname='donorschoose', table=table)
    params['estimate_extent'] = False
    params['extent'] = ','.join(map(str, bounds)) #'-20037508,-19929239,20037508,19929239'
    
    lyr.datasource = mapnik2.PostGIS(**params)

    lyr.styles.append('data_style')
    m.layers.append(lyr)
    m.zoom_to_box(lyr.envelope())
    
    goog_x, goog_y = tile_calc.GoogleTile(tile_x, tile_y, zoom)
    
    file_name = '../tiles/%d_%d_%d.png' % (zoom, goog_x, goog_y)
    mapnik2.render_to_file(m, file_name, 'png')

style = get_style(data_col)
for x in range(min_tile_x, max_tile_x):
    for y in range(min_tile_y, max_tile_y):
        create_tile(x, y, zoom, style)