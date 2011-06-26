import mapnik2
import globalmaptiles
import psycopg2
import json
import sys
import os

class DataTiles():
    def __init__(self, config, geography="states"):
        self.global_mercator = globalmaptiles.GlobalMercator()
        self.extent = config["extent"]
        self.db = config["db"]
        self.geography  = config[geography]

    @staticmethod
    def rgbify(num):
        r = (num >> 16) & 0xff
        g = (num >> 8) & 0xff
        b = num & 0xff
        return r, g, b

    def get_style(self):
        style = mapnik2.Style()
        conn = psycopg2.connect(host=self.db["host"],user=self.db["user"],password=self.db["password"],database=self.db["database"])
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT %s FROM %s;" % (self.geography["id_col"], self.geography["table"]))
        results = cur.fetchall()
    
        for vals in results:
            rule = mapnik2.Rule()
            val = int(vals[0])
        
            ex = "[%s] = %d" % (self.geography["id_col"], val)
        
            rule.filter = mapnik2.Expression(str(ex))
            rule.symbols.append(mapnik2.PolygonSymbolizer(mapnik2.Color(0, 0, val)))
            style.rules.append(rule)
    
        cur.close
        conn.close
        return style

    def create_tile(self, tile_x, tile_y, zoom, style):
        m = mapnik2.Map(256, 256)
        m.append_style('data_style', style)
        lyr = mapnik2.Layer('Geometry from PostGIS')
    
        bounds = self.global_mercator.TileBounds(tile_x, tile_y, zoom)
    
        params = dict(
            host=str(self.db["host"]),
            user=str(self.db["user"]),
            password=str(self.db["password"]),
            dbname=str(self.db["database"]),
            table=str(self.geography["table"]),
            estimate_extent=False,
            extent=','.join(map(str, bounds)) #'-20037508,-19929239,20037508,19929239'
        ) 
    
        lyr.datasource = mapnik2.PostGIS(**params)

        lyr.styles.append('data_style')
        m.layers.append(lyr)
        m.zoom_to_box(lyr.envelope())
    
        goog_x, goog_y = self.global_mercator.GoogleTile(tile_x, tile_y, zoom)
    
        file_name = '../tiles/%d_%d_%d.png' % (zoom, goog_x, goog_y)
        mapnik2.render_to_file(m, file_name, 'png')

    def get_tile_bounds(self, zoom):
        tl_x, tl_y = self.global_mercator.MetersToTile(self.extent["left"], self.extent["top"], zoom)
        br_x, br_y = self.global_mercator.MetersToTile(self.extent["right"], self.extent["bottom"], zoom)
    
        return (tl_x, tl_y, br_x, br_y)
        
    def create_tiles(self):
        style = self.get_style()
        
        for z in range(self.geography["min_zoom"], self.geography["max_zoom"]+1):
            tl_x, tl_y, br_x, br_y = self.get_tile_bounds(z)
            
            for x in range(tl_x, br_x+1):
                for y in range(br_y, tl_y+1):
                    print z, x, y
                    self.create_tile(x, y, z, style)