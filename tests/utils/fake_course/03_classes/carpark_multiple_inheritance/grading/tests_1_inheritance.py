#!/usr/bin/env python3

import sys
import ast
from abc import ABC

try:
    from universal.harness import *
except:
    sys.path.append("../../universal/")
    from harness import *

car_implementation = grading_import("task", "car")
combustion_car_implementation = grading_import("task", "combustion_car")
electric_car_implementation = grading_import("task", "electric_car")
hybrid_car_implementation = grading_import("task", "hybrid_car")

ANNO = "abstractmethod"

class TestInheritance(AccessTestCase):

    def test_car(self):
        try:
            class TestCar(car_implementation.Car):
                def get_remaining_range(self): pass
                def drive(self): pass
            sut = TestCar()
        except:
            m = "Anonymous subclass of Car cannot be instantiated."
            self.hint(m)
            self.fail()
        self.hint("Car does not extend ABC.")
        self.assertIsInstance(sut, ABC)

    def test_electric_car(self):
        try:
            sut = electric_car_implementation.ElectricCar(1.0, 2.0)
        except:
            m = "ElectricCar cannot be instantiated."
            self.hint(m)
            self.fail()
        self.hint("ElectricCar does not extend Car.")
        self.assertIsInstance(sut, car_implementation.Car)

    def test_combustion_car(self):
        try:
            sut = combustion_car_implementation.CombustionCar(1.0, 2.0)
        except:
            m = "CombustionCar cannot be instantiated."
            self.hint(m)
            self.fail()
        self.hint("CombustionCar does not extend Car.")
        self.assertIsInstance(sut, car_implementation.Car)

    def test_hybrid_car(self):
        try:
            sut = hybrid_car_implementation.HybridCar(1.0, 2.0, 3.0, 4.0)
        except:
            m = "HybridCar cannot be instantiated."
            self.hint(m)
            self.fail()
        self.hint("HybridCar does not extend Car.")
        self.assertIsInstance(sut, car_implementation.Car)
        self.hint("HybridCar does not extend ElectricCar.")
        self.assertIsInstance(sut, electric_car_implementation.ElectricCar)
        self.hint("HybridCar does not extend CombustionCar.")
        self.assertIsInstance(sut, combustion_car_implementation.CombustionCar)

    def test_for_abstract_method_annotations(self):
        with open("task/car.py") as f:
            tree = ast.parse(f.read())

            #print(ast.dump(tree))

            v = ABCTestVisitor()
            v.visit(tree)

            for name in ["drive", "get_remaining_range"]:
                if name not in v.annotated_methods:
                    m = "The method '{}' lacks the required annotation '{}'.".format(name, ANNO)
                    self.hint(m)
                    self.fail()


class ABCTestVisitor(ast.NodeVisitor):

    def __init__(self):
        self.annotated_methods = []

    def visit_FunctionDef(self, node):
        for d in node.decorator_list:
            if d.id == ANNO:
                self.annotated_methods.append(node.name)



