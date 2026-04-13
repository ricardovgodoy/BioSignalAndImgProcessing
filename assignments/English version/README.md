# 📡 Biosignal and Image Processing — English Version Assignments

This folder contains the **English-language Jupyter notebooks** for the *Biosignal and Image Processing* course. The material follows a structured progression from foundational signal processing through advanced image analysis, with hands-on Python exercises throughout.

---

## 📂 Contents Overview

| Notebook | Topic |
|---|---|
| `Aula_3_en.ipynb` | Discrete Signals & Sampling |
| `Aula_5_e_6_en.ipynb` | DFT, Circular Convolution & FFT |
| `Aula_7_en.ipynb` | Time-Domain Filtering |
| `Aula_8_en.ipynb` | Frequency-Domain Filtering |
| `Aula_10_en.ipynb` | EMG Signal Analysis |
| `Aula_12_e_13_en.ipynb` | Autoregressive (AR) Modeling |
| `Aula_17_en.ipynb` | Image Fundamentals (Ch. 2) |
| `Aula_18_en.ipynb` | Spatial-Domain Enhancement (Ch. 3) |
| `Aula_19_en.ipynb` | Frequency-Domain Enhancement (Ch. 4) |
| `Aula_20_en.ipynb` | Practice — Image Fundamentals & Enhancement |
| `Aula_21_en.ipynb` | Image Restoration (Ch. 5) |
| `Aula_22_en.ipynb` | Image Segmentation (Ch. 10) |
| `Aula_23_en.ipynb` | Wavelets (Ch. 7) |
| `Demonstração_EMG_en.ipynb` | EMG Demonstration — Gesture Recognition |
| `Demonstração_EMG (1)_en.ipynb` | EMG Demonstration — Extended Version |
| `Extra_Aula_12_e_13_en.ipynb` | Extra — Speech Segmentation & AR Modeling |
| `Exercícios_de_programação_1_en.ipynb` | Graded Assignment 1 — ECG Filter Design |
| `Pratica_de_python_2_en.ipynb` | Graded Assignment 2 — EMG Gesture Classification |
| `Pratica_3_en.ipynb` | Practice 3 — Feature Extraction & Classification |
| `Pratica_final_en.ipynb` | Final Project — Blood Cell Classification System |

---

## 🧠 Part I — Biosignal Processing

### `Aula_3_en.ipynb` — Discrete Signals & Sampling
Introduction to discrete-time signals: unit impulse δ[n], unit step u[n], and discrete sinusoids. Demonstrates periodic sampling and the aliasing effect through a simulated ECG signal. Shows how insufficient sampling rate causes frequency distortion and how it impacts peak detection and arrhythmia analysis.

**Key concepts:** discrete-time axis, impulse train, Nyquist theorem, aliasing, ECG simulation.

---

### `Aula_5_e_6_en.ipynb` — DFT, Circular Convolution & FFT
Manual implementation of the Discrete Fourier Transform followed by a step-by-step comparison with NumPy's FFT. Covers circular convolution with worked examples, DFT-based spectral analysis, and the computational advantage of the FFT.

**Key concepts:** DFT formula, circular convolution, FFT complexity, spectral resolution, frequency identification.

---

### `Aula_7_en.ipynb` — Time-Domain Filtering
Applies three classical time-domain techniques to ECG signals loaded from `.dat` files. Derivative filters are used to remove baseline wander (low-frequency drift); moving average filters smooth high-frequency noise; synchronized averaging exploits signal periodicity to recover a clean QRS template from a noisy ECG.

**Key concepts:** first/second-order derivatives, moving average, synchronized averaging, baseline wander, QRS template.

**Data files required:** `ecg_lfn.dat`, `ecg_hfn.dat`

---

### `Aula_8_en.ipynb` — Frequency-Domain Filtering
Designs and applies Butterworth low-pass, high-pass, and notch filters using `scipy.signal`. Demonstrates each filter on a synthetic multi-component signal and then applies a 60 Hz notch filter to a real ECG with power-line interference. Also shows DFT-based frequency-domain removal as an alternative to the IIR notch filter.

**Key concepts:** Butterworth filter design, `butter`/`filtfilt`, notch filter (`iirnotch`), frequency response (`freqz`), power-line interference.

**Data files required:** `ecg2x60.dat`, `ecg_lfn.dat`, `ecg_hfn.dat`

---

### `Aula_10_en.ipynb` — EMG Signal Analysis
Analyzes a diaphragmatic EMG signal (10 kHz, from a dog) representing two respiratory cycles. Implements a `moving_rms` function via convolution and compares 50 ms and 150 ms window sizes. Then introduces *turns count* as an alternative signal descriptor and evaluates which measure (RMS, envelope, turns count) best correlates with respiratory airflow. A second example applies similar moving-window analysis to a voice signal (word "safety", 8 kHz).

**Key concepts:** EMG envelope, RMS, zero-crossing rate, turns count, decimation, window analysis.

**Data files required:** `emg_dog2.dat`

---

### `Aula_12_e_13_en.ipynb` — Autoregressive (AR) Modeling
Introduces all-pole (AR) parametric modeling of biosignals using the autocorrelation method and Yule-Walker equations (solved via `scipy.linalg.solve_toeplitz`). Applies AR modeling to a damped sinusoid and a synthetic ECG. Explores the effect of model order (p = 4, 8, 12) on signal reconstruction, and demonstrates how baseline wander degrades AR coefficient estimation and how high-pass preprocessing restores performance.

**Key concepts:** AR(p) model, autocorrelation method, Toeplitz matrix, Yule-Walker equations, model order selection, baseline wander.

---

## 🖼️ Part II — Medical Image Processing

### `Aula_17_en.ipynb` — Image Fundamentals (Chapter 2)
Loads a brain MRI volume from `scikit-image` and covers foundational digital image operations: spatial resolution reduction, intensity quantization (false contours), bicubic/bilinear/nearest-neighbor interpolation, arithmetic and logical operations, histogram computation, and geometric transformations including DFT for periodic-noise analysis.

**Key concepts:** spatial vs. intensity resolution, quantization, interpolation, ROI masking, neighborhood filtering, image histograms.

---

### `Aula_18_en.ipynb` — Spatial-Domain Enhancement (Chapter 3)
Systematic tour of intensity-domain enhancement techniques applied to a brain MRI slice. Covers image negative, log and power-law (gamma) transforms, contrast stretching, bit-plane slicing, global histogram equalization, CLAHE, spatial smoothing filters (mean, Gaussian, median), and spatial sharpening via Laplacian, unsharp masking, highboost, and Sobel gradient.

**Key concepts:** intensity transformations, histogram equalization, CLAHE, convolution vs. correlation, noise types, Laplacian sharpening, Sobel operator.

---

### `Aula_19_en.ipynb` — Frequency-Domain Enhancement (Chapter 4)
Full treatment of the 2D DFT and its application to image filtering. Starts from 1D complex numbers and the Convolution Theorem, then demonstrates aliasing, 1D and 2D DFT, spectrum centering, and frequency-domain filtering with padding. Implements and compares Ideal (ILPF), Butterworth (BLPF), and Gaussian (GLPF) low-pass filters, and the corresponding high-pass filters including homomorphic filtering.

**Key concepts:** FFT/IFFT, spectrum centering (`fftshift`), zero-padding, aliasing, ILPF/BLPF/GLPF, ringing artifacts, highboost, homomorphic filtering.

---

### `Aula_20_en.ipynb` — Practice: Image Fundamentals & Enhancement
Hands-on guided practice integrating Chapters 1–4. Students run pre-written code blocks and answer discussion questions covering spatial/intensity resolution, distances between pixels, pointwise intensity transforms, histogram equalization vs. CLAHE, smoothing filters (mean, Gaussian, median), sharpening (Laplacian, unsharp mask), and frequency-domain filtering (GLPF and GHPF) — all applied to a brain MRI slice.

---

### `Aula_21_en.ipynb` — Image Restoration (Chapter 5)
Covers the image degradation model g = h * f + η and restoration strategies. Demonstrates: periodic noise removal with a Gaussian notch filter in the frequency domain; simulation of motion blur using a linear PSF; inverse filtering (direct and truncated/pseudo-inverse); and Wiener filtering as the minimum-MSE restoration approach.

**Key concepts:** degradation model, PSF, H(u,v) estimation, periodic noise, notch filter, inverse filtering, truncated inverse filter, Wiener filter (K parameter).

---

### `Aula_22_en.ipynb` — Image Segmentation (Chapter 10)
Practical session on image segmentation. Implements Sobel (Gx, Gy, magnitude) and Canny edge detection with parameter exploration. Covers global thresholding (manual and Otsu), adaptive/local thresholding (Gaussian neighborhood), and a simplified seed-based region growing algorithm using a BFS queue.

**Key concepts:** Sobel operator, Canny (sigma, hysteresis thresholds), Otsu threshold, adaptive thresholding, region growing, 8-connectivity.

---

### `Aula_23_en.ipynb` — Wavelets (Chapter 7)
Introduction to wavelet transforms using PyWavelets (`pywt`). Visualizes Haar scaling and wavelet functions. Demonstrates 1D DWT (approximation cA and detail cD coefficients), multilevel decomposition with `wavedec`, and perfect signal reconstruction. Extends to 2D wavelet decomposition of a brain MRI (LL, LH, HL, HH sub-bands), with exercises exploring coefficient zeroing for denoising/compression.

**Key concepts:** Haar wavelet, scaling function, DWT, `pywt.dwt`/`wavedec`/`wavedec2`, approximation vs. detail sub-bands, perfect reconstruction, Daubechies wavelets.

---

## 🔬 Demonstrations

### `Demonstração_EMG (1)_en.ipynb` — EMG Gesture Recognition
Hands-on demonstration using 8-channel surface EMG signals (1,200 Hz, g.tec g.USBamp, 0.5–100 Hz bandpass) acquired from a healthy subject performing three hand gestures: **full grasp**, **pinch**, and **rest**. Channels cover dorsal interosseous, opponens pollicis, abductor pollicis longus, finger flexors/extensors, and biceps brachii. After loading and plotting raw signals and DFT spectra for each gesture, students extract and tabulate eight time-domain features:

| Feature | Abbreviation |
|---|---|
| Root Mean Square | RMS |
| Waveform Length | WL |
| Zero Crossings | ZC |
| Integrated EMG | IEMG |
| Mean Absolute Value | MAV |
| Willison Amplitude | WAMP |
| Variance | VAR |
| Log Detector | LogD |


---

## 📝 Exercises & Graded Assignments

### `Exercícios_de_programação_1_en.ipynb` — Graded Assignment 1: ECG Filter Design
Students select and tune appropriate filters for three ECG recordings with different noise profiles:

- **ecg_lfn.dat** (1000 Hz) — low-frequency baseline wander → high-pass / derivative filters
- **ecg_hfn.dat** (1000 Hz) — high-frequency noise → low-pass / moving average filters
- **ecg2x60.dat** (200 Hz) — 60 Hz power-line interference → notch filter

All filter implementations are provided; students choose correct filter types and tune parameters. Final clean code is submitted as a group deliverable via Canvas.

---

### `Extra_Aula_12_e_13_en.ipynb` — Extra Assignment: Speech & PCG AR Modeling
**Exercise 1:** Segments the speech signal for the word *"safety"* (8 kHz, `safety.wav`) into voiced, unvoiced, and silence using short-term RMS and ZCR (zero-crossing rate) with 30 ms windows. Applies AR modeling (Yule-Walker, order 14 voiced / order 8 unvoiced) to each segment and compares original vs. synthesized signal.

**Exercise 2:** Analyzes three-channel PCG/ECG/carotid pulse recordings (`pec1.dat`, `pec33.dat`, `pec52.dat`, 1000 Hz). The `pec33` signal contains a systolic murmur (pulmonary stenosis / VSD / pulmonary hypertension). Students segment each recording into systolic and diastolic phases and apply AR modeling to each segment.

---

### `Pratica_de_python_2_en.ipynb` — Graded Assignment 2: EMG Gesture Classification with Random Forest
Uses 8-channel EMG data (1,200 Hz, g.USBamp, 5–500 Hz Butterworth + 50 Hz notch) from 4 grasp types plus rest (5 classes). Provides train/test splits across 10 repetitions.

