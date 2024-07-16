#!/usr/bin/env python3

import sys

try:
    from universal.harness import *
except:
    sys.path.append("../../universal/")
    from harness import *

implementation = grading_import("task", "hybrid_car")

class TestHybridCar(AccessTestCase):

    def _assert_resources(self, sut, gas_cur, gas_max, bat_cur, bat_max, m_part):
        try:
            actual_gcur, actual_gmax = sut.get_gas_tank_status()
            actual_bcur, actual_bmax = sut.get_battery_status()
        except:
            m = "Unexpected error when checking gas tank and battery of a Hybrid car after {}."
            m.format(m_part)
            self.hint(m)
            self.fail()

        tmp = "Incorrect {} when checking the gas tank of a Hybrid car after {}."
        m = tmp.format("current level", m_part)
        self.hint(m)
        self.assertAlmostEqual(gas_cur, actual_gcur, delta=0.001)
        m = tmp.format("maximum level", m_part)
        self.hint(m)
        self.assertAlmostEqual(gas_max, actual_gmax, delta=0.001)

        tmp = "Incorrect {} when checking the battery of a Hybrid car after {}."
        m = tmp.format("current level", m_part)
        self.hint(m)
        self.assertAlmostEqual(bat_cur, actual_bcur, delta=0.001)
        m = tmp.format("maximum level", m_part)
        self.hint(m)
        self.assertAlmostEqual(bat_max, actual_bmax, delta=0.001)


    def test00_battery_and_gas_init(self):
        try:
            sut = implementation.HybridCar(1.0, 2.0, 3.0, 4.0)
        except:
            m = "Unexpected error when initializing a HybridCar."
            self.hint(m)
            self.fail()
        self._assert_resources(sut, 1.0, 1.0, 3.0, 3.0, "initialization")

    def test01_remaining_range(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            actual = sut.get_remaining_range()
            expected = 500.0
        except:
            m = "Unexpected error when checking the range of a HybridCar directly after initialization."
            self.hint(m)
            self.fail()
        m = "Incorrect result when checking the range of a HybridCar directly after initialization."
        self.hint(m)
        self.assertAlmostEqual(expected, actual, delta=0.001)

    def test02_drive_battery_implicit(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.drive(100.0)
        except:
            m = "Unexpected error when driving a HybridCar for a short distance (without selecting the mode)."
            self.hint(m)
            self.fail()
        self._assert_resources(sut, 24.0, 24.0, 15.0, 30.0, "driving a short distance (without selecting the mode)")

    def test03_drive_battery_explicit(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_combustion()
            sut.switch_to_electric()
            sut.drive(100.0)
        except:
            m = "Unexpected error when driving a HybridCar for a short distance in electric mode."
            self.hint(m)
            self.fail()
        self._assert_resources(sut, 24.0, 24.0, 15.0, 30.0, "driving a short distance in electric mode")

    def test04_drive_combustion(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_combustion()
            sut.drive(100.0)
        except:
            m = "Unexpected error when driving a HybridCar for a short distance in combustion mode."
            self.hint(m)
            self.fail()
        self._assert_resources(sut, 16.0, 24.0, 30.0, 30.0, "driving a short distance in combustion mode")

    def test05_drive_auto_switch_to_combustion(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_electric()
            sut.drive(250.0)
        except:
            m = "Unexpected error when driving a HybridCar for a distance on electric that requires a switch to combustion."
            self.hint(m)
            self.fail()
        m = "driving a distance on electric that requires a switch to combustion"
        self._assert_resources(sut, 20.0, 24.0, 0.0, 30.0, m)

    def test06_drive_auto_switch_to_battery(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_combustion()
            sut.drive(350.0)
        except:
            m = "Unexpected error when driving a HybridCar for a distance on combustion that requires a switch to electric."
            self.hint(m)
            self.fail()
        m = "driving a distance on combustion that requires a switch to electric"
        self._assert_resources(sut, 0.0, 24.0, 22.5, 30.0, m)

    def test07_drive_error_too_far1_e_c(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_electric()
            sut.drive(250.0)
            sut.drive(250.1)
        except Warning:
            return
        except:
            m = "Unexpected error when fully depleting both battery and gas tank."
            self.hint(m)
            self.fail()
        else:
            m = "Fully depleting both battery and gas tank should raise a Warning."
            self.hint(m)
            self.fail()

    def test08_drive_error_too_far_c_e(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_combustion()
            sut.drive(350.0)
            sut.drive(150.1)
        except Warning:
            return
        except:
            m = "Unexpected error when fully depleting both battery and gas tank."
            self.hint(m)
            self.fail()
        else:
            m = "Fully depleting both battery and gas tank should raise a Warning."
            self.hint(m)
            self.fail()

    def test09_error_drive_too_far_e(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_electric()
            sut.drive(500.1)
        except Warning:
            return
        except:
            m = "Unexpected error when fully depleting both battery and gas tank."
            self.hint(m)
            self.fail()
        else:
            m = "Fully depleting both battery and gas tank should raise a Warning."
            self.hint(m)
            self.fail()

    def test10_error_drive_too_far_c(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_combustion()
            sut.drive(500.1)
        except Warning:
            return
        except:
            m = "Unexpected error when fully depleting both battery and gas tank."
            self.hint(m)
            self.fail()
        else:
            m = "Fully depleting both battery and gas tank should raise a Warning."
            self.hint(m)
            self.fail()

    def test11_error_drive_too_far_depletes_everything(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_combustion()
            sut.drive(500.1)
        except:
            pass
        else:
            self.hint("Depleting the battery does not raise an exception.")
            self.fail()
        try:
            actual_g = sut.get_gas_tank_status()
            actual_b = sut.get_battery_status()
        except:
            self.hint("Failed to get gas tank status or battery status of a HybridCar after depleting all resources.")
            self.fail()
        m = "Driving a HybridCar until all resources are depleted should set the levels of the battery charge and the gas tank to 0."
        self.hint(m)
        self.assertEqual((0, 24), actual_g, m)
        self.hint(m)
        self.assertEqual((0, 30), actual_b, m)

    def test12_error_drive_combustion_wrong_type(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_combustion()
            sut.drive("")
        except Warning:
            return
        except:
            m = "Unexpected error when passing a non-float distance to 'Hybrid.drive'."
            self.hint(m)
            self.fail()
        else:
            m = "Passing a non-float distance to 'Hybrid.drive' should raise a Warning."
            self.hint(m)
            self.fail()

    def test13_error_drive_combustion_too_small(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_combustion()
            sut.drive(-1.0)
        except Warning:
            return
        except:
            m = "Unexpected error when passing a non-positive distance to 'Hybrid.drive'."
            self.hint(m)
            self.fail()
        else:
            m = "Passing a non-positive distance to 'Hybrid.drive' should raise a Warning."
            self.hint(m)
            self.fail()

    def test14_error_drive_electric_wrong_type(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_electric()
            sut.drive("")
        except Warning:
            return
        except:
            m = "Unexpected error when passing a non-float distance to 'Hybrid.drive'."
            self.hint(m)
            self.fail()
        else:
            m = "Passing a non-float distance to 'Hybrid.drive' should raise a Warning."
            self.hint(m)
            self.fail()

    def test15_error_drive_electric_too_small(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_electric()
            sut.drive(-1.0)
        except Warning:
            return
        except:
            m = "Unexpected error when passing a non-positive distance to 'Hybrid.drive'."
            self.hint(m)
            self.fail()
        else:
            m = "Passing a non-positive distance to 'Hybrid.drive' should raise a Warning."
            self.hint(m)
            self.fail()

    def test16_fuel(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_combustion()
            sut.drive(150.0)
            sut.fuel(1.0)
        except:
            m = "Unexpected error when refueling a HybridCar after a short drive in combustion mode."
            self.hint(m)
            self.fail()
        m = "after driving a short distance in combustion mode and refueling"
        self._assert_resources(sut, 13.0, 24.0, 30.0, 30.0, m)

    def test17_fuel_overfill(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_combustion()
            sut.drive(150.0)
            sut.fuel(12.1)
        except Warning:
            return
        except:
            m = "Unexpected error when over-filling the gas tank of a HybridCar after a short drive in combustion mode."
            self.hint(m)
            self.fail()
        else:
            m = "Over-filling the gas tank of a HybridCar after a short drive in combustion mode should raise a Warning."
            self.hint(m)
            self.fail()

    def test18_charge(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_electric()
            sut.drive(150.0)
            sut.charge(1.0)
        except:
            m = "Unexpected error when recharging a HybridCar after a short drive in electric mode."
            self.hint(m)
            self.fail()
        m = "after driving a short distance in electric mode and recharging"
        self._assert_resources(sut, 24.0, 24.0, 8.5, 30.0, m)

    def test19_charge_overcharge(self):
        try:
            sut = implementation.HybridCar(24.0, 8.0, 30.0, 200.0)
            sut.switch_to_electric()
            sut.drive(150.0)
            sut.charge(22.6)
        except Warning:
            return
        except:
            m = "Unexpected error when over-charging the battery of a HybridCar after a short drive in electric mode."
            self.hint(m)
            self.fail()
        else:
            m = "Over-charging the battery of a HybridCar after a short drive in electric mode should raise a Warning."
            self.hint(m)
            self.fail()

    def test20_error_init_gas_max_type(self):
        try:
            implementation.HybridCar("", 8.0, 30.0, 200.0)
        except Warning:
            return
        except:
            m = "Unexpected error initializing a HybridCar with a non-float gas tank capacity."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing a HybridCar with a non-float gas tank capacity should raise a Warning."
            self.hint(m)
            self.fail()

    def test21_error_init_gas_max_value(self):
        try:
            implementation.HybridCar(-1.0, 8.0, 30.0, 200.0)
        except Warning:
            return
        except:
            m = "Unexpected error initializing a HybridCar with a non-positive gas tank capacity."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing a HybridCar with a non-positive gas tank capacity should raise a Warning."
            self.hint(m)
            self.fail()

    def test22_error_init_gas_mileage_type(self):
        try:
            implementation.HybridCar(24.0, "", 30.0, 200.0)
        except Warning:
            return
        except:
            m = "Unexpected error initializing a HybridCar with a non-float gas mileage."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing a HybridCar with a non-float gas mileage should raise a Warning."
            self.hint(m)
            self.fail()

    def test23_error_init_gas_mileage_value(self):
        try:
            implementation.HybridCar(24.0, -1.0, 30.0, 200.0)
        except Warning:
            return
        except:
            m = "Unexpected error initializing a HybridCar with a non-positive gas mileage."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing a HybridCar with a non-positive gas mileage should raise a Warning."
            self.hint(m)
            self.fail()

    def test24_error_init_battery_capacity_type(self):
        try:
            implementation.HybridCar(24.0, 8.0, "", 200.0)
        except Warning:
            return
        except:
            m = "Unexpected error initializing a HybridCar with a non-float battery capacity."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing a HybridCar with a non-float battery capacity should raise a Warning."
            self.hint(m)
            self.fail()

    def test25_error_init_battery_capacity_value(self):
        try:
            implementation.HybridCar(24.0, 8.0, -1.0, 200.0)
        except Warning:
            return
        except:
            m = "Unexpected error initializing a HybridCar with a non-positive battery capacity."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing a HybridCar with a non-positive battery capacity should raise a Warning."
            self.hint(m)
            self.fail()

    def test26_error_init_battery_range_type(self):
        try:
            implementation.HybridCar(24.0, 8.0, 30.0, "")
        except Warning:
            return
        except:
            m = "Unexpected error initializing a HybridCar with a non-float battery range."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing a HybridCar with a non-float battery range should raise a Warning."
            self.hint(m)
            self.fail()

    def test27_error_init_battery_range_value(self):
        try:
            implementation.HybridCar(24.0, 8.0, 30.0, -1.0)
        except Warning:
            return
        except:
            m = "Unexpected error initializing a HybridCar with a non-float battery capacity."
            self.hint(m)
            self.fail()
        else:
            m = "Initializing a HybridCar with a non-float battery capacity should raise a Warning."
            self.hint(m)
            self.fail()
