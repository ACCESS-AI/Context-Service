#!/usr/bin/env python3

import sys

try:
    from universal.harness import *
except:
    sys.path.append("../../universal/")
    from harness import *

implementation = grading_import("task", "electric_car")

class TestElectricCar(AccessTestCase):

    def test00_gas_init(self):
        try:
            sut = implementation.ElectricCar(123.4, 3.45)
            actual_cur, actual_max = sut.get_battery_status()
        except:
            m = "Unexpected error when checking the battery of an ElectricCar directly after initialization."
            self.hint(m)
            self.fail()
        m = "Incorrect result when checking the battery of an ElectricCar directly after initialization."
        self.hint(m)
        self.assertAlmostEqual(123.4, actual_cur, delta=0.001)
        self.hint(m)
        self.assertAlmostEqual(123.4, actual_max, delta=0.001)

    def test01_remaining_range(self):
        try:
            sut = implementation.ElectricCar(12.0, 24.0)
            actual = sut.get_remaining_range()
            expected = 24.0
        except:
            m = "Unexpected error when checking the remaining range of an ElectricCar with a full battery."
            self.hint(m)
            self.fail()
        m = "Incorrect result when checking the remaining range of an ElectricCar with a full battery."
        self.hint(m)
        self.assertAlmostEqual(expected, actual, delta=0.001)

    def test02_drive(self):
        try:
            sut = implementation.ElectricCar(10.0, 500.0)
            sut.drive(100.0)
            actual_cur, actual_max = sut.get_battery_status()
        except:
            m = "Unexpected error when checking the battery of an ElectricCar after a short drive."
            self.hint(m)
            self.fail()
        m = "Incorrect result when checking the battery of an ElectricCar after a short drive."
        self.hint(m)
        self.assertAlmostEqual(8.0, actual_cur, delta=0.001)
        self.hint(m)
        self.assertAlmostEqual(10.0, actual_max, delta=0.001)

    def test03_error_drive_wrong_type(self):
        try:
            sut = implementation.ElectricCar(1.0, 2.0)
            sut.drive("")
        except Warning:
            return
        except:
            m = "Unexpected error when passing a non-float to 'ElectricCar.drive'."
            self.hint(m)
            self.fail()
        else:
            m = "Passing a non-float to 'ElectricCar.drive' should raise a Warning."
            self.hint(m)
            self.fail()

    def test04_error_drive_too_small(self):
        try:
            sut = implementation.ElectricCar(1.0, 2.0)
            sut.drive(-1.0)
        except Warning:
            return
        except:
            m = "Unexpected error when passing a negative distance to 'ElectricCar.drive'."
            self.hint(m)
            self.fail()
        else:
            m = "Passing a negative distance to 'ElectricCar.drive' should raise a Warning."
            self.hint(m)
            self.fail()

    def test05_error_drive_too_far(self):
        try:
            sut = implementation.ElectricCar(10.0, 100.0)
            sut.drive(100.1)
        except Warning:
            return
        except:
            m = "Unexpected error when driving an ElectricCar until the battery is depleted."
            self.hint(m)
            self.fail()
        else:
            m = "Driving an ElectricCar until the battery is depleted should raise a Warning."
            self.hint(m)
            self.fail()

    def test06_error_drive_too_far_depletes_gas_tank(self):
        try:
            sut = implementation.ElectricCar(10.0, 100.0)
            sut.drive(100.1)
        except:
            pass
        else:
            self.hint("Depleting the battery in an ElectricCar does not raise an exception.")
            self.fail()
        try:
            actual = sut.get_battery_status()
        except:
            self.hint("Failed to get battery status of an ElectricCar after fully depleting the battery.")
            self.fail()
        m = "Driving a ElectricCar until the battery is depleted should set the battery charge level to 0."
        self.hint(m)
        self.assertEqual((0, 10), actual)

    def test07_charge(self):
        try:
            sut = implementation.ElectricCar(10.0, 1000.0)
            sut.drive(150.0)
            sut.charge(1.0)
            actual_cur, actual_max = sut.get_battery_status()
        except:
            m = "Unexpected error when checking the battery of an ElectricCar after driving and charging."
            self.hint(m)
            self.fail()
        m = "Incorrect result when checking the battery of an ElectricCar after driving and charging."
        self.hint(m)
        self.assertAlmostEqual(9.5, actual_cur, delta=0.001)
        self.hint(m)
        self.assertAlmostEqual(10.0, actual_max, delta=0.001)

    def test08_error_battery_overcharge(self):
        try:
            sut = implementation.ElectricCar(10.0, 200.0)
            sut.drive(100.0)
            sut.charge(5.1)
        except Warning:
            return
        except:
            m = "Unexpected error when overcharging the battery of an ElectricCar after a drive."
            self.hint(m)
            self.fail()
        else:
            m = "Overcharging the battery of an ElectricCar after a drive should raise a Warning."
            self.hint(m)
            self.fail()

    def test09_error_init_capacity_type(self):
        try:
            implementation.ElectricCar("", 3.45)
        except Warning:
            return
        except:
            m = "Unexpected error initializing an ElectricCar with a non-float battery capacity."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing an ElectricCar with a non-float battery capacity should raise a Warning."
            self.hint(m)
            self.fail()

    def test10_error_init_capacity_value(self):
        try:
            implementation.ElectricCar(-1.0, 3.45)
        except Warning:
            return
        except:
            m = "Unexpected error initializing an ElectricCar with a non-positive battery capacity."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing an ElectricCar with a non-positive battery capacity should raise a Warning."
            self.hint(m)
            self.fail()

    def test11_error_init_range_type(self):
        try:
            implementation.ElectricCar(123.4, "")
        except Warning:
            return
        except:
            m = "Unexpected error initializing an ElectricCar with a non-float range."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing an ElectricCar with a non-float range should raise a Warning."
            self.hint(m)
            self.fail()

    def test12_error_init_range_value(self):
        try:
            implementation.ElectricCar(123.4, -1.0)
        except Warning:
            return
        except:
            m = "Unexpected error initializing an ElectricCar with a non-positive range."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing an ElectricCar with a non-positive range should raise a Warning."
            self.hint(m)
            self.fail()
