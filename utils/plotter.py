import librosa
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_freq(audio_path, freq_min=0, freq_max=None, use_db=True, save_path=None):
    y, sr = librosa.load(audio_path, sr=None, mono=True)

    N = len(y)
    y_fft = np.fft.rfft(y)
    freq = np.fft.rfftfreq(N, d=1/sr)
    
    magnitude = np.abs(y_fft)
    
    if use_db:
        magnitude = 20 * np.log10(magnitude + 1e-12)
    
    if freq_max is None:
        freq_max = sr / 2  
    
    mask = (freq >= freq_min) & (freq <= freq_max)
    freq_filtered = freq[mask]
    mag_filtered = magnitude[mask]
    
    plt.figure(figsize=(12, 5))
    plt.plot(freq_filtered, mag_filtered)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)" if use_db else "Magnitude")
    plt.title(f"Frequency range: {freq_min} Hz → {freq_max} Hz")
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)

    plt.show()

    return freq_filtered, mag_filtered

def plot_spectrogram(audio_path, sr=None, n_fft=2048, hop_length=512, freq_max=None, save_path=None):
    y, sr = librosa.load(audio_path, sr=sr, mono=True)

    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)

    S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)

    plt.figure(figsize=(12, 6))
    librosa.display.specshow(
        S_db,
        sr=sr,
        hop_length=hop_length,
        x_axis='time',
        y_axis='hz'
    )
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram (dB scale)")

    if freq_max is not None:
        plt.ylim(0, freq_max)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        
    plt.show()

    return S_db