<p align="center">
  <h1 align="center">
    Sigment
  </h1>
</p>

<p align="center">
  <em>An extensible data augmentation package for creating complex transformation pipelines for audio signals.</em>
</p>

<p align="center">
  <div align="center">
    <a href="https://pypi.org/project/sigment">
      <img src="https://img.shields.io/pypi/v/sigment?style=flat" alt="PyPI"/>
    </a>
    <a href="https://pypi.org/project/sigment">
      <img src="https://img.shields.io/pypi/pyversions/sigment?style=flat" alt="PyPI - Python Version"/>
    </a>
    <a href="https://raw.githubusercontent.com/eonu/sigment/master/LICENSE">
      <img src="https://img.shields.io/pypi/l/sigment?style=flat" alt="PyPI - License"/>
    </a>
    <a href="https://sigment.readthedocs.io/en/latest">
      <img src="https://readthedocs.org/projects/sigment/badge/?version=latest&style=flat" alt="Read The Docs - Documentation">
    </a>
    <a href="https://travis-ci.org/eonu/sigment">
      <img src="https://img.shields.io/travis/eonu/sigment?logo=travis&style=flat" alt="Travis - Build">
    </a>
  </div>
</p>

## What is data augmentation?

Data augmentation is the creation of artificial data from original data. It often works by applying a transformation, or multiple transformations, to the original data.

In image data for example, it is common to use horizontal and vertical flipping, random cropping, zooming and additive noise for augmentation. In audio we can use other transformations such as pitch shifting and fading the signal in or out, but some image augmentation methods such as additive noise can also be used on audio data.

Sigment provides the following augmentation methods for both mono and stereo signals. More information about each can be found in the [RTD documentation](https://sigment.readthedocs.io/en/latest):

<ul style="columns:2;-webkit-columns:2;-moz-columns:2;">
    <li>Uniform White Noise</li>
    <li>Gaussian White Noise</li>
    <li>Laplacian White Noise</li>
    <li>Time Stretching</li>
    <li>Pitch Shifting</li>
    <li>Edge Cropping</li>
    <li>Fading</li>
</ul>

> **Soon**: Normalization, Random Cropping and Median Filtering

It is also possible to design your own augmentation methods using a `Transform` simple base class provided by Sigment.