import numpy as np
from rtlsdr import RtlSdr
import os, time

sdr = RtlSdr()
sdr.center_freq = 467.5626e6
sdr.sample_rate = 1e6
sdr.gain = 40.2

power_levels = [
    (0, 3),
    (3, 6),
    (6, 9),
    (9, 12),
    (12, 15),
    (15, 18),
    (18, 21),
    (21, 24)
]

waveforms = {
    1: "single_tone",
    2: "sweep", 
    3: "gaussian"
}

# First capture walkie talkie normal signal
input("\n=== WALKIE TALKIE CAPTURE ===\nTurn ON walkie talkies Channel 1\nMake sure jammer is OFF\nPress Enter...")
os.makedirs("/home/vandit/data/real_walkie_talkie", exist_ok=True)
print("Capturing 500 walkie talkie samples...")
for i in range(500):
    samples = sdr.read_samples(256*1024)
    np.save(f"/home/vandit/data/real_walkie_talkie/iq_{i}.npy", samples)
    print(f"walkie_talkie {i+1}/500")
    time.sleep(0.05)
print("✅ Walkie talkie done!")

# Capture no signal
input("\n=== NO SIGNAL ===\nTurn OFF walkie talkies\nMake sure jammer is OFF\nPress Enter...")
os.makedirs("/home/vandit/data/real_no_signal", exist_ok=True)
print("Capturing 500 no signal samples...")
for i in range(500):
    samples = sdr.read_samples(256*1024)
    np.save(f"/home/vandit/data/real_no_signal/iq_{i}.npy", samples)
    print(f"no_signal {i+1}/500")
    time.sleep(0.05)
print("✅ No signal done!")

# Now capture each waveform at each power level
for waveform_num, waveform_name in waveforms.items():
    for power_low, power_high in power_levels:
        folder = f"/home/vandit/data/real_{waveform_name}_pwr{power_low}_{power_high}"
        os.makedirs(folder, exist_ok=True)
        
        input(f"\n=== {waveform_name.upper()} | Power {power_low}-{power_high} dB ===\nSet waveform={waveform_num}, power={power_low} in jamRF_v3.py\nSTART JAMMER then press Enter...")
        
        print(f"Capturing 500 samples of {waveform_name} at power {power_low}-{power_high}...")
        for i in range(500):
            samples = sdr.read_samples(256*1024)
            np.save(f"{folder}/iq_{i}.npy", samples)
            print(f"{waveform_name} pwr{power_low}-{power_high}: {i+1}/500")
            time.sleep(0.05)
        print(f"✅ {waveform_name} power {power_low}-{power_high} done!")

sdr.close()
print("\n🎉 ALL SAMPLES CAPTURED SUCCESSFULLY!")
