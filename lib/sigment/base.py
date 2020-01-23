# -*- coding: utf-8 -*-

from soundfile import read, write

class _Base:
    def apply_to_wav(self, source, out=None):
        out = source if out is None else out
        X, sr = read(source)
        write(out, data=self.__call__(X, sr), samplerate=sr)

    def generate_from_wav(self, source, n=1):
        X, sr = read(source)
        return self.generate(X, n, sr)