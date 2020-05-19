.. Sigment documentation master file, created by
   sphinx-quickstart on Sat Jan 11 13:35:54 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. role:: raw-html(raw)
    :format: html

About
=====

Sigment is an extensible data augmentation package for creating complex transformation pipelines for audio signals.

What is data augmentation?
--------------------------

Data augmentation is the creation of artificial data from original data by typically applying a transformation, or multiple transformations, to the original data. It is a common method for improving the versatility of machine learning models, in addition to providing more training examples for datasets of limited size.

In image data for example, it is common to use horizontal and vertical flipping, random cropping, zooming and additive noise for augmentation. In audio, we can use other transformations such as pitch shifting, time stretching or fading the signal in or out. Some image augmentation methods such as additive noise can also be transferred over to audio data.

Example
-------

From an audio signal like:

.. image:: https://i.ibb.co/jzB9Hr5/original.png
  :alt: Original

Sigment can produce augmentations such as:

.. image:: https://i.ibb.co/tqwvXcc/augmented.png
  :alt: Augmented

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Sigment

   self
   changelog.rst

.. toctree::
    :maxdepth: 2
    :caption: Features

    sections/transformations.rst
    sections/quantifiers.rst
    sections/validations.rst

Documentation Search and Index
==============================

* :ref:`search`
* :ref:`genindex`