import numpy as np
from rtlsdr import RtlSdr
from scipy.signal import spectrogram
from scipy.ndimage import zoom
import os, time

sdr = RtlSdr()
sdr.center_freq = 467.5626e6
sdr.sample_rate = 1e6
sdr.gain = 40.2

def capture_spectrograms(folder, label, count=200):
    os.makedirs(folder, exist_ok=True)
    print(f"Capturing {count} spectrograms of {label}...")
    for i in range(count):
        samples = sdr.read_samples(256*1024)
        f, t, Sxx = spectrogram(samples.real, fs=1e6, nperseg=256, noverlap=128)
        Sxx_resized = zoom(Sxx, (128/Sxx.shape[0], 128/Sxx.shape[1]))
        Sxx_log = np.log1p(np.abs(Sxx_resized))
        Sxx_norm = ((Sxx_log - Sxx_log.min()) / 
                   (Sxx_log.max() - Sxx_log.min() + 1e-9)).astype(np.float32)
        np.save(f"{folder}/spec_{i}.npy", Sxx_norm)
        if (i+1) % 50 == 0:
            print(f"{label}: {i+1}/{count}")
    print(f"✅ {label} done!")

power_levels = [0, 3, 6, 9, 12, 15, 18, 21, 24]
waveforms = {1: "single_tone", 2: "sweep", 3: "gaussian"}

# No signal first
input("\n=== NO SIGNAL ===\nJammer OFF, press Enter...")
capture_spectrograms("/home/vandit/spectrograms/no_signal", "no_signal", 200)

# Each waveform at each power level
for waveform_num, waveform_name in waveforms.items():
    for power in power_levels:
        input(f"\n=== {waveform_name.upper()} | Power {power} dB ===\nSet waveform={waveform_num}, power={power}, START JAMMER then press Enter...")
        folder = f"/home/vandit/spectrograms/{waveform_name}_pwr{power}"
        capture_spectrograms(folder, f"{waveform_name}_pwr{power}", 200)

sdr.close()
print("\n🎉 ALL DONE!")
