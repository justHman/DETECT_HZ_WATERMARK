"""
Demo script để test Streamlit app
"""
import subprocess
import sys
import os

def install_requirements():
    """Cài đặt requirements"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Đã cài đặt thành công các thư viện cần thiết!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi cài đặt requirements: {e}")
        return False
    return True

def check_ffmpeg():
    """Kiểm tra FFmpeg"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ FFmpeg đã được cài đặt!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  FFmpeg chưa được cài đặt. Video conversion có thể không hoạt động.")
        print("Hướng dẫn cài đặt FFmpeg:")
        print("- Windows: Tải từ https://ffmpeg.org/download.html")
        print("- macOS: brew install ffmpeg") 
        print("- Ubuntu: sudo apt install ffmpeg")
        return False

def run_streamlit():
    """Chạy Streamlit app"""
    try:
        print("🚀 Đang khởi động Streamlit app...")
        print("📱 App sẽ mở tại: http://localhost:8501")
        print("🔚 Nhấn Ctrl+C để dừng")
        
        # Chạy streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app/streamlit_app.py",
            "--server.headless=true",
            "--server.fileWatcherType=none",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Đã dừng ứng dụng!")
    except Exception as e:
        print(f"❌ Lỗi khi chạy Streamlit: {e}")

def main():
    print("🎵 Audio Frequency Analyzer - Demo Setup")
    print("=" * 50)
    
    # Kiểm tra thư mục hiện tại
    if not os.path.exists("app/streamlit_app.py"):
        print("❌ Không tìm thấy app/streamlit_app.py")
        print("Vui lòng chạy script từ thư mục gốc của project")
        return
    
    # Tạo thư mục cần thiết
    os.makedirs("data/temp", exist_ok=True)
    os.makedirs("data/audio", exist_ok=True)
    os.makedirs("results/plots", exist_ok=True)
    print("📁 Đã tạo các thư mục cần thiết")
    
    # Cài đặt requirements
    print("\n📦 Đang cài đặt thư viện...")
    if not install_requirements():
        return
    
    # Kiểm tra FFmpeg
    print("\n🔧 Đang kiểm tra FFmpeg...")
    check_ffmpeg()
    
    # Chạy app
    print("\n" + "=" * 50)
    run_streamlit()

if __name__ == "__main__":
    main()