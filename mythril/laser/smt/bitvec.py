"""This module provides classes for an SMT abstraction of bit vectors."""

from typing import Union

import z3

from mythril.laser.smt.bool import Bool
from mythril.laser.smt.expression import Expression


# fmt: off


class BitVec(Expression):
    """A bit vector symbol."""

    def __init__(self, raw, annotations=None):
        """

        :param raw:
        :param annotations:
        """
        super().__init__(raw, annotations)

    def size(self):
        """TODO: documentation

        :return:
        """
        return self.raw.size()

    @property
    def symbolic(self):
        """Returns whether this symbol doesn't have a concrete value.

        :return:
        """
        self.simplify()
        return not isinstance(self.raw, z3.BitVecNumRef)

    @property
    def value(self):
        """Returns the value of this symbol if concrete, otherwise None.

        :return:
        """
        if self.symbolic:
            return None
        assert isinstance(self.raw, z3.BitVecNumRef)
        return self.raw.as_long()

    def __add__(self, other) -> "BitVec":
        """Create an addition expression.

        :param other:
        :return:
        """
        if isinstance(other, int):
            return BitVec(self.raw + other, annotations=self.annotations)

        union = self.annotations + other.annotations
        return BitVec(self.raw + other.raw, annotations=union)

    def __sub__(self, other) -> "BitVec":
        """Create a subtraction expression.

        :param other:
        :return:
        """

        if isinstance(other, int):
            return BitVec(self.raw - other, annotations=self.annotations)

        union = self.annotations + other.annotations
        return BitVec(self.raw - other.raw, annotations=union)

    def __mul__(self, other) -> "BitVec":
        """Create a multiplication expression.

        :param other:
        :return:
        """
        union = self.annotations + other.annotations
        return BitVec(self.raw * other.raw, annotations=union)

    def __truediv__(self, other) -> "BitVec":
        """Create a signed division expression.

        :param other:
        :return:
        """
        union = self.annotations + other.annotations
        return BitVec(self.raw / other.raw, annotations=union)

    def __and__(self, other) -> "BitVec":
        """Create an and expression.

        :param other:
        :return:
        """
        if not isinstance(other, BitVec):
            other = BitVec(z3.BitVecVal(other, 256))
        union = self.annotations + other.annotations
        return BitVec(self.raw & other.raw, annotations=union)

    def __or__(self, other) -> "BitVec":
        """Create an or expression.

        :param other:
        :return:
        """
        union = self.annotations + other.annotations
        return BitVec(self.raw | other.raw, annotations=union)

    def __xor__(self, other) -> "BitVec":
        """Create a xor expression.

        :param other:
        :return:
        """
        union = self.annotations + other.annotations
        return BitVec(self.raw ^ other.raw, annotations=union)

    def __lt__(self, other) -> Bool:
        """Create a signed less than expression.

        :param other:
        :return:
        """
        union = self.annotations + other.annotations
        return Bool(self.raw < other.raw, annotations=union)

    def __gt__(self, other) -> Bool:
        """Create a signed greater than expression.

        :param other:
        :return:
        """
        union = self.annotations + other.annotations
        return Bool(self.raw > other.raw, annotations=union)

    def __eq__(self, other) -> Bool:
        """Create an equality expression.

        :param other:
        :return:
        """
        if not isinstance(other, BitVec):
            return Bool(self.raw == other, annotations=self.annotations)

        union = self.annotations + other.annotations
        return Bool(self.raw == other.raw, annotations=union)

    def __ne__(self, other) -> Bool:
        """Create an inequality expression.

        :param other:
        :return:
        """
        if not isinstance(other, BitVec):
            return Bool(self.raw != other, annotations=self.annotations)

        union = self.annotations + other.annotations
        return Bool(self.raw != other.raw, annotations=union)


def If(a: Bool, b: BitVec, c: BitVec):
    """Create an if-then-else expression.

    :param a:
    :param b:
    :param c:
    :return:
    """
    if not isinstance(a, Expression):
        a = Bool(z3.BoolVal(a))
    if not isinstance(b, Expression):
        b = BitVec(z3.BitVecVal(b, 256))
    if not isinstance(c, Expression):
        c = BitVec(z3.BitVecVal(c, 256))
    union = a.annotations + b.annotations + c.annotations
    return BitVec(z3.If(a.raw, b.raw, c.raw), union)


