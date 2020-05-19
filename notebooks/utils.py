import numpy as np, matplotlib.pyplot as plt, IPython.display as ipd, librosa.display

def listen(signals, sr=None):
    if isinstance(signals, str):
        ipd.display(ipd.Audio(signals))
    elif isinstance(signals, np.ndarray):
        ipd.display(ipd.Audio(signals, rate=sr))
    elif isinstance(signals, list):
        for signal in signals:
            ipd.display(ipd.Audio(signal, rate=sr))

def plot(X1, X2=None, sr=None):
    if sr is None:
        raise ValueError('Sample rate required')

    if X2 is None:
        plt.figure(figsize=(6.3, 2))
        librosa.display.waveplot(X1, sr=sr, color='r', alpha=0.5)

    if X2 is not None:
        fig, axs = plt.subplots(2, 1, figsize=(6.3, 3.75), sharey=True)
        p1 = librosa.display.waveplot(X1, sr=sr, ax=axs[0], color='r', alpha=0.5)
        axs[0].xaxis.label.set_visible(False)
        p2 = librosa.display.waveplot(X2, sr=sr, ax=axs[1], color='b', alpha=0.5)
        fig.legend((p1, p2), ('Original', 'Transformed'), 'upper center', ncol=2, bbox_to_anchor=(0.5, 1.05))

    plt.tight_layout()
    plt.show()