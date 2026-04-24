import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pickle

SPEC_DIR = "/home/vandit/spectrograms"
MAX_PER_FOLDER = 50  # Only load 50 per power level to save RAM

X = []
y = []

def load_folder(folder, label, max_samples=50):
    if not os.path.exists(folder):
        return 0
    files = os.listdir(folder)[:max_samples]
    for f in files:
        spec = np.load(os.path.join(folder, f))
        X.append(spec.flatten())
        y.append(label)
    return len(files)

# No signal
n = load_folder(f"{SPEC_DIR}/no_signal", "no_signal", 200)
print(f"no_signal: {n}")

# Gaussian - 50 per power level = 450 total
total = 0
for pwr in [0,3,6,9,12,15,18,21,24]:
    total += load_folder(f"{SPEC_DIR}/gaussian_pwr{pwr}", "gaussian", MAX_PER_FOLDER)
print(f"gaussian: {total}")

# Single Tone
total = 0
for pwr in [0,3,6,9,12,15,18,21,24]:
    total += load_folder(f"{SPEC_DIR}/single_tone_pwr{pwr}", "single_tone", MAX_PER_FOLDER)
print(f"single_tone: {total}")

# Sweep
total = 0
for pwr in [0,3,6,9,12,15,18,21,24]:
    total += load_folder(f"{SPEC_DIR}/sweep_pwr{pwr}", "sweep", MAX_PER_FOLDER)
print(f"sweep: {total}")

X = np.array(X, dtype=np.float32)
y = np.array(y)
print(f"\nTotal: {len(X)} samples | Features: {X.shape[1]}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Train: {len(X_train)} | Test: {len(X_test)}")

print("\nTraining Random Forest...")
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("\n=== CLASSIFICATION REPORT ===")
print(classification_report(y_test, y_pred))
print("=== CONFUSION MATRIX ===")
print(confusion_matrix(y_test, y_pred))

pickle.dump(clf, open("/home/vandit/rf_model.pkl", "wb"))
print("\n✅ Model saved!")
