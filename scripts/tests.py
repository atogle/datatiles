import unittest
import datatiles
import json

config = json.load(open("tile.yml"))
dt = datatiles.DataTiles(config, "states")

class TileMadnessTests (unittest.TestCase):
    def test_tile_bounds(self):
        bounds = dt.get_tile_bounds(4)
        self.assertEqual(bounds, (0, 12, 5, 8))

    def test_tile_bounds(self):
        self.assertEqual(dt.rgbify(1), (0, 0, 1))
        self.assertEqual(dt.rgbify(256), (0, 1, 0))
        self.assertEqual(dt.rgbify(65536), (1, 0, 0))
        
if __name__ == "__main__":
    unittest.main()