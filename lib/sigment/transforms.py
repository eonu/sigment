# -*- coding: utf-8 -*-

from math import ceil
from copy import copy
import numpy as np
from librosa.effects import time_stretch, pitch_shift
from .base import _Base
from .internals import _Validator, flatten, choice

__all__ = [
    'Transform', 'Identity',
    'UniformWhiteNoise', 'GaussianWhiteNoise', 'LaplacianWhiteNoise',
    'TimeStretch', 'PitchShift',
    'EdgeCrop', 'Fade'
]

class Transform(_Base):
    """Base class representing a single transformation or augmentation.

    .. note::
        As this is a base class, it should **not** be directly instantiated.

        You can however, use it to create your own transformations, following the
        implementation of the pre-defined transformations in Sigment.

    Parameters
    ----------
    p: float [0 <= p <= 1]
        The probability of executing the transformation.

    random_state: numpy.RandomState, int, optional
        A random state object or seed for reproducible randomness.
    """

    def __init__(self, p, random_state):
        if self.__class__ == Transform:
            raise NotImplementedError('Transform is a base class for creating augmentations as a subclass - ' \
                'you cannot directly instantiate it')
        self._val = _Validator()
        self.p = self._val.restricted_float(
            p, 'p (probability)',
            lambda x: 0. <= x <= 1., 'between zero and one')
        self.random_state = self._val.random_state(random_state)

    """Runs the transformation on a provided input signal.

    Parameters
    ----------
    X: numpy.ndarray [shape (T,) or (Tx1) for mono, (Tx2) for stereo]
        The input signal to transform.

    sr: int, optional
        The sample rate for the input signal.

        .. note::
            Not required if the transformation does not rely on `sr`.

    Returns
    -------
    transformed: numpy.ndarray [shape (T,) for mono, (Tx2) for stereo]
        The transformed signal.

        .. note::
            If a mono signal `X` of shape `(Tx1)` was used, the output is reshaped to `(T,)`.
    """
    def __call__(self, X, sr=None):
        return flatten(self._transform(copy(X), sr) if choice(self.random_state, self.p) else copy(X))

    """Runs the transformation on a provided input signal, producing multiple augmented copies of the input signal.

    Parameters
    ----------
    X: numpy.ndarray [shape (T,) or (Tx1) for mono, (Tx2) for stereo]
        The input signal to transform.

    n: int [n > 0]
        Number of augmented copies of `X` to generate.

    sr: int, optional
        The sample rate for the input signal.

        .. note::
            Not required if not using transformations that require a sample rate.

    Returns
    -------
    augmented: List[numpy.ndarray] or numpy.ndarray
        The augmented copies (or copy if `n=1`) of the signal `X`.

        .. note::
            If a mono signal `X` of shape `(Tx1)` was used, the output is reshaped to `(T,)`.
    """
    def generate(self, X, n, sr=None):
        X = self._val.signal(X)
        n = self._val.restricted_integer(
            n, 'n (number of augmented copies)',
            lambda x: x > 0, 'positive')
        sr = sr if sr is None else self._val.restricted_integer(
            sr, 'sr (sample rate)',
            lambda x: x > 0, 'positive')
        X = [self.__call__(X, sr) for _ in range(n)]
        return X[0] if n == 1 else X

    def _transform(self, X, sr):
        raise NotImplementedError

    def __repr__(self, indent=4, level=0):
        module = self.__class__.__module__
        attrs = [(k, v) for k, v in self.__dict__.items() if
            k not in ['p', 'random_state'] and not k.startswith('_')]
        return (' ' * indent * level) + '{}{}({}{})'.format(
            '' if module == '__main__' else '{}.'.format(module),
            self.__class__.__name__,
            '' if len(attrs) == 0 else (', '.join('{}={}'.format(k, v) for k, v in attrs) + ', '),
            'p={}'.format(self.p)
        )

class Identity(Transform):
    """TODO"""

    def __init__(self):
        super().__init__(p=1., random_state=None)

    def __call__(self, X, sr=None):
        return flatten(self._val.signal(copy(X)))

