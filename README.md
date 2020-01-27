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

> **Disclaimer**: Although the core functionality of this package is fully implemented, it still requires proper unit testing.

## What is data augmentation?

Data augmentation is the creation of artificial data from original data by typically applying a transformation, or multiple transformations, to the original data. It is a common method for improving the versatility of machine learning models, in addition to providing more training examples for datasets of limited size.

In image data for example, it is common to use horizontal and vertical flipping, random cropping, zooming and additive noise for augmentation. In audio, we can use other transformations such as pitch shifting and fading the signal in or out, but some image augmentation methods such as additive noise can also be used on audio data.

### Supported augmentation methods

Sigment provides the following augmentation methods for both mono and stereo signals. More information about each can be found in the [documentation](https://sigment.readthedocs.io/en/latest):

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

## Installation

To install Sigment from PyPI, you can use `pip`:

```console
pip install sigment
```

## Components

Sigment provides two main components that can be used to construct augmentation pipelines:

- **Transforms** (`sigment.transforms`): Used to apply a specific type of transformation to the audio data.

- **Quantifiers** (`sigment.quantifiers`): Used to specify rules for how a sequence of transformations
or nested quantifiers should be applied to augment the audio data.

Read the [documentation](https://sigment.readthedocs.io/en/latest) and [example notebooks](https://nbviewer.jupyter.org/github/eonu/sigment/blob/master/notebooks/) for more information about the usage of both.

## Acknowledgements

Sigment offers a familiar interface for transformations, taking inspiration from some other well-written augmentation libraries. Without the following libraries, the capabilities of Sigment would be very limited:

- [aleju/**imgaug**](https://github.com/aleju/imgaug): _Image augmentation for machine learning experiments._
- [makcedward/**nlpaug**](https://github.com/makcedward/nlpaug): _Data augmentation for NLP_
- [albumentations-team/**albumentations**](https://github.com/albumentations-team/albumentations): _fast image augmentation library and easy to use wrapper around other libraries_
- [iver56/**audiomentations**](https://github.com/iver56/audiomentations): _A Python library for audio data augmentation. Inspired by albumentations. Useful for machine learning._

## Contributors

All contributions to this repository are greatly appreciated. Contribution guidelines can be found [here](/CONTRIBUTING.md).

<table>
	<thead>
		<tr>
			<th align="center">
        <a href="https://github.com/eonu">
        <img src="https://avatars0.githubusercontent.com/u/24795571?s=460&v=4" alt="Edwin Onuonga" width="60px">
        <br/><sub><b>Edwin Onuonga</b></sub>
        </a>
        <br/>
        <a href="mailto:ed@eonu.net">✉️</a>
        <a href="https://eonu.net">🌍</a>
			</th>
			<!-- Add more <th></th> blocks for more contributors -->
		</tr>
	</thead>
</table>

---

<p align="center">
  <b>Sigment</b> &copy; 2019-2020, Edwin Onuonga - Released under the <a href="https://opensource.org/licenses/MIT">MIT</a> License.<br/>
  <em>Authored and maintained by Edwin Onuonga.</em>
</p>