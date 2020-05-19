.. _transformations:

.. role:: raw-html(raw)
    :format: html

Transformations
===============

Audio signal transformations in Sigment are represented by classes that can be used to apply
a specific type of transformation to the audio data.

Some example transformation classes include :class:`GaussianWhiteNoise` and :class:`TimeStretch`. A full
list of available transformations and their details and parameters can be found below.

Each of these transformation classes are a subclass of the more generic :class:`Transform` base class,
which provides a basic interface that can also be used to `write custom transformations <https://nbviewer.jupyter.org/github/eonu/sigment/blob/master/notebooks/Custom%20Transformations.ipynb>`_.

Sigment offers a familiar interface for transformations, taking inspiration from popular augmentation libraries
such as `imgaug <https://github.com/aleju/imgaug>`_, `nlpaug <https://github.com/makcedward/nlpaug>`_,
`albumentations <https://github.com/albumentations-team/albumentations>`_ and `audiomentations <https://github.com/iver56/audiomentations>`_.

:raw-html:`<hr/>`

.. contents:: Section contents
    :local:

Available transformations
-------------------------

Identity
^^^^^^^^
.. autoclass:: sigment.transforms.Identity
    :members:

Additive Gaussian White Noise
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: sigment.transforms.GaussianWhiteNoise
    :members:

Time Stretch
^^^^^^^^^^^^
.. autoclass:: sigment.transforms.TimeStretch
    :members:

Pitch Shift
^^^^^^^^^^^
.. autoclass:: sigment.transforms.PitchShift
    :members:

Edge Crop
^^^^^^^^^
.. autoclass:: sigment.transforms.EdgeCrop
    :members:

Random Crop
^^^^^^^^^^^
.. autoclass:: sigment.transforms.RandomCrop
    :members:

Linear Fade In/Out
^^^^^^^^^^^^^^^^^^
.. autoclass:: sigment.transforms.LinearFade
    :members:

Normalize
^^^^^^^^^
.. autoclass:: sigment.transforms.Normalize
    :members:

Pre-Emphasize
^^^^^^^^^^^^^
.. autoclass:: sigment.transforms.PreEmphasize
    :members:

Extract Loudest Section
^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: sigment.transforms.ExtractLoudestSection
    :members:

Median Filter
^^^^^^^^^^^^^
.. autoclass:: sigment.transforms.MedianFilter
    :members:

Reverberate
^^^^^^^^^^^
.. autoclass:: sigment.transforms.Reverb
    :members:

Clipping Distortion
^^^^^^^^^^^^^^^^^^^
.. autoclass:: sigment.transforms.ClipDistort
    :members:

Using transformations
---------------------

Each transformation class comes with a number of methods that can be used to apply the transformation to either a ``numpy.ndarray`` or WAV file.

All transformations accept the `p` and `random_state` parameters, inherited from the :class:`Transform` base class described below.

.. autoclass:: sigment.transforms.Transform
    :members:
    :special-members: __call__
    :inherited-members: