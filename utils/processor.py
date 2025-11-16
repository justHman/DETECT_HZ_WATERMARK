import os
import av

def video_to_audio(video_path, output_audio_path="data/tmp.aac"):
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

    try:
        container = av.open(video_path)
        
        # Tạo tệp âm thanh đầu ra
        with open(output_audio_path, "wb") as audio_file:
            # Duyệt qua các gói dữ liệu trong luồng âm thanh
            for frame in container.decode(audio=0):  # Giả sử luồng âm thanh đầu tiên
                audio_file.write(frame.planes[0].to_bytes())
        
        print(f"Âm thanh đã được lưu tại: {output_audio_path}")
        return output_audio_path
    except Exception as e:
        print(f"Lỗi khi chuyển đổi video thành âm thanh: {e}")
    

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
    
    
