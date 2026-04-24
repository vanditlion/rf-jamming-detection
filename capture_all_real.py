import numpy as np
from rtlsdr import RtlSdr
import os, time, shutil

sdr = RtlSdr()
sdr.center_freq = 467.5626e6
sdr.sample_rate = 1e6
sdr.gain = 40.2

# NO SIGNAL
input("\n=== STEP 1 === Make sure JAMMER IS OFF then press Enter...")
print("Capturing 100 NO SIGNAL samples...")
for i in range(100):
    samples = sdr.read_samples(256*1024)
    np.save(f"/home/vandit/data/real_no_signal/iq_{i}.npy", samples)
    print(f"no_signal {i+1}/100")
    time.sleep(0.1)
print("✅ NO SIGNAL done!")

# GAUSSIAN
input("\n=== STEP 2 === Set waveform=3, START JAMMER then press Enter...")
print("Capturing 100 GAUSSIAN samples...")
for i in range(100):
    samples = sdr.read_samples(256*1024)
    np.save(f"/home/vandit/data/real_gaussian/iq_{i}.npy", samples)
    print(f"gaussian {i+1}/100")
    time.sleep(0.1)
print("✅ GAUSSIAN done!")

# SINGLE TONE
input("\n=== STEP 3 === Set waveform=1, RESTART JAMMER then press Enter...")
print("Capturing 100 SINGLE TONE samples...")
for i in range(100):
    samples = sdr.read_samples(256*1024)
    np.save(f"/home/vandit/data/real_single_tone/iq_{i}.npy", samples)
    print(f"single_tone {i+1}/100")
    time.sleep(0.1)
print("✅ SINGLE TONE done!")

# SWEEP
input("\n=== STEP 4 === Set waveform=2, RESTART JAMMER then press Enter...")
print("Capturing 100 SWEEP samples...")
for i in range(100):
    samples = sdr.read_samples(256*1024)
    np.save(f"/home/vandit/data/real_sweep/iq_{i}.npy", samples)
    print(f"sweep {i+1}/100")
    time.sleep(0.1)
print("✅ SWEEP done!")

sdr.close()
print("\n🎉 ALL 400 SAMPLES CAPTURED SUCCESSFULLY!")
