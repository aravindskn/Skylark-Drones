"""
Copyright (C) 2016 Skylark Drones
Unit test case for FlightMath library class
"""

from unittest import TestCase
import flightmath
import dateutil.tz
from datetime import datetime
import os, sys

sys.path.insert(0, os.path.abspath(".."))


class TestFlightMath(TestCase):

    def setUp(self):
        self.fm = flightmath.FlightMath()

    def test_convert_ms_to_duration(self):
        self.assertEqual(self.fm.convert_ms_to_duration(25352230), {'hours': 7, 'minutes': 2, 'seconds': 32})

    def test_calculate_wind_speed(self):
        self.assertEqual(self.fm.calculate_wind_speed([20.0, 10.0], [10.0, 5.0]), [10.0, 5.0])

    def test_calculate_max_value(self):
        self.assertEqual(self.fm.calculate_max_value([15, 25, 30]), 30)

    def test_calculate_average(self):
        self.assertEqual(self.fm.calculate_average([2.0, 3.0, 7.0]), 4.0)
        self.assertEqual(self.fm.calculate_average([1, 2, 3, 4, 5]), 3.0)

    def test_leap(self):
        self.assertEqual(self.fm.leap(datetime(2016, 2, 1, 10, 30, 15)), 17)

    def test_gps_to_utc(self):
        self.utc_time = datetime(2016, 6, 10, 9, 21, 1)
        self.assertEqual(self.fm.gps2utc(1900, 465678), self.utc_time)

    def test_gps_to_local(self):
        self.local_time = datetime(2016, 6, 10, 14, 51, 1, tzinfo=dateutil.tz.tzlocal())
        self.assertEqual(self.fm.gps_to_local(1900, 465678), self.local_time)

    def tearDown(self):
        pass
