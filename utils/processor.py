import os
import subprocess

def video_to_audio(video_path, output_audio_path="data/audio/tmp.aac"):
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

    try:
        # Lệnh ffmpeg để trích xuất âm thanh
        command = [
            "ffmpeg",
            "-i", video_path,  # Đầu vào là tệp video
            "-vn",             # Bỏ phần video
            "-acodec", "copy", # Giữ nguyên codec âm thanh
            output_audio_path  # Đầu ra là tệp âm thanh
        ]
        # Chạy lệnh ffmpeg
        subprocess.run(command, check=True)
        print(f"Âm thanh đã được lưu tại: {output_audio_path}")
        return output_audio_path
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi trích xuất âm thanh: {e}")
        return None
    
def check_type(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"}
    audio_extensions = {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"}

    if ext in video_extensions:
        return "video"
    elif ext in audio_extensions:
        return "audio"
    else:
        return "unknown"
    
if __name__ == "__main__":
    video_file = r"D:\Downloads\7229528504080.mp4"
    audio_file = video_to_audio(video_file, output_audio_path="data/output_audio.aac")
    print(f"Extracted audio file: {audio_file}")
    
    
