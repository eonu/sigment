# -*- coding: utf-8 -*-

from random import sample
from .sequence import Sequence
from .internals import _Validator, choice

__all__ = ['Sometimes', 'SomeOf', 'OneOf']

class Quantifier(Sequence):
    """Specifies how to execute transformation or quantifier steps.

    .. note::
        As this is a base class, it should **not** be directly instantiated.

    Parameters
    ----------
    steps: List[Transform, Quantifier]
        A collection of transformation or quantifier steps to apply.

    random_order: bool
        Whether or not to randomize the order of execution of `steps`.

    random_state: numpy.RandomState, int, optional
        A random state object or seed for reproducible randomness.
    """
    pass

class Sometimes(Quantifier):
    """Probabilistically applies the provided transformation or quantifier steps.

    Parameters
    ----------
    steps: List[Transform, Quantifier]
        A collection of transformation or quantifier steps to apply.

    p: float [0 <= p <= 1]
        The probability of executing the transformations or quantifiers.

    random_order: bool
        Whether or not to randomize the order of execution of `steps`.

    random_state: numpy.RandomState, int, optional
        A random state object or seed for reproducible randomness.
    """

    def __init__(self, steps, p=0.5, random_order=False, random_state=None):
        super().__init__(steps, random_order, random_state)
        self.p = self._val.restricted_float(
            p, 'p (probability)',
            lambda x: 0. <= x <= 1., 'between zero and one')

    def _generate_steps(self):
        return self.steps if choice(self.random_state, self.p) else []

class SomeOf(Quantifier):
    """TODO"""

    def __init__(self, steps, n, random_order=False, random_state=None):
        super().__init__(steps, random_order, random_state)
        self._val.integer_value(
            n, 'n (number of steps to run)',
            lambda x1, x2: x2 >= x1 > 0, 'positive')
        if n[1] > len(steps):
            raise ValueError('Quantifier upper limit for n (number of steps) cannot exceed the number of available augmentations')
        self.n = n

    def _generate_steps(self):
        n = self.random_state.choice(range(self.n[0], self.n[1] + 1))
        idxs = range(len(self.steps))
        return [self.steps[idx] for idx in sorted(sample(idxs, k=n))]

class OneOf(SomeOf):
    """TODO"""

    def __init__(self, steps, random_order=False, random_state=None):
        super().__init__(steps, (1, 1), random_order, random_state)