from utils.processor import video_to_audio, check_type
from utils.plotter import plot_freq, plot_spectrogram

file_path = input("Enter the path to the media file (audio/video): ").strip()
file_type = check_type(file_path)
if file_type == "video":
    file_path = video_to_audio(file_path)

print(f"Processing {file_type} file: {file_path}")
plot_freq(file_path, freq_min=20, freq_max=20000, use_db=True, save_path="results/plots/freq_plot.png")
plot_spectrogram(file_path, freq_max=8000, save_path="results/plots/spectrogram.png")


