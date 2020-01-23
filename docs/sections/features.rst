.. _features:

.. role:: raw-html(raw)
    :format: html

Transformations
===============

Describe transformations

.. contents:: Contents
    :local:

.. _Transformations:

Available transformations
-------------------------

+-------------------------------------------------+----------------------------------------------------+
| Transformation                                  | Summary                                            |
+=================================================+====================================================+
| | :raw-html:`<h3>Transform (Base)</h3>`         | A base class representing a single transformation. |
| | ``Transform(**kwargs)``                       |                                                    |
|                                                 +----------------------------------------------------+
|                                                 | | **Main parameters**                              |
|                                                 | | • None                                           |
|                                                 +----------------------------------------------------+
|                                                 | **Requires sample rate?**: No                      |
|                                                 +----------------------------------------------------+
|                                                 | **Notes**: As this is a base class,                |
|                                                 | it should **not** be initialized.                  |
+-------------------------------------------------+----------------------------------------------------+
|                                                                                                      |
+-------------------------------------------------+----------------------------------------------------+
| | :raw-html:`<h3>Identity</h3>`                 | Applies an identity transformation to a signal.    |
| | ``Identity()``                                |                                                    |
|                                                 +----------------------------------------------------+
|                                                 | | **Main parameters**                              |
|                                                 | | • None                                           |
|                                                 +----------------------------------------------------+
|                                                 | **Requires sample rate?**: No                      |
|                                                 +----------------------------------------------------+
|                                                 | **Notes**: None                                    |
+-------------------------------------------------+----------------------------------------------------+
|                                                                                                      |
+-------------------------------------------------+----------------------------------------------------+
| | :raw-html:`<h3>Uniform White Noise</h3>`      | Applies uniform white noise to a signal.           |
| | ``UniformWhiteNoise(upper, **kwargs)``        |                                                    |
|                                                 +----------------------------------------------------+
|                                                 | | **Main parameters**                              |
|                                                 | | • `upper`: ``tuple`` or ``float > 0``            |
|                                                 | |   Upper limit for                                |
|                                                 |   the uniform distribution.                        |
|                                                 +----------------------------------------------------+
|                                                 | **Requires sample rate?**: No                      |
|                                                 +----------------------------------------------------+
|                                                 | **Notes**: None                                    |
+-------------------------------------------------+----------------------------------------------------+
|                                                                                                      |
+-------------------------------------------------+----------------------------------------------------+
| | :raw-html:`<h3>Gaussian White Noise</h3>`     | Applies Gaussian white noise to a signal.          |
| | ``GaussianWhiteNoise(scale, **kwargs)``       |                                                    |
|                                                 +----------------------------------------------------+
|                                                 | | **Main parameters**                              |
|                                                 | | • `scale`: ``tuple`` or ``float > 0``            |
|                                                 | |   Amount to scale the value sampled from the     |
|                                                 |   standard normal distribution.                    |
|                                                 | |   Essentially the variance :math:`\sigma^2`.     |
|                                                 +----------------------------------------------------+
|                                                 | **Requires sample rate?**: No                      |
|                                                 +----------------------------------------------------+
|                                                 | **Notes**: None                                    |
+-------------------------------------------------+----------------------------------------------------+
|                                                                                                      |
+-------------------------------------------------+----------------------------------------------------+
| | :raw-html:`<h3>Laplacian White Noise</h3>`    | Applies Laplacian white noise to a signal.         |
| | ``LaplacianWhiteNoise(scale, **kwargs)``      |                                                    |
|                                                 +----------------------------------------------------+
|                                                 | | **Main parameters**                              |
|                                                 | | • `scale`: ``tuple`` or ``float > 0``            |
|                                                 | |   Scale parameter for the distribution.          |
|                                                 +----------------------------------------------------+
|                                                 | **Requires sample rate?**: No                      |
|                                                 +----------------------------------------------------+
|                                                 | **Notes**: None                                    |
+-------------------------------------------------+----------------------------------------------------+
|                                                                                                      |
+-------------------------------------------------+----------------------------------------------------+
| | :raw-html:`<h3>Time Stretching</h3>`          | Changes the duration or speed of the signal        |
| | ``TimeStretch(rate, **kwargs)``               | without affecting its pitch.                       |
|                                                 +----------------------------------------------------+
|                                                 | | **Main parameters**                              |
|                                                 | | • `rate`: ``tuple`` or ``float > 0``             |
|                                                 | |   Stretch rate.                                  |
|                                                 | |   - If `rate < 1`, the signal is slowed          |
|                                                 |   down.                                            |
|                                                 | |   - If `rate > 1`, the signal is sped up.        |
|                                                 +----------------------------------------------------+
|                                                 | **Requires sample rate?**: No                      |
|                                                 +----------------------------------------------------+
|                                                 | **Notes**: None                                    |
+-------------------------------------------------+----------------------------------------------------+
|                                                                                                      |
+-------------------------------------------------+----------------------------------------------------+
| | :raw-html:`<h3>Pitch Shifting</h3>`           | Changes the pitch of a signal without affecting    |
| | ``PitchShift(n_steps, **kwargs)``             | its speed.                                         |
|                                                 +----------------------------------------------------+
|                                                 | | **Main parameters**                              |
|                                                 | | • `n_steps`: ``tuple`` or ``-12 <= float <= 12`` |
|                                                 | |   Number of semitones to shift.                  |
|                                                 +----------------------------------------------------+
|                                                 | **Requires sample rate?**: Yes                     |
|                                                 +----------------------------------------------------+
|                                                 | **Notes**: None                                    |
+-------------------------------------------------+----------------------------------------------------+
|                                                                                                      |
+-------------------------------------------------+----------------------------------------------------+
| | :raw-html:`<h3>Edge Cropping</h3>`            | Crops the start or end of a signal by some amount. |
| | ``EdgeCrop(side, crop_size, **kwargs)``       |                                                    |
|                                                 +----------------------------------------------------+
|                                                 | | **Main parameters**                              |
|                                                 | | • `side`: ``{'start', 'end'}``                   |
|                                                 | |   The side of the signal to crop.                |
|                                                 | | • `crop_size`: ``0 <= float <= 0.5``             |
|                                                 | |   The fraction of the signal duration to crop    |
|                                                 |   from the chosen ``side``.                        |
|                                                 +----------------------------------------------------+
|                                                 | **Requires sample rate?**: No                      |
|                                                 +----------------------------------------------------+
|                                                 | **Notes**: None                                    |
+-------------------------------------------------+----------------------------------------------------+

