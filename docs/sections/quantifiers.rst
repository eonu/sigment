.. _quantifiers:

.. role:: raw-html(raw)
    :format: html

Quantifiers
===========

Quantifiers are used to specify rules for how a sequence of transformations
or quantifiers should be applied.

Each quantifier class is a subclass of the more generic :class:`Quantifier` base class,
which provides a basic interface that can also be used to write custom quantifiers,
though there is rarely a need for this.

As with transformations, Sigment offers a familiar interface for quantifiers, taking inspiration from popular augmentation libraries
such as `imgaug <https://github.com/aleju/imgaug>`_ and `nlpaug <https://github.com/makcedward/nlpaug>`_.

:raw-html:`<hr/>`

.. contents:: Section contents
    :local:

Available quantifiers
---------------------

In the below quantifiers, the `steps` argument is a list of :class:`Transform` and/or :class:`Quantifier` objects,
specifying a sequence of transformations or quantifiers to be applied.

Pipeline
^^^^^^^^
.. autoclass:: sigment.quantifiers.Pipeline
    :members:

Sometimes
^^^^^^^^^
.. autoclass:: sigment.quantifiers.Sometimes
    :members:

Some Of
^^^^^^^
.. autoclass:: sigment.quantifiers.SomeOf
    :members:

One Of
^^^^^^
.. autoclass:: sigment.quantifiers.OneOf
    :members:

Using quantifiers
-----------------

Each quantifier class comes with a number of methods that can be used to apply the transformations to either a ``numpy.ndarray`` or WAV file.

All quantifiers accept the `random_order` and `random_state` parameters, inherited from the :class:`Quantifier` base class described below.

.. autoclass:: sigment.quantifiers.Quantifier
    :members:
    :special-members: __call__
    :inherited-members: