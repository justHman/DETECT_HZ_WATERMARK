import os
import tempfile
import shutil
import subprocess
from pathlib import Path

class FileHandler:
    """Xử lý file upload và conversion"""
    
    def __init__(self):
        self.temp_dir = "data/temp"
        self.audio_dir = "data/audio"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Tạo các thư mục cần thiết"""
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs("results/plots", exist_ok=True)
    
    def save_uploaded_file(self, uploaded_file):
        """Lưu file được upload"""
        try:
            file_path = os.path.join(self.temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path
        except Exception as e:
            raise Exception(f"Lỗi khi lưu file: {str(e)}")
    
    def check_file_type(self, file_path):
        """Kiểm tra loại file"""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}
        audio_extensions = {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"}
        
        if ext in video_extensions:
            return "video"
        elif ext in audio_extensions:
            return "audio"
        else:
            return "unknown"
    
    def video_to_audio(self, video_path):
        """Chuyển đổi video thành audio"""
        try:
            # Tạo tên file output
            video_name = Path(video_path).stem
            output_path = os.path.join(self.audio_dir, f"{video_name}.wav")
            
            # Lệnh ffmpeg
            command = [
                "ffmpeg",
                "-i", video_path,
                "-vn",  # Bỏ video
                "-acodec", "pcm_s16le",  # Codec audio
                "-ar", "44100",  # Sample rate
                "-ac", "2",  # Stereo
                "-y",  # Overwrite output file
                output_path
            ]
            
            # Chạy lệnh ffmpeg
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True,
                timeout=300  # Timeout 5 phút
            )
            
            if result.returncode == 0:
                return output_path
            else:
                raise Exception(f"FFmpeg error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            raise Exception("Timeout khi chuyển đổi video (>5 phút)")
        except FileNotFoundError:
            raise Exception("Không tìm thấy FFmpeg. Vui lòng cài đặt FFmpeg và thêm vào PATH")
        except Exception as e:
            raise Exception(f"Lỗi khi chuyển đổi video: {str(e)}")
    
    def cleanup_temp_files(self):
        """Dọn dẹp file tạm"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                os.makedirs(self.temp_dir, exist_ok=True)
        except Exception:
            pass  # Ignore cleanup errors