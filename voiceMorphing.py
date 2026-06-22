import os
from shutil import rmtree
import numpy as np
import soundfile as sf
import pyworld as pw
import matplotlib.pyplot as plt
import librosa

# =========================================================
# CONFIGURATION 
# =========================================================
SPEAKER_NAME = 'Winki'
input_file = 'Winki_MiniProject.wav'

frame_period = 5.0
output_dir = f'test/{SPEAKER_NAME}'

# =========================================================
# 1. Prepare Directory & Extract Baseline
# =========================================================
if not os.path.exists(input_file):
    print(f"File not found: {input_file}. Please ensure the audio file is in the same directory as the script!")
else:
    if os.path.isdir(output_dir):
        rmtree(output_dir)
    os.makedirs(output_dir)

    x, fs = sf.read(input_file)
    x = x.astype(np.float64)

    print(f"Processing data for {SPEAKER_NAME}...")
    print("Performing algorithm analysis (DIO + Stonemask + CheapTrick + D4C)...")
    
    _f0, t = pw.dio(x, fs, frame_period=frame_period)
    f0 = pw.stonemask(x, _f0, t, fs)
    sp = pw.cheaptrick(x, f0, t, fs)
    ap = pw.d4c(x, f0, t, fs)

    y_original = pw.synthesize(f0, sp, ap, fs, frame_period)
    sf.write(f'{output_dir}/0_Baseline_Original.wav', y_original, fs)

    print("\nGenerating voice morphing effects...")

    # ---------------------------------------------------------
    # Experiment A: Adult to Child Conversion
    # ---------------------------------------------------------
    print("-> Executing Experiment A (Adult to Child)...")
    f0_child = f0 * 2.2
    sp_child = np.zeros_like(sp)
    for i in range(sp.shape[0]):
        sp_child[i, :] = np.interp(
            np.linspace(0, fs/2, sp.shape[1]),
            np.linspace(0, fs/2 * 1.5, sp.shape[1]),
            sp[i, :]
        )
    y_child = pw.synthesize(f0_child, sp_child, ap, fs, frame_period)
    sf.write(f'{output_dir}/Experiment_A_Child.wav', y_child, fs)

    # ---------------------------------------------------------
    # Experiment B: Female to Male Conversion
    # ---------------------------------------------------------
    print("-> Executing Experiment B (Female to Male)...")
    f0_male = f0 * 0.6
    sp_male = np.zeros_like(sp)
    for i in range(sp.shape[0]):
        sp_male[i, :] = np.interp(
            np.linspace(0, fs/2, sp.shape[1]),
            np.linspace(0, fs/2 * 0.85, sp.shape[1]),
            sp[i, :]
        )
    y_male = pw.synthesize(f0_male, sp_male, ap, fs, frame_period)
    sf.write(f'{output_dir}/Experiment_B_Male.wav', y_male, fs)

    # ---------------------------------------------------------
    # 3. Calculate and Print Mean F0
    # ---------------------------------------------------------
    mean_original = np.mean(f0[f0 > 0])
    mean_child = np.mean(f0_child[f0_child > 0])
    mean_male = np.mean(f0_male[f0_male > 0])

    print("\n" + "="*40)
    print(f"--- Mean F0 Results for {SPEAKER_NAME} ---")
    print(f"Original Mean F0    : {mean_original:.1f} Hz")
    print(f"Child Morph Mean F0 : {mean_child:.1f} Hz")
    print(f"Male Morph Mean F0  : {mean_male:.1f} Hz")
    print("="*40)

    # =========================================================
    # 4. Generate UP/DOWN Comparison Plots
    # =========================================================
    def plot_comparison_f0(f0_orig, f0_morph, frame_period, filename_prefix, morph_label, save_path):
        print(f"Drawing F0 Comparison for: {filename_prefix}...")
        t_f0 = np.arange(len(f0_orig)) * (frame_period / 1000.0)
        
        fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True, sharey=True)

        axs[0].plot(t_f0, f0_orig, color='tab:blue')
        axs[0].set_title(f"Original Pitch (F0) - {SPEAKER_NAME}")
        axs[0].set_ylabel("Frequency (Hz)")

        axs[1].plot(t_f0, f0_morph, color='tab:red')
        axs[1].set_title(f"Morphed Pitch (F0) - {morph_label}")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Frequency (Hz)")

        plt.tight_layout()
        plt.savefig(f"{save_path}/{filename_prefix}_F0_Combo.png")
        plt.close()

    def plot_comparison_sp(sp_orig, sp_morph, fs, frame_period, filename_prefix, morph_label, save_path):
        print(f"Drawing Spectral Comparison for: {filename_prefix}...")
        t_f0 = np.arange(len(sp_orig)) * (frame_period / 1000.0)
        
        sp_orig_db = 10 * np.log10(sp_orig + 1e-16)
        sp_morph_db = 10 * np.log10(sp_morph + 1e-16)

        fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        img1 = axs[0].imshow(sp_orig_db.T, aspect='auto', origin='lower', extent=[t_f0[0], t_f0[-1], 0, fs/2], cmap='viridis')
        axs[0].set_title(f"Original Spectral Envelope - {SPEAKER_NAME}")
        axs[0].set_ylabel("Frequency (Hz)")
        fig.colorbar(img1, ax=axs[0], format="%+2.0f dB")

        img2 = axs[1].imshow(sp_morph_db.T, aspect='auto', origin='lower', extent=[t_f0[0], t_f0[-1], 0, fs/2], cmap='viridis')
        axs[1].set_title(f"Morphed Spectral Envelope - {morph_label}")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Frequency (Hz)")
        fig.colorbar(img2, ax=axs[1], format="%+2.0f dB")

        plt.tight_layout()
        plt.savefig(f"{save_path}/{filename_prefix}_Spectral_Combo.png")
        plt.close()

    print("\nGenerating Report Figures (Up/Down Combinations)...")
    
    plot_comparison_f0(f0, f0_child, frame_period, f"{SPEAKER_NAME}_A_Child", "Adult-to-Child", output_dir)
    plot_comparison_sp(sp, sp_child, fs, frame_period, f"{SPEAKER_NAME}_A_Child", "Adult-to-Child", output_dir)

    plot_comparison_f0(f0, f0_male, frame_period, f"{SPEAKER_NAME}_B_Male", "Female-to-Male", output_dir)
    plot_comparison_sp(sp, sp_male, fs, frame_period, f"{SPEAKER_NAME}_B_Male", "Female-to-Male", output_dir)

    print(f"Figures successfully generated in '{output_dir}' folder!")

    # =========================================================
    # 5. Calculate Mel-Cepstral Distortion (MCD)
    # =========================================================
    def calculate_mcd(y_original, y_converted, sr):
        mfcc_orig = librosa.feature.mfcc(y=y_original, sr=sr, n_mfcc=24)
        mfcc_conv = librosa.feature.mfcc(y=y_converted, sr=sr, n_mfcc=24)

        mfcc_orig = mfcc_orig[1:, :]
        mfcc_conv = mfcc_conv[1:, :]

        min_len = min(mfcc_orig.shape[1], mfcc_conv.shape[1])
        mfcc_orig = mfcc_orig[:, :min_len]
        mfcc_conv = mfcc_conv[:, :min_len]

        diff = mfcc_orig - mfcc_conv
        dist = np.sqrt(np.sum(diff**2, axis=0))

        constant = (10 * np.sqrt(2)) / np.log(10)
        return constant * np.mean(dist)

    print("\n" + "="*40)
    print(f"--- MCD Results for {SPEAKER_NAME} ---")
    
    mcd_child = calculate_mcd(x, y_child, fs)
    mcd_male = calculate_mcd(x, y_male, fs)

    print(f"Original Baseline MCD : 0.00 dB")
    print(f"Adult to Child MCD    : {mcd_child:.2f} dB")
    print(f"Female to Male MCD    : {mcd_male:.2f} dB")
    print("="*40)