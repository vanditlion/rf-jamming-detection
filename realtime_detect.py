import numpy as np
from rtlsdr import RtlSdr
from scipy.signal import spectrogram
from scipy.ndimage import zoom
import pickle
import time

# Load model
clf = pickle.load(open("/home/vandit/rf_model.pkl", "rb"))
print("✅ Model loaded!")

# Setup RTL-SDR
sdr = RtlSdr()
sdr.center_freq = 467.5626e6
sdr.sample_rate = 1e6
sdr.gain = 40.2

print("=" * 55)
print("  RF JAMMING DETECTOR")
print("  Monitoring: 467.56260 MHz")
print("  Bandwidth:  1000 kHz")
print("  Classes:    Gaussian | Single Tone | Sweep | No Signal")
print("  Press Ctrl+C to stop")
print("=" * 55)

try:
    while True:
        start = time.time()

        # Capture IQ
        samples = sdr.read_samples(256*1024)

        # Spectrogram
        f, t, Sxx = spectrogram(samples.real, fs=1e6, nperseg=256, noverlap=128)
        Sxx_resized = zoom(Sxx, (128/Sxx.shape[0], 128/Sxx.shape[1]))
        Sxx_log = np.log1p(np.abs(Sxx_resized))
        Sxx_norm = ((Sxx_log - Sxx_log.min()) /
                   (Sxx_log.max() - Sxx_log.min() + 1e-9)).astype(np.float32)

        # Classify
        features = Sxx_norm.flatten().reshape(1, -1)
        pred = clf.predict(features)[0]
        proba = clf.predict_proba(features)[0]
        confidence = max(proba) * 100

        elapsed = (time.time() - start) * 1000

        if pred == "no_signal":
            print(f"✅ NO SIGNAL        | Confidence: {confidence:.1f}% | {elapsed:.1f}ms")
        else:
            label = pred.upper().replace("_", " ")
            print(f"🚨 JAMMING: {label:<12} | Confidence: {confidence:.1f}% | {elapsed:.1f}ms")

except KeyboardInterrupt:
    print("\nStopped.")
    sdr.close()