Using transformations
---------------------

Each transformation class comes with a number of methods that can be used to apply the transformation to either a ``numpy.ndarray`` or WAV file.

The ``**kwargs`` used in the table above are the `p` and `random_state` parameters of the ``Transform`` base class described below.

.. py:class:: sigment.transforms.Transform([main params], p=1., random_state=None)

    Base class representing a single transformation or augmentation.

    .. note::
        As ``Transform`` is a base class, it should **not** be directly instantiated – use one of the transformation classes listed :ref:`above<Transformations>`.

        You can however, use it to create your own transformations, following the
        implementation of the pre-defined transformations in Sigment.

    :param p: The probability of executing the transformation.
    :type p: :math:`0 \leq` ``float`` :math:`\leq 1`

    :param random_state: A random state object or seed for reproducible randomness.
    :type random_state: ``numpy.RandomState``, ``int`` or ``None``

    .. py:function:: __call__(self, X, sr=None)

        Runs the transformation on a provided input signal.

        :param X: The input signal to transform.
        :type X: ``numpy.ndarray`` :math:`(T,)` or :math:`(T\times1)` for mono, :math:`(T\times2)` for stereo

        :param sr: Sample rate. :raw-html:`<br/>` If the transformation does not depend on a sample rate, this should be ``None`` (which is the default). See the :ref:`transformations table<Transformations>` to determine whether you need a sample rate or not.
        :type sr: ``int`` :math:`> 0` or ``None``

        :return: The transformed signal.
        :rtype: ``numpy.ndarray`` :math:`(T,)` for mono, :math:`(T\times2)` for stereo

        **Example**:

        .. code-block:: python
            :linenos:

            import numpy as np
            from sigment.transforms import PitchShift

            # Create an example stereo signal.
            X = np.array([
                [0.325, 1.21 ],
                [0.53 , 0.834],
                [1.393, 1.022],
                [1.211, 0.38 ]
            ])

            # Create the pitch-shifting transformation object.
            shift = PitchShift(n_steps=(-1., 1.))

            # Run the __call__ method on the transformation object to transform X.
            # NOTE: Pitch shifting requires a sample rate when called.
            X_shift = shift(X, sr=10)

    .. py:function:: generate(self, X, n, sr=None)

        Runs the transformation on a provided input signal, producing multiple augmented copies of the input signal.

        :param X: The input signal to transform.
        :type X: ``numpy.ndarray`` :math:`(T,)` or :math:`(T\times1)` for mono, :math:`(T\times2)` for stereo

        :param n: Number of augmented versions of `X` to generate.
        :type n: ``int`` :math:`> 0`

        :param sr: Sample rate. :raw-html:`<br/>` If the transformation does not depend on a sample rate, this should be ``None`` (which is the default). See the :ref:`transformations table<Transformations>` to determine whether you need a sample rate or not.
        :type sr: ``int`` :math:`> 0` or ``None``

        :return: The augmented versions (or version if `n=1`) of the signal `X`.
        :rtype: ``List[numpy.ndarray]`` or ``numpy.ndarray``

        **Example**:

        .. code-block:: python
            :linenos:

            import numpy as np
            from sigment.transforms import GaussianWhiteNoise

            # Create an example stereo signal.
            X = np.array([
                [0.325, 1.21 ],
                [0.53 , 0.834],
                [1.393, 1.022],
                [1.211, 0.38 ]
            ])

            # Create the Gaussian white noise transformation object.
            add_noise = GaussianWhiteNoise(scale=(0.05, 0.15))

            # Generate 5 augmented versions of X, using the noise transformation.
            Xs_noisy = add_noise.generate(X, n=5)

    .. py:function:: apply_to_wav(self, source, out=None)

        Runs the transformation on a provided input WAV file and writes the resulting signal back to a WAV file.

        .. warning:: If `out` is set to ``None`` (which is the default) or the same as `source`, the input WAV file **will** be overwritten!

        :param source: Path to the input WAV file.
        :type source: ``str``, ``Path`` or *path-like*

        :param out: Output WAV path for the augmented signal.
        :type out: ``str``, ``Path`` or *path-like*

        **Example**:

        .. code-block:: python
            :linenos:

            import numpy as np
            from sigment.transforms import Identity

            # Create the identity transformation object.
            identity = Identity()

            # Apply the transformation to the input WAV file and write it to the output file
            identity.apply_to_wav('in.wav', 'out.wav')

    .. py:function:: generate_from_wav(self, source, n=1)

        Runs the transformation on a provided input WAV file and returns a ``numpy.ndarray``.

        :param source: Path to the input WAV file.
        :type source: ``str``, ``Path`` or *path-like*

        :param n: Number of augmented versions of the `source` signal to generate.
        :type n: ``int`` :math:`> 0`

        :return: The augmented versions (or version if `n=1`) of the `source` signal.
        :rtype: ``List[numpy.ndarray]`` or ``numpy.ndarray``

        **Example**:

        .. code-block:: python
            :linenos:

            import numpy as np
            from sigment.transforms import Fade

            # Create the fade-in transformation object.
            fade_in = Fade(direction='in', fade_size=(0.025, 0.1))

            # Generate 5 augmented versions of the signal data from 'signal.wav' as numpy.ndarrays, using the fade-in transformation.
            Xs_faded = fade_in.generate_from_wav('signal.wav', n=5)