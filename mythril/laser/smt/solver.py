"""This module contains an abstract SMT representation of an SMT solver."""
import z3
from mythril.laser.smt.bool import Bool
from mythril.laser.smt.expression import Expression


class Solver:
    """An SMT solver object."""

    def __init__(self):
        """

        """
        self.raw = z3.Solver()

    def set_timeout(self, timeout: int) -> None:
        """ Sets the timeout that will be used by this solver, timeout is in milliseconds

        :param timeout:
        """
        self.raw.set(timeout=timeout)

    def add(self, constraints: list) -> None:
        """ Adds the constraints to this solver

        :param constraints:
        :return:
        """
        if not isinstance(constraints, list):
            self.raw.add(constraints.raw)
            return
        constraints = [c.raw for c in constraints]
        self.raw.add(constraints)

    def append(self, constraints: list) -> None:
        """ Adds the constraints to this solver

        :param constraints:
        :return:
        """
        if not isinstance(constraints, list):
            self.raw.append(constraints.raw)
            return
        constraints = [c.raw for c in constraints]
        self.raw.add(constraints)

    def check(self):
        """ Returns z3 smt check result

        :return:
        """
        return self.raw.check()

    def model(self):
        """ Returns z3 model for a solution
        :return:
        """
        return self.raw.model()

    def reset(self) -> None:
        """Reset this solver."""
        self.raw.reset()

    def pop(self, num) -> None:
        """ Pop num constraints from this solver

        :param num:
        """
        self.raw.pop(num)


class Optimize(Solver):
    """
    An optimizing smt solver
    """

    def __init__(self):
        """Create a new optimizing solver instance."""
        super().__init__()
        self.raw = z3.Optimize()

    def minimize(self, element: Expression):
        """ In solving this solver will try to minimize the passed expression

        :param element:
        """
        self.raw.minimize(element.raw)

    def maximize(self, element: Expression):
        """ In solving this solver will try to maximize the passed expression

        :param element:
        """
        self.raw.maximize(element.raw)
