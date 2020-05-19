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

## What is data augmentation?

Data augmentation is the creation of artificial data from original data by typically applying a transformation, or multiple transformations, to the original data. It is a common method for improving the versatility of machine learning models, in addition to providing more training examples for datasets of limited size.

In image data for example, it is common to use horizontal and vertical flipping, random cropping, zooming and additive noise for augmentation. In audio, we can use other transformations such as pitch shifting, time stretching or fading the signal in or out. Some image augmentation methods such as additive noise can also be transferred over to audio data.

### Supported augmentation methods

Sigment currently provides the following augmentation methods for both mono and stereo signals. More information about each can be found in the [documentation](https://sigment.readthedocs.io/en/latest):

- [x] Additive Gaussian White Noise
- [x] Time Stretching and Pitch Shifting
- [x] Edge Cropping and Random Cropping
- [x] Linear Fading In/Out
- [x] Normalization, Pre-Emphasis and [Loudest Section Extraction](https://github.com/petewarden/extract_loudest_section)
- [x] Median Filtering
- [x] Clipping Distortion and Reverb

It is also possible to design custom augmentation methods using a simple `Transform` base class provided by Sigment.

## Example

Suppose we have the following stereo signal from `audio.wav`:

<p align="center">
    <img src="https://i.ibb.co/jzB9Hr5/original.png" alt="Original">
</p>

We can apply a pipeline of transformations to the signal to produce multiple augmented copies of it:

<p align="center">
    <img src="https://i.ibb.co/tqwvXcc/augmented.png" alt="Augmented">
</p>

<details>
<summary>
    <b>Click here to see the code for the augmentation pipeline that produces these signals!</b>
</summary>
<p>

```python
from librosa import load
from sigment import *

# Load the stereo WAV audio file
X, sr = load('audio.wav', mono=False)

# Create a complex augmentation pipeline
transform = Pipeline([
    GaussianWhiteNoise(scale=(0.001, 0.0075), p=0.65),
    ExtractLoudestSection(duration=(0.85, 0.95)),
    OneOf([
        RandomCrop(crop_size=(0.01, 0.04), n_crops=(2, 5)),
        SomeOf([
            EdgeCrop('start', crop_size=(0.05, 0.1)),
            EdgeCrop('end', crop_size=(0.05, 0.1))
        ], n=(1, 2))
    ]),
    Sometimes([
        SomeOf([
            LinearFade('in', fade_size=(0.1, 0.2)),
            LinearFade('out', fade_size=(0.1, 0.2))
        ], n=(1, 2))
    ], p=0.5),
    TimeStretch(rate=(0.8, 1.2)),
    PitchShift(n_steps=(-0.25, 0.25)),
    MedianFilter(window_size=(5, 10), p=0.5)
])

# Generate 25 augmentations of the signal X
transform.generate(X, n=25, sr=sr)
```

> **Note**: The full code for this example can be found in the notebook [here](https://nbviewer.jupyter.org/github/eonu/sigment/blob/master/notebooks/README.ipynb).

</p>
</details>

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