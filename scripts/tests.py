import unittest
import create_tiles

class TileMadnessTests (unittest.TestCase):
    def test_tile_bounds(self):
        config = {"extent": {
            "top": 12520000,
            "left": -20030000,
            "bottom": 2504000,
            "right": -7514000
        }}
        
        bounds = create_tiles.get_tile_bounds(config, 4)
        self.assertEqual(bounds, (0, 12, 5, 8))


    def test_tile_bounds(self):
        self.assertEqual(create_tiles.rgbify(1), (0, 0, 1))
        self.assertEqual(create_tiles.rgbify(256), (0, 1, 0))
        self.assertEqual(create_tiles.rgbify(65536), (1, 0, 0))
        
        
        
if __name__ == "__main__":
    unittest.main()