def UGT(a: BitVec, b: BitVec) -> Bool:
    """Create an unsigned greater than expression.

    :param a:
    :param b:
    :return:
    """
    annotations = a.annotations + b.annotations
    return Bool(z3.UGT(a.raw, b.raw), annotations)


def UGE(a: BitVec, b:BitVec) -> Bool:
    """Create an unsigned greater or equals expression.

    :param a:
    :param b:
    :return:
    """
    annotations = a.annotations + b.annotations
    return Bool(z3.UGE(a.raw, b.raw), annotations)


def ULT(a: BitVec, b: BitVec) -> Bool:
    """Create an unsigned less than expression.

    :param a:
    :param b:
    :return:
    """
    annotations = a.annotations + b.annotations
    return Bool(z3.ULT(a.raw, b.raw), annotations)


def Concat(*args) -> BitVec:
    """Create a concatenation expression.

    :param args:
    :return:
    """

    # The following statement is used if a list is provided as an argument to concat
    if len(args) == 1 and isinstance(args[0], list):
        args = args[0]

    nraw = z3.Concat([a.raw for a in args])
    annotations = []
    for bv in args:
        annotations += bv.annotations
    return BitVec(nraw, annotations)


def Extract(high: int, low: int, bv: BitVec) -> BitVec:
    """Create an extract expression.

    :param high:
    :param low:
    :param bv:
    :return:
    """
    return BitVec(z3.Extract(high, low, bv.raw), annotations=bv.annotations)


def URem(a: BitVec, b: BitVec) -> BitVec:
    """Create an unsigned remainder expression.

    :param a:
    :param b:
    :return:
    """
    union = a.annotations + b.annotations
    return BitVec(z3.URem(a.raw, b.raw), annotations=union)


def SRem(a: BitVec, b: BitVec) -> BitVec:
    """Create a signed remainder expression.

    :param a:
    :param b:
    :return:
    """
    union = a.annotations + b.annotations
    return BitVec(z3.SRem(a.raw, b.raw), annotations=union)


def UDiv(a: BitVec, b: BitVec) -> BitVec:
    """Create an unsigned division expression.

    :param a:
    :param b:
    :return:
    """
    union = a.annotations + b.annotations
    return BitVec(z3.UDiv(a.raw, b.raw), annotations=union)


def Sum(*args) -> BitVec:
    """Create sum expression.

    :return:
    """
    nraw = z3.Sum([a.raw for a in args])
    annotations = []
    for bv in args:
        annotations += bv.annotations
    return BitVec(nraw, annotations)


def BVAddNoOverflow(a: Union[BitVec, int], b: Union[BitVec, int], signed: bool) -> Bool:
    """Creates predicate that verifies that the addition doesn't overflow.

    :param a:
    :param b:
    :param signed:
    :return:
    """
    if not isinstance(a, Expression):
        a = BitVec(z3.BitVecVal(a, 256))
    if not isinstance(b, Expression):
        b = BitVec(z3.BitVecVal(b, 256))
    return Bool(z3.BVAddNoOverflow(a.raw, b.raw, signed))


def BVMulNoOverflow(a: Union[BitVec, int], b: Union[BitVec, int], signed: bool) -> Bool:
    """Creates predicate that verifies that the multiplication doesn't
    overflow.

    :param a:
    :param b:
    :param signed:
    :return:
    """
    if not isinstance(a, Expression):
        a = BitVec(z3.BitVecVal(a, 256))
    if not isinstance(b, Expression):
        b = BitVec(z3.BitVecVal(b, 256))
    return Bool(z3.BVMulNoOverflow(a.raw, b.raw, signed))


def BVSubNoUnderflow(a: Union[BitVec, int], b: Union[BitVec, int], signed: bool) -> Bool:
    """Creates predicate that verifies that the subtraction doesn't overflow.

    :param a:
    :param b:
    :param signed:
    :return:
    """
    if not isinstance(a, Expression):
        a = BitVec(z3.BitVecVal(a, 256))
    if not isinstance(b, Expression):
        b = BitVec(z3.BitVecVal(b, 256))

    return Bool(z3.BVSubNoUnderflow(a.raw, b.raw, signed))
