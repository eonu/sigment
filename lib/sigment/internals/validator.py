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

        Raises
        ------
        TypeError
            If the value is not an ``int``.

        Examples
        --------
        >>> validator = _Validator()
        >>> n_crops = 3
        >>> validator.integer(n_crops, 'n_crops (number of sections to crop)')
        """
        if not isinstance(item, int):
            raise TypeError("Expected {} to be an integer".format(desc))
        return item

    def real(self, item, desc):
        """Validates a real number.

        Parameters
        ----------
        item: float
            The item to validate.

        desc: str
            A description of the item being validated.

        Returns
        -------
        item: float
            The original input item if valid.

        Raises
        ------
        TypeError
            If the value cannot be converted into a ``float``.

        Examples
        --------
        >>> validator = _Validator()
        >>> var = 5.0
        >>> validator.real(var, 'var (variance)')
        """
        try:
            return float(item)
        except ValueError:
            raise TypeError("Expected {} to be a real number".format(desc))

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

        Raises
        ------
        TypeError
            If the value is not a ``str``.

        Examples
        --------
        >>> validator = _Validator()
        >>> method = 'median'
        >>> method = validator.string(method, 'method (filter type)')
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

        Raises
        ------
        TypeError
            If the value is not ``True`` or ``False``.

        Examples
        --------
        >>> validator = _Validator()
        >>> indep = True
        >>> indep = validator.boolean(indep, 'indep (whether to independently normalize channels)')
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

        items: Iterable[Any]
            The collection of permitted values to check against.

        Returns
        -------
        item: Any
            The original input item if valid.

        Raises
        ------
        ValueError
            If the value is not one of the specified permitted values.

        Examples
        --------
        >>> validator = _Validator()
        >>> method = 'median'
        >>> method = validator.one_of(method, 'method (filter type)', ['median', 'mean'])
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

        Raises
        ------
        ValueError
            If the ``int`` value does not satisfy the provided condition.

        Examples
        --------
        >>> validator = _Validator()
        >>> n_crops = 3
        >>> n_crops = validator.restricted_integer(
        >>>     n_crops, 'n_crops (number of sections to crop)',
        >>>     lambda x: 0 <= x <= 5, 'between zero and five')
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

        Raises
        ------
        ValueError
            If the ``float`` value does not satisfy the provided condition.

        Examples
        --------
        >>> validator = _Validator()
        >>> var = 5.0
        >>> validator.restricted_float(var, 'var (variance)', lambda x: x > 0, 'positive')
        """
        item = self.real(item, desc)
        if not condition(item):
            raise ValueError('Expected {} to be {}'.format(desc, expected))
        else:
            return item

    def integer_value(self, item, desc, condition, expected):
        """Validates an integer value or value range and checks that it satisfies some condition.

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
        item: tuple(int, int)
            The value range if the input item is valid.

        Raises
        ------
        TypeError
            If the value is not a ``int`` or ``(int, int)``.

        ValueError
            If the value is a tuple with more than two elements (sanity check).

        Examples
        --------
        >>> validator = _Validator()
        >>> validator.integer_value(5, 'window_size (window size)', lambda a, b: 0 < a <= b, 'positive')
        >>> #=> (5, 5)
        >>> validator.integer_value((5, 10), 'window_size (window size)', lambda a, b: 0 < a <= b, 'positive')
        >>> #=> (5, 10)
        """
        if isinstance(item, tuple):
            if len(item) == 2:
                self.restricted_integer(item[0], 'lower limit for {}'.format(desc),
                    lambda a: condition(a, a), expected)
                self.restricted_integer(item[1], 'upper limit for {}'.format(desc),
                    lambda b: condition(item[0], b), '{} and greater than or equal to the lower limit'.format(expected))
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
        """Validates a float value or value range and checks that it satisfies some condition.

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
        item: tuple(float, float)
            The value range if the input item is valid.

        Raises
        ------
        TypeError
            If the value is not a ``float`` or ``(float, float)``.

        ValueError
            If the value is a tuple with more than two elements (sanity check).

        Examples
        --------
        >>> validator = _Validator()
        >>> validator.float_value(5.0, 'var (variance)', lambda a, b: 0 < a <= b, 'positive')
        >>> #=> (5.0, 5.0)
        >>> validator.float_value((5, 10), 'var (variance)', lambda a, b: 0 < a <= b, 'positive')
        >>> #=> (5.0, 10.0)
        """
        if isinstance(item, tuple):
            if len(item) == 2:
                self.restricted_float(item[0], 'lower limit for {}'.format(desc),
                    lambda a: condition(a, a), expected)
                self.restricted_float(item[1], 'upper limit for {}'.format(desc),
                    lambda b: condition(item[0], b), '{} and greater than or equal to the lower limit'.format(expected))
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
        """Validates a WAV audio signal.

        Parameters
        ----------
        signal: numpy.ndarray [shape (T,) or (1xT) for mono, (2xT) for stereo]
            The input signal to validate.

        Returns
        -------
        signal: numpy.ndarray [shape (T,) for mono, (2xT) for stereo]
            The original signal if it is valid.

        Raises
        ------
        TypeError
            - If the signal is of the wrong type.
            - If the signal is not a floating point ``numpy.ndarray``.
            - If the signal is a floating point ``numpy.ndarray`` with samples outside :math:`[-1, 1]`.

        ValueError
            - If the signal is a ``numpy.ndarray`` with more than two dimensions.
            - If the signal has more than two channels.
        """
        if isinstance(signal, np.ndarray):
            if any(signal.dtype == np.dtype(type_) for type_ in (np.float16, np.float32, np.float64)):
                if (signal.min() >= -1) and (signal.max() <= 1):
                    if signal.ndim == 1:
                        return signal.reshape(1, -1).astype(np.float32)
                    elif signal.ndim == 2:
                        if any(n_channels in signal.shape for n_channels in (1, 2)):
                            a, b = signal.shape
                            return (signal.T if b in (1, 2) else signal).astype(np.float32)
                        else:
                            raise ValueError('Expected signal to be mono (T,) or stereo (2xT)')
                    else:
                        raise ValueError('Expected signal to be a 1D or 2D numpy.ndarray')
                else:
                    raise TypeError('Expected signal to have samples in range [-1, 1]')
            else:
                raise TypeError('Expected a floating point signal')
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

        Raises
        ------
        TypeError
            If the random state object is of the incorrect type.
        """
        if isinstance(state, int) or (state is None):
            return np.random.RandomState(seed=state)
        elif isinstance(state, np.random.RandomState):
            return state
        else:
            raise TypeError('Expected random state to be of type: None, int, or numpy.random.RandomState')