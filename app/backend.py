import os
import sys
import tempfile
import streamlit as st
from pathlib import Path

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))

from utils.processor import video_to_audio, check_type
from utils.plotter import plot_freq, plot_spectrogram


def process_uploaded_file(uploaded_file):
    """
    Xử lý file upload và trả về đường dẫn file audio.
    
    Args:
        uploaded_file: File upload từ Streamlit
        
    Returns:
        tuple: (audio_path, file_type, original_filename)
    """
    # Tạo thư mục tạm để lưu file upload
    temp_dir = tempfile.gettempdir()
    original_filename = uploaded_file.name
    file_extension = os.path.splitext(original_filename)[1]
    
    # Lưu file upload vào thư mục tạm
    temp_file_path = os.path.join(temp_dir, f"uploaded_{original_filename}")
    
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Kiểm tra loại file
    file_type = check_type(temp_file_path)
    
    # Nếu là video, chuyển đổi sang audio
    if file_type == "video":
        audio_path = video_to_audio(temp_file_path, output_audio_path=os.path.join(temp_dir, "temp_audio.aac"))
    elif file_type == "audio":
        audio_path = temp_file_path
    else:
        raise ValueError(f"Định dạng file không được hỗ trợ: {file_extension}")
    
    return audio_path, file_type, original_filename


def generate_plots(audio_path, freq_min, freq_max, use_db, save_plots=False):
    """
    Tạo các biểu đồ tần số và spectrogram.
    
    Args:
        audio_path: Đường dẫn file audio
        freq_min: Tần số tối thiểu (Hz)
        freq_max: Tần số tối đa (Hz)
        use_db: Sử dụng thang đo dB hay không
        save_plots: Lưu biểu đồ hay không
        
    Returns:
        tuple: (freq_plot_path, spectrogram_path)
    """
    import matplotlib
    matplotlib.use('Agg')  # Sử dụng backend không cần GUI
    import matplotlib.pyplot as plt
    
    # Đường dẫn lưu plots
    if save_plots:
        freq_plot_path = "results/plots/freq_plot.png"
        spectrogram_path = "results/plots/spectrogram.png"
        os.makedirs("results/plots", exist_ok=True)
    else:
        temp_dir = tempfile.gettempdir()
        freq_plot_path = os.path.join(temp_dir, "freq_plot.png")
        spectrogram_path = os.path.join(temp_dir, "spectrogram.png")
    
    # Tạo biểu đồ tần số
    plt.clf()
    plot_freq(audio_path, freq_min=freq_min, freq_max=freq_max, use_db=use_db, save_path=freq_plot_path)
    plt.close('all')
    
    # Tạo spectrogram
    plt.clf()
    plot_spectrogram(audio_path, freq_max=freq_max, save_path=spectrogram_path)
    plt.close('all')
    
    return freq_plot_path, spectrogram_path


def get_audio_info(audio_path):
    """
    Lấy thông tin về file audio.
    
    Args:
        audio_path: Đường dẫn file audio
        
    Returns:
        dict: Thông tin audio (sample_rate, duration, channels)
    """
    import librosa
    
    y, sr = librosa.load(audio_path, sr=None, mono=False)
    duration = librosa.get_duration(y=y, sr=sr)
    
    # Kiểm tra số kênh
    if y.ndim == 1:
        channels = 1
    else:
        channels = y.shape[0]
    
    return {
        "sample_rate": sr,
        "duration": duration,
        "channels": channels,
        "max_freq_fft": sr / 2
    }
