# -*- coding: utf-8 -*-

from librosa import load
from soundfile import write
from numpy import asfortranarray

class _Base:
    def apply_to_wav(self, source, out=None):
        """Applies the augmentation to the provided input WAV file and writes the resulting signal back to a WAV file.

        .. note::
            The resulting signal is always clipped so that it fits into the :math:`[-1,1]` range required for 32-bit floating point WAVs.

        Parameters
        ----------
        source: str, Path or path-like
            Path to the input WAV file.

        out: str, Path or path-like
            Output WAV path for the augmented signal.

            .. warning:: If `out` is set to ``None`` (which is the default) or the same as `source`, the input WAV file **will** be overwritten!

        Examples
        --------
        >>> from sigment import *
        >>> # Create a transformation or quantifier object.
        >>> transform = ...
        >>> # Apply the transformation to the input WAV file and write it to the output file
        >>> transform.apply_to_wav('in.wav', 'out.wav')
        """
        out = source if out is None else out
        X, sr = load(source, mono=False)
        write(out, data=self.__call__(X, sr).T, samplerate=sr)

    def generate_from_wav(self, source, n=1):
        """Applies the augmentation to the provided input WAV file and returns a ``numpy.ndarray``.

        Parameters
        ----------
        source: str, Path or path-like
            Path to the input WAV file.

        n: int [n > 0]
            Number of augmented versions of the `source` signal to generate.

        Returns
        -------
        augmented: List[numpy.ndarray] or numpy.ndarray
            The augmented versions (or version if `n=1`) of the `source` signal, clipped so that they fit into the :math:`[-1,1]` range required for 32-bit floating point WAVs.

        Examples
        --------
        >>> from sigment import *
        >>> # Create a transformation or quantifier object.
        >>> transform = ...
        >>> # Generate 5 augmented versions of the signal data from 'signal.wav' as numpy.ndarrays.
        >>> transformed = transform.generate_from_wav('signal.wav', n=5)
        """
        X, sr = load(source, mono=False)
        return self.generate(X, n, sr)

    def _apply(self):
        return self.random_state.uniform(size=1).item() < self.p

    def _flatten(self, X):
        return asfortranarray((X.reshape(-1) if any(i == 1 for i in X.shape) else X) if X.ndim == 2 else X)