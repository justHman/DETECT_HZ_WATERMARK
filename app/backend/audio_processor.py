import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from pathlib import Path
import soundfile as sf

# Use Agg backend for matplotlib to avoid GUI issues
matplotlib.use('Agg')

class AudioProcessor:
    """Xử lý và phân tích audio"""
    
    def __init__(self):
        self.setup_matplotlib_style()
    
    def setup_matplotlib_style(self):
        """Cấu hình style cho matplotlib"""
        plt.style.use('default')
        plt.rcParams.update({
            'font.size': 10,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.titlesize': 16,
            'font.family': 'sans-serif'
        })
    
    def get_audio_info(self, audio_path):
        """Lấy thông tin audio"""
        try:
            # Sử dụng soundfile để lấy thông tin nhanh hơn
            info = sf.info(audio_path)
            
            return {
                'sample_rate': info.samplerate,
                'duration': info.duration,
                'channels': info.channels,
                'format': info.format,
                'subtype': info.subtype
            }
        except Exception as e:
            # Fallback to librosa
            try:
                y, sr = librosa.load(audio_path, sr=None)
                return {
                    'sample_rate': sr,
                    'duration': len(y) / sr,
                    'channels': 1,  # librosa loads as mono by default
                    'format': 'Unknown',
                    'subtype': 'Unknown'
                }
            except Exception:
                raise Exception(f"Không thể đọc thông tin audio: {str(e)}")
    
    def plot_frequency(self, audio_path, freq_min=0, freq_max=None, use_db=True, save_path=None):
        """Tạo biểu đồ tần số"""
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=None, mono=True)
            
            # Tính FFT
            N = len(y)
            y_fft = np.fft.rfft(y)
            freq = np.fft.rfftfreq(N, d=1/sr)
            
            magnitude = np.abs(y_fft)
            
            # Chuyển đổi sang dB nếu cần
            if use_db:
                magnitude = 20 * np.log10(magnitude + 1e-12)
            
            # Giới hạn tần số
            if freq_max is None:
                freq_max = sr / 2
            
            mask = (freq >= freq_min) & (freq <= freq_max)
            freq_filtered = freq[mask]
            mag_filtered = magnitude[mask]
            
            # Tạo plot
            fig, ax = plt.subplots(figsize=(12, 6))
            
            ax.plot(freq_filtered, mag_filtered, linewidth=0.8, alpha=0.9, color='#2E86C1')
            ax.fill_between(freq_filtered, mag_filtered, alpha=0.3, color='#5DADE2')
            
            ax.set_xlabel("Tần số (Hz)", fontweight='bold')
            ax.set_ylabel("Magnitude (dB)" if use_db else "Magnitude", fontweight='bold')
            ax.set_title(f"Phổ tần số: {freq_min} Hz → {freq_max} Hz", fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#F8F9FA')
            
            # Thêm thông tin thống kê
            if use_db:
                max_db = np.max(mag_filtered)
                max_freq = freq_filtered[np.argmax(mag_filtered)]
                ax.axvline(max_freq, color='red', linestyle='--', alpha=0.7, 
                          label=f'Peak: {max_freq:.1f} Hz ({max_db:.1f} dB)')
                ax.legend()
            
            plt.tight_layout()
            
            # Lưu file nếu cần
            if save_path:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
            return fig
            
        except Exception as e:
            raise Exception(f"Lỗi khi tạo biểu đồ tần số: {str(e)}")
    
    def plot_spectrogram(self, audio_path, sr=None, n_fft=2048, hop_length=512, 
                        freq_max=None, save_path=None):
        """Tạo spectrogram"""
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=sr, mono=True)
            
            # Tính STFT
            S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
            S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)
            
            # Tạo plot
            fig, ax = plt.subplots(figsize=(12, 8))
            
            img = librosa.display.specshow(
                S_db,
                sr=sr,
                hop_length=hop_length,
                x_axis='time',
                y_axis='hz',
                ax=ax,
                cmap='magma'
            )
            
            # Colorbar
            cbar = plt.colorbar(img, ax=ax, format="%+2.0f dB")
            cbar.set_label('Magnitude (dB)', fontweight='bold')
            
            ax.set_xlabel("Thời gian (s)", fontweight='bold')
            ax.set_ylabel("Tần số (Hz)", fontweight='bold')
            ax.set_title("Spectrogram (dB scale)", fontweight='bold', pad=20)
            
            # Giới hạn tần số nếu cần
            if freq_max is not None:
                ax.set_ylim(0, freq_max)
            
            plt.tight_layout()
            
            # Lưu file nếu cần
            if save_path:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
            return fig
            
        except Exception as e:
            raise Exception(f"Lỗi khi tạo spectrogram: {str(e)}")
    
    def analyze_frequency_peaks(self, audio_path, freq_min=20, freq_max=20000, 
                               threshold_db=-40, num_peaks=10):
        """Phân tích các peak tần số"""
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=None, mono=True)
            
            # Tính FFT
            N = len(y)
            y_fft = np.fft.rfft(y)
            freq = np.fft.rfftfreq(N, d=1/sr)
            
            magnitude_db = 20 * np.log10(np.abs(y_fft) + 1e-12)
            
            # Lọc theo tần số
            mask = (freq >= freq_min) & (freq <= freq_max)
            freq_filtered = freq[mask]
            mag_filtered = magnitude_db[mask]
            
            # Tìm peaks
            from scipy.signal import find_peaks
            
            peaks, properties = find_peaks(
                mag_filtered, 
                height=threshold_db,
                distance=len(mag_filtered) // 100  # Khoảng cách tối thiểu giữa peaks
            )
            
            # Lấy top peaks
            if len(peaks) > 0:
                peak_heights = mag_filtered[peaks]
                top_indices = np.argsort(peak_heights)[-num_peaks:][::-1]
                
                results = []
                for i in top_indices:
                    if i < len(peaks):
                        peak_idx = peaks[i]
                        results.append({
                            'frequency': freq_filtered[peak_idx],
                            'magnitude_db': mag_filtered[peak_idx],
                            'magnitude_linear': 10 ** (mag_filtered[peak_idx] / 20)
                        })
                
                return sorted(results, key=lambda x: x['magnitude_db'], reverse=True)
            else:
                return []
                
        except Exception as e:
            raise Exception(f"Lỗi khi phân tích peaks: {str(e)}")