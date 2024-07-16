#!/usr/bin/env python3

from grading.tests_1_inheritance import TestInheritance
from grading.tests_2a_combustion_car import TestCombustionCar
from grading.tests_2b_electric_car import TestElectricCar
from grading.tests_2c_hybrid_car import TestHybridCar


import sys

try:
    from universal.harness import *
except:
    sys.path.append("../../universal/")
    from harness import *

TestRunner().run(
    AccessTestSuite(
        4,
        [
            TestInheritance,
            TestCombustionCar,
            TestElectricCar,
            TestHybridCar,
        ],
    )
)
