# -*- coding: utf-8 -*-

import numpy as np
from itertools import chain
from math import ceil
from copy import copy
from librosa import to_mono
from librosa.effects import time_stretch, pitch_shift
from .base import _Base
from .internals import _Validator

__all__ = [
    'Transform', 'Identity',
    'GaussianWhiteNoise',
    'TimeStretch', 'PitchShift',
    'EdgeCrop', 'RandomCrop',
    'LinearFade',
    'Normalize', 'PreEmphasize', 'ExtractLoudestSection',
    'MedianFilter',
    'Reverb', 'ClipDistort'
]

class Transform(_Base):
    """Base class representing a single transformation or augmentation.

    .. note::
        As this is a base class, it should **not** be directly instantiated.

        You can however, use it to `create your own transformations <https://nbviewer.jupyter.org/github/eonu/sigment/blob/master/notebooks/Custom%20Transformations.ipynb>`_, following the
        implementation of the pre-defined transformations in Sigment.

    Parameters
    ----------
    p: float [0 ≤ p ≤ 1]
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

    def __call__(self, X, sr=None):
        """Runs the transformation on a provided input signal.

        Parameters
        ----------
        X: numpy.ndarray [shape (T,) or (1xT) for mono, (2xT) for stereo]
            The input signal to transform.

        sr: int [sr > 0], optional
            The sample rate for the input signal.

            .. note::
                Not required if using transformations that **do not** require a sample rate.

        Returns
        -------
        transformed: numpy.ndarray [shape (T,) for mono, (2xT) for stereo]
            The transformed signal, clipped so that it fits into the :math:`[-1,1]` range required for 32-bit floating point WAVs.

            .. note::
                If a mono signal `X` of shape `(1xT)` was used, the output is reshaped to `(T,)`.

        Examples
        --------
        >>> import numpy as np
        >>> from sigment.transforms import PitchShift
        >>> # Create an example stereo signal.
        >>> X = np.array([
        >>>     [0.325, 0.53 , 0.393, 0.211],
        >>>     [0.21 , 0.834, 0.022, 0.38 ]
        >>> ])
        >>> # Create the pitch-shifting transformation object.
        >>> shift = PitchShift(n_steps=(-1., 1.))
        >>> # Run the __call__ method on the transformation object to transform X.
        >>> # NOTE: Pitch shifting requires a sample rate when called.
        >>> X_shift = shift(X, sr=10)
        """
        return self._flatten(self._transform(copy(X), sr) if self._apply() else copy(X)).clip(min=-1., max=1.)

    def generate(self, X, n, sr=None):
        """Runs the transformation on a provided input signal, producing multiple augmented copies of the input signal.

        Parameters
        ----------
        X: numpy.ndarray [shape (T,) or (1xT) for mono, (2xT) for stereo]
            The input signal to transform.

        n: int [n > 0]
            Number of augmented copies of `X` to generate.

        sr: int [sr > 0], optional
            The sample rate for the input signal.

            .. note::
                Not required if using transformations that **do not** require a sample rate.

        Returns
        -------
        augmented: List[numpy.ndarray] or numpy.ndarray
            The augmented copies (or copy if `n=1`) of the signal `X`, clipped so that they fit into the :math:`[-1,1]` range required for 32-bit floating point WAVs.

            .. note::
                If a mono signal `X` of shape `(1xT)` was used, the output is reshaped to `(T,)`.

        Examples
        --------
        >>> import numpy as np
        >>> from sigment.transforms import GaussianWhiteNoise
        >>> # Create an example stereo signal.
        >>> X = np.array([
        >>>     [0.325, 0.53 , 0.393, 0.211],
        >>>     [0.21 , 0.834, 0.022, 0.38 ]
        >>> ])
        >>> # Create the Gaussian white noise transformation object.
        >>> add_noise = GaussianWhiteNoise(scale=(0.05, 0.15))
        >>> # Generate 5 augmented versions of X, using the noise transformation.
        >>> Xs_noisy = add_noise.generate(X, n=5)
        """
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
    """Applies an identity transformation to a signal.

    Notes
    -----
    - A sampling rate **is not** required when applying this transformation.
    """

    def __init__(self):
        super().__init__(p=1., random_state=None)

    def __call__(self, X, sr=None):
        return self._flatten(self._val.signal(copy(X)))

class GaussianWhiteNoise(Transform):
    """Applies additive Gaussian white noise to the signal.

    Parameters
    ----------
    scale: float [scale > 0] or (float, float)
        | Amount to scale the value sampled from the standard normal distribution.
        | Essentially the variance :math:`\sigma^2`.

    Notes
    -----
    - A sampling rate **is not** required when applying this transformation.
    """

    def __init__(self, scale, p=1., random_state=None):
        super().__init__(p, random_state)
        self.scale = self._val.float_value(
            scale, 'scale (scale parameter)',
            lambda a, b: 0. < a <= b, 'positive')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        scale = self.random_state.uniform(*self.scale)

        # Generate the additive Gaussian white signal noise
        noise = self.random_state.normal(loc=0, scale=scale, size=X.shape)

        # Return the signal with added noise
        return X + noise

class TimeStretch(Transform):
    """Stretches the duration or speed of the signal without affecting its pitch.

    Parameters
    ----------
    rate: float [rate > 0] or (float, float)
        Stretch rate.

        - If `rate < 1`, the signal is slowed down.
        - If `rate > 1`, the signal is sped up.

    Notes
    -----
    - A sampling rate **is not** required when applying this transformation.
    """

    def __init__(self, rate, p=1., random_state=None):
        super().__init__(p, random_state)
        self.rate = self._val.float_value(
            rate, 'rate (stretch rate)',
            lambda a, b: 0. < a <= b, 'positive')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        rate = self.random_state.uniform(*self.rate)

        # Return the signal with time stretching applied to each channel independently
        return np.apply_along_axis(time_stretch, 1, np.asfortranarray(X.T).T, rate=rate)

class PitchShift(Transform):
    """Shifts the pitch of the signal without changing its duration or speed.

    Parameters
    ----------
    n_steps: float [-12 ≤ n_steps ≤ 12] or (float, float)
        Number of semitones to shift.

    Notes
    -----
    - A sampling rate **is** required when applying this transformation.
    """

    def __init__(self, n_steps, p=1., random_state=None):
        super().__init__(p, random_state)
        self.n_steps = self._val.float_value(
            n_steps, 'n_steps (number of semitones to shift)',
            lambda a, b: -12. <= a <= b <= 12., 'between -12 and 12')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        sr = self._val.restricted_integer(
            sr, 'sr (sample rate)',
            lambda x: x > 0, 'positive')
        n_steps = self.random_state.uniform(*self.n_steps)

        # Return the signal with pitch shifting applied to each channel independently
        return np.apply_along_axis(pitch_shift, 1, np.asfortranarray(X.T).T, sr=sr, n_steps=n_steps)

class EdgeCrop(Transform):
    """Crops a section from the start or end of the signal.

    Parameters
    ----------
    side: {'start', 'end'}
        The side of the signal to crop.

    crop_size: float [0 < crop_size ≤ 0.5] or (float, float)
        The fraction of the signal duration to crop from the chosen `side`.

    Notes
    -----
    - A sampling rate **is not** required when applying this transformation.
    """

    def __init__(self, side, crop_size, p=1., random_state=None):
        super().__init__(p, random_state)
        self.side = self._val.one_of(
            side, 'side (side to crop)',
            ['start', 'end'])
        self.crop_size = self._val.float_value(
            crop_size, 'crop_size (fraction of signal duration)',
            lambda a, b: 0. < a <= b <= 0.5, 'between zero and a half')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        crop_size = self.random_state.uniform(*self.crop_size)

        # Calculate the number of frames to crop
        crop_frames = int(crop_size * X.shape[1])

        # Remove the frames from the start or end of the signal
        return X[:, crop_frames:] if self.side == 'start' else X[:, :-crop_frames]

class RandomCrop(Transform):
    """Randomly crops multiple sections from the signal.

    Parameters
    ----------
    crop_size: float [0 < crop_size < 1] or (float, float)
        The fraction of the signal duration to crop.

    n_crops: int [n_crops > 0] or (int, int)
        The number of random crops of size `crop_size` to make.

    Notes
    -----
    - Chunking is done according to the algorithm defined at [1]_.
    - `crop_size` :math:`\\times` `n_crops` must not exceed 1.
    - A sampling rate **is not** required when applying this transformation.

    References
    ----------
    .. [1]  https://stackoverflow.com/a/49944026
    """

    def __init__(self, crop_size, n_crops, p=1., random_state=None):
        super().__init__(p, random_state)
        self.crop_size = self._val.float_value(
            crop_size, 'crop_size (fraction of signal duration)',
            lambda a, b: 0. < a <= b < 1., 'between zero and one')
        self.n_crops = self._val.integer_value(
            n_crops, 'n_crops (number of crops)',
            lambda a, b: b >= a > 0, 'positive')
        if self.crop_size[1] * self.n_crops[1] >= 1.:
            raise ValueError('Expected maximum possible crop_size * n_crops to be less than one')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        n_crops = self.random_state.randint(self.n_crops[0], self.n_crops[1] + 1)

        # Convert crop_size fraction to number of frames
        length = X.shape[1]
        lower_crop_size, upper_crop_size = int(self.crop_size[0] * length), int(self.crop_size[1] * length)

        # Get at least enough random chunk sizes in the specified range (i.e. lower <= n <= upper)
        ns = self.random_state.randint(lower_crop_size, upper_crop_size + 1, size=length//lower_crop_size)
        # Add up the chunk sizes to get the indices at which we'll slice up the input array
        idxs = np.add.accumulate(ns)
        # Truncate idxs so that its contents are all valid indices with respect to signal
        idxs = idxs[:np.searchsorted(idxs, length)]
        # Retrieve chunks from the signal using idxs
        chunks = [X[:, start:end] for start, end in zip(chain([None], idxs), chain(idxs, [None]))]

        # Return signal with chunks removed
        remove_idxs = self.random_state.choice(range(len(chunks)), n_crops, replace=False)
        return np.hstack([c for i, c in enumerate(chunks) if i not in remove_idxs])

class LinearFade(Transform):
    """Linearly fades the signal in or out.

    Parameters
    ----------
    direction: {'in', 'out'}
        The direction to fade the signal.

    fade_size: float [0 < fade_size ≤ 0.5] or (float, float)
        The fraction of the signal to fade in the chosen `direction`.

    Notes
    -----
    - A sampling rate **is not** required when applying this transformation.
    """

    def __init__(self, direction, fade_size, p=1., random_state=None):
        super().__init__(p, random_state)
        self.direction = self._val.one_of(
            direction, 'direction (direction to fade)',
            ['in', 'out'])
        self.fade_size = self._val.float_value(
            fade_size, 'fade_size (fraction of signal duration)',
            lambda a, b: 0. < a <= b <= 0.5, 'between zero and a half')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        fade_size = self.random_state.uniform(*self.fade_size)

        # Calculate the number of frames to fade
        fade_frames = int(fade_size * X.shape[1])
        # Generate scalars for fading
        scalars = np.arange(1, fade_frames + 1).reshape(1, -1) / float(fade_frames)
        # Fade the signal from the start or end with the scalars
        if self.direction == 'in':
            X[:, :fade_frames] *= scalars
        else:
            X[:, -fade_frames:] *= np.flip(scalars)

        # Return the faded signal
        return X

class Normalize(Transform):
    """Normalizes the signal by dividing each sample by the maximum absolute sample amplitude.

    Parameters
    ----------
    independent: bool
        Whether or not to normalize each channel independently.

    Notes
    -----
    - A sampling rate **is not** required when applying this transformation.
    """

    def __init__(self, independent=True, p=1., random_state=None):
        super().__init__(p, random_state)
        self.independent = self._val.boolean(
            independent, 'independent (whether to independently normalize channels)')

    def _transform(self, X, sr):
        X = self._val.signal(X)

        # Return the normalized signal (treat each channel separately if independent=True)
        return X / (np.max(np.abs(X), axis=1, keepdims=True) if self.independent else np.max(np.abs(X)))

class PreEmphasize(Transform):
    """Pre-emphasizes the signal by applying a first-order high-pass filter.

    .. math::
      x'[t] = \\begin{cases}
        x[t] & \\text{if $t=0$} \\\\
        x[t] - \\alpha x[t-1] & \\text{otherwise}
      \\end{cases}

    Parameters
    ----------
    alpha: float [0 < alpha ≤ 1] or (float, float)
        Pre-emphasis coefficient.

    Notes
    -----
    - A sampling rate **is not** required when applying this transformation.
    """

    def __init__(self, alpha=0.95, p=1., random_state=None):
        super().__init__(p, random_state)
        self.alpha = self._val.float_value(
            alpha, 'alpha (pre-emphasis coefficient)',
            lambda a, b: 0. < a <= b <= 1., 'between zero and one')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        alpha = self.random_state.uniform(*self.alpha)

        # Return the pre-emphasized signal
        return np.append(X[:, 0][:, None], X[:, 1:] - alpha * X[:, :-1], axis=1)

class ExtractLoudestSection(Transform):
    """Extracts the loudest section from the signal using sliding window aggregation over amplitudes.

    Parameters
    ----------
    duration: float [0 < duration ≤ 1] or (float, float)
        The duration of the section to extract, as a fraction of the original signal duration.

    Notes
    -----
    - See [2]_ for more details on the implementation.
    - A sampling rate **is not** required when applying this transformation.

    References
    ----------
    .. [2] https://github.com/petewarden/extract_loudest_section
    """

    def __init__(self, duration, p=1., random_state=None):
        super().__init__(p, random_state)
        self.duration = self._val.float_value(
            duration, 'duration (fraction of signal duration)',
            lambda a, b: 0. < a <= b <= 1., 'between zero and one')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        duration = self.random_state.uniform(*self.duration)

        # Convert stereo signals to mono and take the absolute value
        mono_amp = np.abs(to_mono(X))
        # Calculate the length of the section in terms of frames
        total_frames = len(mono_amp)
        frames = ceil(total_frames * duration)
        # Initialize variables for keeping track of loudest section
        previous_amp, section_amp = None, 0
        start, end = 0, frames
        loudest_amp, loudest_idx = -1, (start, end)

        # Slide the moving section window
        while end < total_frames:
            # Calculate volume for current section
            section_amp += mono_amp[start:end].sum() if previous_amp is None else mono_amp[end] - previous_amp
            # Update loudest section indices if current section is loudest
            if section_amp > loudest_amp:
                loudest_amp, loudest_idx = section_amp, (start, end)
            # Store volume of the frame leaving the moving window
            previous_amp = mono_amp[start]
            # Update section indices
            start, end = start + 1, end + 1

        # Return section of the original signal which was the loudest
        return X[:, loudest_idx[0]:loudest_idx[1]]

class MedianFilter(Transform):
    """Applies a median filter to the signal.

    .. math::
      x'[t] = \\mathrm{median}
      \\underbrace{\\Big[
        \\ldots, x[t-1], x[t], x[t+1], \\ldots
      \\Big]}_\\text{window size}

    Parameters
    ----------
    window_size: int [window_size > 1] or (int, int)
        The size of the window of neighbouring samples.

    Notes
    -----
    - A sampling rate **is not** required when applying this transformation.
    """

    def __init__(self, window_size, p=1., random_state=None):
        super().__init__(p, random_state)
        self.window_size = self._val.integer_value(
            window_size, 'window_size (filter window size)',
            lambda a, b: 0 < a <= b, 'positive')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        window_size = self.random_state.randint(self.window_size[0], self.window_size[1] + 1)

        # Create array to store filtered samples
        filtered = np.zeros(X.shape)
        # Calculate number of elements to the right and left
        right = window_size // 2
        left = (window_size - 1) - right
        # Slide the moving window and store filtered samples
        for i in range(X.shape[1]):
            l, m, r = X[:, ((i - left) * (left < i)):i], X[:, i][:, None], X[:, (i + 1):(i + 1 + right)]
            filtered[:, i] = np.median(np.hstack((l, m, r)), axis=1)

        # Return the filtered signal
        return filtered

class Reverb(Transform):
    """Applies reverb to the signal.

    Parameters
    ----------
    delay: float [0 < delay ≤ 1] or (float, float)
        Fraction of signal diration to delay reverberated samples by.

    decay: float [0 < decay ≤ 1] or (float, float)
        Scalar to decay reverberated samples by.

    Notes
    -----
    - See [3]_ for more details on the implementation.

    References
    ----------
    .. [3] https://stackoverflow.com/a/1117249
    """

    def __init__(self, delay, decay, p=1., random_state=None):
        super().__init__(p, random_state)
        self.delay = self._val.float_value(
            delay, 'delay (fraction of signal duration)',
            lambda a, b: 0. < a <= b <= 1., 'between zero and one')
        self.decay = self._val.float_value(
            decay, 'decay (scalar to decay samples by)',
            lambda a, b: 0. < a <= b <= 1., 'between zero and one')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        delay = self.random_state.uniform(*self.delay)
        decay = self.random_state.uniform(*self.decay)

        # Calculate the number of frames to delay
        C, T = X.shape
        delay_frames = int(delay * T)

        # Decay and delay the signal
        out = np.zeros((C, T))
        for t in range(T):
            out[:, t] += X[:, t]
            if t < T - delay_frames:
                out[:, t + delay_frames] += X[:, t] * decay

        # Return the reverberated signal
        return out

class ClipDistort(Transform):
    """Applies clipping distortion to the signal according to a percentile clipping threshold.

    Parameters
    ----------
    percentile: int [0 < percentile ≤ 100]
        Percentile of sample amplitudes to use as a clipping threshold.

    independent: boolean
        Whether or not to independently distort channels by calculating individual percentiles.
    """

    def __init__(self, percentile, independent=False, p=1., random_state=None):
        super().__init__(p, random_state)
        self.percentile = self._val.integer_value(
            percentile, 'percentile (clipping threshold)',
            lambda a, b: 0 < a <= b <= 100, 'between zero and 100')
        self.independent = self._val.boolean(
            independent, 'independent (whether to independently distort channels)')

    def _transform(self, X, sr):
        X = self._val.signal(X)
        percentile = self.random_state.randint(self.percentile[0], self.percentile[1] + 1)

        # Return the distorted signal by clipping at the percentile threshold
        clip = lambda signal, percentile: signal.clip(max=np.percentile(signal, percentile))
        return np.apply_along_axis(clip, 1, X, percentile) if self.independent else clip(X, percentile)