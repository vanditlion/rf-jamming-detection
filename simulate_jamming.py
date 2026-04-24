import numpy as np
import os
import time

SAMPLE_RATE = 1e6
NUM_SAMPLES = 256 * 1024

def save(label, samples, i):
    path = f"/home/vandit/data/{label}/iq_{label}_{i}.npy"
    np.save(path, samples)
    print(f"Saved {path}")

for i in range(50):
    t = np.arange(NUM_SAMPLES) / SAMPLE_RATE

    # Gaussian noise jamming
    gaussian = (np.random.randn(NUM_SAMPLES) + 1j * np.random.randn(NUM_SAMPLES)) * 0.5
    save("gaussian", gaussian, i)

    # Single tone jamming — fixed tone within 100kHz bandwidth
    f_jam = 40e3
    single_tone = np.exp(2j * np.pi * f_jam * t)
    save("single_tone", single_tone, i)

    # Sweep jamming — sweeping within 100kHz bandwidth
    f_start, f_end = 10e3, 90e3
    sweep_freq = np.linspace(f_start, f_end, NUM_SAMPLES)
    sweep = np.exp(2j * np.pi * np.cumsum(sweep_freq) / SAMPLE_RATE)
    save("sweep", sweep, i)

print("Done! 50 files per class generated.")

# Add no_signal class
import os
os.makedirs("/home/vandit/data/no_signal", exist_ok=True)
SAMPLE_RATE_NS = 1e6
NUM_SAMPLES_NS = 256 * 1024
for i in range(50):
    t = np.arange(NUM_SAMPLES_NS) / SAMPLE_RATE_NS
    # Thermal noise — very low power random noise
    no_signal = (np.random.randn(NUM_SAMPLES_NS) + 1j * np.random.randn(NUM_SAMPLES_NS)) * 0.01
    path = f"/home/vandit/data/no_signal/iq_no_signal_{i}.npy"
    np.save(path, no_signal)
    print(f"Saved {path}")
print("No signal class done!")
