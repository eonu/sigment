# -*- coding: utf-8 -*-

import numpy as np

class _Validator:
    """Performs internal validations on various input types."""

    def integer(self, item, desc):
        """Validates an integer.

        Parameters
        ----------
        item: int
            The item to validate.

        desc: str
            A description of the item being validated.

        Returns
        -------
        item: int
            The original input item if valid.
        """
        if not isinstance(item, int):
            raise TypeError("Expected {} to be an integer".format(desc))
        return item

    def real(self, item, desc):
        """Validates a real number.

        Parameters
        ----------
        item: int
            The item to validate.

        desc: str
            A description of the item being validated.

        Returns
        -------
        item: int
            The original input item if valid.
        """
        try:
            float(item)
        except ValueError:
            raise TypeError("Expected {} to be a real number".format(desc))
        else:
            return item

    def string(self, item, desc):
        """Validates a string.

        Parameters
        ----------
        item: str
            The item to validate.

        desc: str
            A description of the item being validated.

        Returns
        -------
        item: str
            The original input item if valid.
        """
        if not isinstance(item, str):
            raise TypeError("Expected {} to be a string".format(desc))
        return item

    def boolean(self, item, desc):
        """Validates a boolean.

        Parameters
        ----------
        item: bool
            The item to validate.

        desc: str
            A description of the item being validated.

        Returns
        -------
        item: bool
            The original input item if valid.
        """
        if not isinstance(item, bool):
            raise TypeError("Expected {} to be a boolean".format(desc))
        return item

    def one_of(self, item, desc, items):
        """Validates that an item is one of some permitted values.

        Parameters
        ----------
        item: Any
            The item to validate.

        desc: str
            A description of the item being validated.

        items: List[Any]
            The list of permitted values to check against.

        Returns
        -------
        item: Any
            The original input item if valid.
        """
        if not item in items:
            raise ValueError('Expected {} to be one of {}'.format(desc, items))
        return item

    def restricted_integer(self, item, desc, condition, expected):
        """Validates an integer and checks that it satisfies some condition.

        Parameters
        ----------
        item: int
            The item to validate.

        desc: str
            A description of the item being validated.

        condition: lambda
            A condition to check the item against.

        expected: str
            A description of the condition, or expected value.

        Returns
        -------
        item: int
            The original input item if valid.
        """
        if isinstance(item, int):
            if not condition(item):
                raise ValueError('Expected {} to be {}'.format(desc, expected))
        else:
            raise TypeError("Expected {} to be an integer".format(desc))
        return item

    def restricted_float(self, item, desc, condition, expected):
        """Validates a float and checks that it satisfies some condition.

        Parameters
        ----------
        item: float
            The item to validate.

        desc: str
            A description of the item being validated.

        condition: lambda
            A condition to check the item against.

        expected: str
            A description of the condition, or expected value.

        Returns
        -------
        item: float
            The original input item if valid.
        """
        item = self.real(item, desc)
        if not condition(item):
            raise ValueError('Expected {} to be {}'.format(desc, expected))
        else:
            return item

    def integer_value(self, item, desc, condition, expected):
        if isinstance(item, tuple):
            if len(item) == 2:
                self.restricted_integer(item[0], 'lower limit for {}'.format(desc),
                    lambda x1: condition(x1, x1), expected)
                self.restricted_integer(item[1], 'upper limit for {}'.format(desc),
                    lambda x2: condition(item[0], x2), '{} and greater than or equal to the lower limit'.format(expected))
                return item
            else:
                raise ValueError('Expected range for {} to be a tuple (lower, upper) representing the limits ' \
                    'of the range of values from which the value is drawn'.format(desc, desc))
        elif isinstance(item, int):
            item = self.restricted_integer(item, desc, lambda x: condition(x, x), expected)
            return (item, item)
        else:
            raise TypeError('Expected range for {} to be a tuple (lower, upper) representing the limits ' \
                    'of the range of values from which the value is drawn'.format(desc, desc))

    def float_value(self, item, desc, condition, expected):
        if isinstance(item, tuple):
            if len(item) == 2:
                self.restricted_float(item[0], 'lower limit for {}'.format(desc),
                    lambda x1: condition(x1, x1), expected)
                self.restricted_float(item[1], 'upper limit for {}'.format(desc),
                    lambda x2: condition(item[0], x2), '{} and greater than or equal to the lower limit'.format(expected))
                return item
            else:
                raise ValueError('Expected range for {} to be a tuple (lower, upper) representing the limits ' \
                    'for a uniform distribution from which the value is sampled'.format(desc, desc))
        elif isinstance(item, (int, float)):
            item = self.restricted_float(item, desc, lambda x: condition(x, x), expected)
            return (item, item)
        else:
            raise TypeError('Expected range for {} to be a tuple (lower, upper) representing the limits ' \
                'for a uniform distribution from which the value is sampled'.format(desc, desc))

    def signal(self, signal):
        if isinstance(signal, np.ndarray):
            if signal.ndim in [1, 2]:
                return np.atleast_2d(signal).astype(float)
            else:
                raise ValueError('Expected signal to be a 1D or 2D numpy.ndarray')
        else:
            raise TypeError('Expected signal to be a numpy.ndarray')

    def random_state(self, state):
        """Validates a random state object or seed.

        Parameters
        ----------
        state: None, int, numpy.random.RandomState
            A random state object or seed.

        Returns
        -------
        state: numpy.random.RandomState
            A random state object.
        """
        if isinstance(state, int) or (state is None):
            return np.random.RandomState(seed=state)
        elif isinstance(state, np.random.RandomState):
            return state
        else:
            raise TypeError('Expected random state to be of type: None, int, or numpy.random.RandomState')