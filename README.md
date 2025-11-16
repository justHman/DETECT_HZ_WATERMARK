# 🎵 Audio Frequency Analyzer

Công cụ phân tích tần số âm thanh chuyên nghiệp với giao diện Streamlit hiện đại.

## ✨ Tính năng

- 📁 **Upload Files**: Hỗ trợ cả file audio và video
- 📊 **Frequency Analysis**: Phân tích phổ tần số chi tiết  
- 📈 **Spectrogram**: Tạo spectrogram với nhiều tùy chọn
- ⚙️ **Tùy chỉnh tham số**: Điều chỉnh freq_min, freq_max, use_db
- 💾 **Lưu kết quả**: Tự động lưu plots và cho phép tải về
- 🎨 **Giao diện đẹp**: Thiết kế hiện đại với chủ đề công nghệ

## 🚀 Cài đặt và chạy

### 1. Clone repository
```bash
git clone https://github.com/justHman/DETECT_HZ_WATERMARK.git
cd DETECT_HZ_WATERMARK
```

### 2. Cài đặt thư viện

#### 🪟 Windows
```bash
# Sử dụng pip
pip install -r requirements.txt

# Hoặc cài từng package
pip install streamlit librosa matplotlib numpy soundfile scipy ffmpeg-python
```

#### 🍎 macOS
```bash
# Cài đặt Homebrew (nếu chưa có)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài đặt Python dependencies
pip3 install -r requirements.txt
```

### 3. Cài đặt FFmpeg (Bắt buộc cho video processing)

#### 🪟 Windows
```bash
# Cách 1: Tải manual
# Tải từ: https://ffmpeg.org/download.html
# Giải nén và thêm vào System PATH

# Cách 2: Sử dụng Chocolatey
choco install ffmpeg

# Cách 3: Sử dụng conda
conda install -c conda-forge ffmpeg
```

#### 🍎 macOS
```bash
# Cách 1: Homebrew (khuyến nghị)
brew install ffmpeg

# Cách 2: MacPorts
sudo port install ffmpeg

# Kiểm tra cài đặt
ffmpeg -version
```

### 4. Chạy ứng dụng

#### Cách 1: Streamlit trực tiếp
```bash
# Windows
streamlit run app/streamlit_app.py

# macOS/Linux
streamlit run app/streamlit_app.py
# Hoặc
python3 -m streamlit run app/streamlit_app.py
```

#### Cách 2: Script tự động
```bash
# Windows
python run_app.py

# macOS/Linux
python3 run_app.py
```

**🌐 Ứng dụng sẽ mở tại**: http://localhost:8501

### 5. Khắc phục sự cố macOS

#### Lỗi permission denied
```bash
# Cấp quyền thực thi
chmod +x run_app.py

# Sử dụng python3 thay vì python
python3 run_app.py
```

#### Lỗi SSL certificate (macOS)
```bash
# Cài đặt certificates
/Applications/Python\ 3.x/Install\ Certificates.command

# Hoặc sử dụng conda
conda install certifi
```

#### Lỗi librosa trên M1/M2 Mac
```bash
# Sử dụng conda-forge
conda install -c conda-forge librosa

# Hoặc cài đặt dependencies riêng
brew install portaudio
pip3 install librosa
```

## 📋 Hướng dẫn sử dụng

1. **Upload File**: Chọn file audio/video từ sidebar
2. **Cài đặt tham số**:
   - `freq_min`: Tần số tối thiểu (Hz)
   - `freq_max`: Tần số tối đa (Hz) 
   - `use_db`: Hiển thị theo thang dB
   - `save_plots`: Lưu biểu đồ vào thư mục results/
3. **Xem kết quả**: Biểu đồ tần số và spectrogram
4. **Tải về**: Download plots đã tạo

## 📊 Bảng tham khảo

### Sample Rate và tần số tối đa

| Sample Rate | Max tần số FFT thấy | 30 kHz có thấy không? |
| ----------- | ------------------- | --------------------- |
| 44100 Hz    | 22050 Hz            | ❌ Không               |
| 48000 Hz    | 24000 Hz            | ❌ Không               |
| 96000 Hz    | 48000 Hz            | ✔️ Có                 |
| 192000 Hz   | 96000 Hz            | ✔️ Có                 |

### Mức độ âm thanh (dB)

| Mức               | Giá trị (dB) | Ý nghĩa                    |
| ----------------- | ------------ | -------------------------- |
| **Rất to**        | +10 → +60 dB | Rất rõ, peak mạnh          |
| **To**            | 0 → +10 dB   | Rõ ràng                    |
| **Vừa**           | -20 → 0 dB   | Nghe được nếu không bị che |
| **Nhỏ**           | -40 → -20 dB | Nghe khó, FFT thấy rõ      |
| **Rất nhỏ**       | -80 → -40 dB | Hầu như không nghe thấy    |
| **Không tồn tại** | < -100 dB    | Gần noise floor            |

## 🛠️ Cấu trúc project

```
visualize_freq_system/
├── app/
│   ├── streamlit_app.py    # Streamlit main app
│   ├── style.css          # CSS styling
│   └── backend/
│       ├── audio_processor.py  # Audio processing
│       └── file_handler.py     # File handling
├── utils/
│   ├── processor.py       # Original utilities
│   └── plotter.py         # Original plotting
├── data/
│   ├── audio/            # Converted audio files
│   └── temp/             # Temporary uploads
├── results/
│   └── plots/            # Generated plots
├── main.py               # Original CLI script
└── README.md
```

## 🎯 Supported formats

**Audio**: MP3, WAV, AAC, FLAC, OGG, M4A
**Video**: MP4, AVI, MOV, MKV, FLV, WMV, WEBM

## 🔧 Troubleshooting

### FFmpeg not found
```bash
# Windows - Thêm FFmpeg vào PATH hoặc:
conda install ffmpeg
# hoặc
pip install ffmpeg-python
```

### Lỗi import librosa
```bash
pip install librosa soundfile
# Trên Windows có thể cần:
pip install librosa[display]
```

### Port đã được sử dụng
```bash
streamlit run app/streamlit_app.py --server.port 8502
```

## 📞 Liên hệ

- GitHub: [justHman](https://github.com/justHman)
- Repository: [DETECT_HZ_WATERMARK](https://github.com/justHman/DETECT_HZ_WATERMARK)

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết.

---

**Phát triển bởi**: justHman  
**Version**: 1.0.0  
**Last Updated**: November 2024