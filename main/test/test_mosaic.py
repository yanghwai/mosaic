from unittest import TestCase
from os.path import dirname, join
from main.core.mosaic import Mosaic


target_uri = join(dirname(__file__), "image_resources", "target.png")
red_uri = join(dirname(__file__), "image_resources", "red.png")
green_uri = join(dirname(__file__), "image_resources", "green.png")
blue_uri = join(dirname(__file__), "image_resources", "blue.png")


class TestMosaic(TestCase):

    def test_add_tiles(self):
        mosaic_manager = Mosaic(target_uri)
        self.assertEqual(len(mosaic_manager.tile_library.library), 0)

        mosaic_manager.add_tiles([red_uri, green_uri, blue_uri])
        self.assertEqual(len(mosaic_manager.tile_library.library), 3)

    def test_transform(self):
        mosaic_manager = Mosaic(target_uri)
        mosaic_manager.add_tiles([red_uri, green_uri, blue_uri])
        mosaic_manager._prepare_resources()

        w_original = mosaic_manager.original_image.width()
        w_tile = mosaic_manager.tile_size[0]
        self.assertEqual(w_original, 10 * w_tile)

    def test_match(self):
        mosaic_manager = Mosaic(red_uri)
        mosaic_manager.add_tiles([red_uri, green_uri, blue_uri])
        mosaic_manager._prepare_resources()
        components = mosaic_manager._match()
        for component in components:
            self.assertEqual(red_uri, component.image._uri)

    def test_create(self):
        mosaic_manager = Mosaic(target_uri)
        mosaic_manager.add_tiles(([red_uri, green_uri, blue_uri]))
        mosaic_manager._prepare_resources()
        img = mosaic_manager._create(mosaic_manager._match())
        self.assertIsNotNone(img)