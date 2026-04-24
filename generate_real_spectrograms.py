import numpy as np
import os
from scipy.signal import spectrogram
from scipy.ndimage import zoom

DATA_DIR = "/home/vandit/data"
OUT_DIR = "/home/vandit/spectrograms"
CLASSES = {
    "real_no_signal": "no_signal",
    "real_gaussian": "gaussian",
    "real_single_tone": "single_tone",
    "real_sweep": "sweep"
}
IMG_SIZE = 128

for folder, cls in CLASSES.items():
    os.makedirs(f"{OUT_DIR}/{cls}", exist_ok=True)
    files = sorted(os.listdir(f"{DATA_DIR}/{folder}"))
    for fname in files:
        iq = np.load(f"{DATA_DIR}/{folder}/{fname}")
        f, t, Sxx = spectrogram(iq.real, fs=1e6, nperseg=256, noverlap=128)
        scale_f = IMG_SIZE / Sxx.shape[0]
        scale_t = IMG_SIZE / Sxx.shape[1]
        Sxx_resized = zoom(Sxx, (scale_f, scale_t))
        Sxx_log = np.log1p(np.abs(Sxx_resized))
        Sxx_norm = (Sxx_log - Sxx_log.min()) / (Sxx_log.max() - Sxx_log.min() + 1e-9)
        np.save(f"{OUT_DIR}/{cls}/{fname}", Sxx_norm.astype(np.float32))
    print(f"Done: {cls} — {len(files)} spectrograms")

print("All real spectrograms generated!")