class UniformWhiteNoise(Transform):
    """TODO"""

    def __init__(self, upper, p=1., random_state=None):
        super().__init__(p, random_state)
        self.upper = self._val.float_value(
            upper, 'upper (uniform distribution upper parameter)',
            lambda x1, x2: x2 >= x1 > 0., 'positive')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        upper = self.random_state.uniform(*self.upper)
        noise = self.random_state.uniform(low=0, high=upper, size=X.shape)
        return X + noise

class GaussianWhiteNoise(Transform):
    """TODO"""

    def __init__(self, scale, p=1., random_state=None):
        super().__init__(p, random_state)
        self.scale = self._val.float_value(
            scale, 'scale (scale parameter)',
            lambda x1, x2: x2 >= x1 > 0., 'positive')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        scale = self.random_state.uniform(*self.scale)
        noise = self.random_state.normal(loc=0, scale=scale, size=X.shape)
        return X + noise

class LaplacianWhiteNoise(Transform):
    """TODO"""

    def __init__(self, scale, p=1., random_state=None):
        super().__init__(p, random_state)
        self.scale = self._val.float_value(
            scale, 'scale (scale parameter)',
            lambda x1, x2: x2 >= x1 > 0., 'positive')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        scale = self.random_state.uniform(*self.scale)
        noise = self.random_state.laplace(loc=0, scale=scale, size=X.shape)
        return X + noise

class TimeStretch(Transform):
    """TODO"""

    def __init__(self, rate, p=1., random_state=None):
        super().__init__(p, random_state)
        self.rate = self._val.float_value(
            rate, 'rate (stretch rate)',
            lambda x1, x2: x2 >= x1 > 0., 'positive')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        rate = self.random_state.uniform(*self.rate)
        return np.apply_along_axis(time_stretch, 0, np.asfortranarray(X), rate=rate)

class PitchShift(Transform):
    """TODO"""

    def __init__(self, n_steps, p=1., random_state=None):
        super().__init__(p, random_state)
        self.n_steps = self._val.float_value(
            n_steps, 'n_steps (number of semitones to shift)',
            lambda x1, x2: -12. <= x1 <= x2 <= 12., 'between -12 and 12')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        sr = self._val.restricted_integer(
            sr, 'sr (sample rate)',
            lambda x: x > 0, 'positive')
        n_steps = self.random_state.uniform(*self.n_steps)
        return np.apply_along_axis(pitch_shift, 0, np.asfortranarray(X), sr=sr, n_steps=n_steps)

class EdgeCrop(Transform):
    """TODO"""

    def __init__(self, side, crop_size, p=1., random_state=None):
        super().__init__(p, random_state)
        self.side = self._val.one_of(
            side, 'side (side to crop)',
            ['start', 'end'])
        self.crop_size = self._val.float_value(
            crop_size, 'crop_size (fraction of signal duration)',
            lambda x1, x2: 0. < x1 <= x2 <= 0.5, 'between zero and a half')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        crop_size = self.random_state.uniform(*self.crop_size)
        crop_frames = ceil(crop_size * len(X))
        return X[crop_frames:] if self.side == 'start' else X[:-crop_frames]

class Fade(Transform):
    """TODO"""

    def __init__(self, direction, fade_size, p=1., random_state=None):
        super().__init__(p, random_state)
        self.direction = self._val.one_of(
            direction, 'direction (direction to fade)',
            ['in', 'out'])
        self.fade_size = self._val.float_value(
            fade_size, 'fade_size (fraction of signal duration)',
            lambda x1, x2: 0. < x1 <= x2 <= 0.5, 'between zero and a half')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        fade_size = self.random_state.uniform(*self.fade_size)
        fade_frames = ceil(fade_size * len(X))
        scalars = np.arange(1, fade_frames + 1).reshape(-1, 1) / float(fade_frames)
        if self.direction == 'in':
            X[:fade_frames] *= scalars
        elif self.direction == 'out':
            X[-fade_frames:] *= np.flip(scalars)
        return X

# Normalize
# RandomCrop
# MedianFilter