from unittest import TestCase
import geotagger
import os, sys

sys.path.insert(0, os.path.abspath(".."))


class TestGeotagger(TestCase):

    def setUp(self):
        self.gt = geotagger.Geotagger()
        self.base_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
        self.cam_file_path = self.base_path + "SAMPLE-CAM.csv"
        self.raw_images_folder = self.base_path + "Raw_Images"

    def test_verify_cam_file_exists(self):
        self.assertTrue(self.gt.verify_cam_file_exists(self.cam_file_path))

    def test_verify_raw_images_folder_exists(self):
        self.assertTrue(self.gt.verify_raw_images_folder(self.raw_images_folder))

    def test_check_one_to_one_count(self):
        self.assertFalse(self.gt.check_one_to_one_count(self.cam_file_path, self.raw_images_folder))

    def tearDown(self):
        pass