**Tasks:**
1. Train a Random Forest on raw reshaped data `(N, 16000)` and evaluate accuracy.
2. Extract the same 8 features per channel as in the EMG demonstration → `(N, 8, 8)` feature matrix; retrain and compare.
3. Discuss which model performs better and why.
4. Evaluate best model with additional metrics (precision, recall, F1, confusion matrix).
5. Vary `n_estimators` and analyze impact on performance.

---

### `Pratica_3_en.ipynb` — Practice 3: Feature Extraction & Classification
Covers Chapters 11 and 12. Implements contour representation (chain codes, 4-direction), Fourier contour descriptors with reconstruction using N descriptors, and regional descriptors (Euler number, statistical texture, Hu moments via OpenCV). Then introduces object recognition: template matching with normalized cross-correlation, Gaussian Naive Bayes classification with decision boundary visualization, and a two-hidden-layer MLP (`MLPClassifier`) from scikit-learn.

---

### `Pratica_final_en.ipynb` — Final Project: Blood Cell Classification System
End-to-end image analysis pipeline using the **BloodMNIST** dataset (8 blood cell types: basophil, eosinophil, erythroblast, ig, lymphocyte, monocyte, neutrophil, platelet). Students build a complete system:

1. **Part 0** — Download BloodMNIST, inspect class distribution, visualize samples.
2. **Part 1** — Preprocessing: grayscale conversion, histogram equalization, Gaussian noise simulation, median filter denoising.
3. **Part 2** — Segmentation: Otsu thresholding + morphological cleaning (`remove_small_objects`, `binary_fill_holes`).
4. **Part 3** — Feature extraction: shape (area, perimeter, eccentricity, solidity, Hu moments), color (mean R/G/B), texture (mean and std of grayscale intensities).
5. **Part 4** — Classification: apply the pipeline to a dataset subset, train an MLP, evaluate with accuracy score and confusion matrix, discuss failure modes and clinical implications.

---

## 🛠️ Dependencies

```
numpy
scipy
matplotlib
scikit-image
scikit-learn
opencv-python (cv2)
pywavelets (pywt)
librosa
tensorflow / keras
medmnist
pandas
sounddevice
gdown
```

Install all at once:
```bash
pip install numpy scipy matplotlib scikit-image scikit-learn opencv-python PyWavelets librosa tensorflow medmnist pandas sounddevice gdown
```

---

## 📁 External Data Files

Some notebooks require `.dat` or `.wav` files cloned from the course repository:

```bash
git clone https://github.com/ricagodoy/BioSignalAndImgProcessing.git
```

| File | Used In |
|---|---|
| `ecg_lfn.dat` | Aula_7, Exercícios_1 |
| `ecg_hfn.dat` | Aula_7, Exercícios_1 |
| `ecg2x60.dat` | Aula_8, Exercícios_1 |
| `emg_dog2.dat` | Aula_10 |
| `safety.wav` | Extra_Aula_12_e_13 |
| `pec1.dat`, `pec33.dat`, `pec52.dat` | Extra_Aula_12_e_13 |
| `EMG_data_*.npy` | Demonstração_EMG, Pratica_2 |

---

## 📖 Course Structure at a Glance

```
Part I — Biosignal Processing
  Aula 3   →  Discrete signals & sampling
  Aula 5–6 →  DFT & FFT
  Aula 7   →  Time-domain filtering
  Aula 8   →  Frequency-domain filtering
  Aula 10  →  EMG analysis (RMS, turns count)
  Aula 12–13 → AR/parametric modeling

Part II — Medical Image Processing
  Aula 17  →  Image fundamentals
  Aula 18  →  Spatial enhancement
  Aula 19  →  Frequency-domain enhancement
  Aula 20  →  Practice (Ch. 1–4)
  Aula 21  →  Image restoration
  Aula 22  →  Segmentation
  Aula 23  →  Wavelets

Demonstrations
  EMG gesture recognition (8 channels, 3 classes)

Graded Assignments
  Assignment 1  →  ECG filter design
  Assignment 2  →  EMG gesture classification (Random Forest)
  Practice 3    →  Feature extraction & classification
  Final Project →  Blood cell classification (BloodMNIST)
```

---

*All notebooks are designed to run in Google Colab. For assignments, go to **File → Save a copy in Drive** to preserve your work before editing.*
