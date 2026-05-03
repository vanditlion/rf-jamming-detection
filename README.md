# RF Jamming Detection on Raspberry Pi

A lightweight, edge-deployable machine learning system for real-time RF signal classification and jamming detection on Raspberry Pi 4 using an RTL-SDR dongle.

## Hardware
- Raspberry Pi 4 (4GB RAM)
- RTL-SDR dongle (RTL2838UHIDIR, R820T tuner)
- NI USRP-2920 (jamming signal generation)
- FRS Walkie-Talkies Channel 1 (victim devices)

## Signal Classes
- No Signal (background noise)
- Gaussian Noise Jamming
- Single-Tone Jamming
- Sweep Jamming

## Results
- 100% classification accuracy on real hardware data
- 580-650ms inference latency on Raspberry Pi 4
- Trained at 467.5626 MHz across power levels 0-24 dBm

## Pipeline
IQ Capture → STFT Spectrogram (128x128) → Random Forest → Detection Alert

## Scripts
- realtime_detect.py — Live jamming detection loop
- train_model_v2.py — Model training with multi-power dataset
- capture_spectrograms_only.py — Real data collection
- generate_real_spectrograms.py — Spectrogram generation

## Author
Vandit Shah
EECE 6902 Graduate Capstone Project II
Loyola Marymount University
Advisor: Prof. Gustavo Vejarano

## Dataset Download
The complete dataset and all project files are available on Google Drive:

🔗 [Download Full Dataset (5,600 spectrograms)](https://drive.google.com/drive/folders/1MOu3p8xwOwnIb1y3AAO4jCqGgmqN_Avu?usp=drive_link)

### Dataset Contents
- 5,600 real spectrograms captured in LMU CubeSat Laboratory
- 4 classes: No Signal, Gaussian Noise, Single-Tone, Sweep
- 9 power levels per jamming class: 0-24 dBm in 3 dBm steps
- 200 spectrograms per class per power level
- Format: 128x128 NumPy .npy files (float32)
- Trained model: rf_model.pkl (Random Forest, scikit-learn)
