<p align="center">
    <h1 align="center">Sigment</h1>
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

<p><b>Note</b>: Although the core functionality of this package is implemented, it remains largely under construction – with tests and documentation to still be done.</p>

## What is data augmentation?

Data augmentation is the creation of artificial data from original data by typically applying a transformation, or multiple transformations, to the original data. It is a common method for improving the versatility of machine learning models, in addition to providing more training examples for datasets of limited size.

In image data for example, it is common to use horizontal and vertical flipping, random cropping, zooming and additive noise for augmentation. In audio, we can use other transformations such as pitch shifting and fading the signal in or out, but some image augmentation methods such as additive noise can also be used on audio data.

### Supported augmentation methods

Sigment provides the following augmentation methods for both mono and stereo signals. More information about each can be found in the [RTD documentation](https://sigment.readthedocs.io/en/latest):

- [x] White Noise (Uniform, Gaussian and Laplacian)
- [x] Time Stretching
- [x] Pitch Shifting
- [x] Edge Cropping
- [x] Fading

> **Soon**: Normalization, Random Cropping and Median Filtering

It is also possible to design your own augmentation methods using a simple `Transform` base class provided by Sigment.

## Example

Suppose we have the following stereo signal `F`:

<p align="center">
    <img src="https://i.ibb.co/cbvgDkY/original.png" alt="Original">
</p>

We can apply a pipeline of transformations to `F` to produce multiple augmented copies of it:

<p align="center">
    <img src="https://i.ibb.co/bKjbZL2/augmented.png" alt="Augmented">
</p>

<details>
<summary>
    <b>Click here to see the code for the augmentation pipeline produces these signals!</b>
</summary>
<p>

```python
import sigment as sig

# Create a complex augmentation pipeline
transform = sig.Pipeline([
    sig.Sometimes([
        sig.OneOf([
            sig.UniformWhiteNoise(upper=(0.1, 0.4)),
            sig.GaussianWhiteNoise(scale=(0.01, 0.075)),
            sig.LaplacianWhiteNoise(scale=(0.01, 0.075))
        ])
    ], p=0.65),
    sig.SomeOf([
        sig.EdgeCrop('start', crop_size=(0.05, 0.15)),
        sig.EdgeCrop('end', crop_size=(0.05, 0.15))
    ], n=(1, 2)),
    sig.Sometimes([
        sig.SomeOf([
            sig.Fade('in', fade_size=(0.1, 0.2)),
            sig.Fade('out', fade_size=(0.1, 0.2))
        ], n=(1, 2))
    ], p=0.5),
    sig.TimeStretch(rate=(0.7, 1.3)),
    sig.PitchShift(n_steps=(-0.25, 0.25)),
])

# Generate 25 augmentations of the signal F
Fs = transform.generate(F, n=25, sr=50)
```

</p>
</details>

> **Note**: The full code for this example can be found in the notebook [here](https://nbviewer.jupyter.org/github/eonu/sigment/blob/master/notebooks/README%20%28Example%29.ipynb).