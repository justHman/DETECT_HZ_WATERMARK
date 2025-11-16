# 🎵 Audio Frequency Analyzer

Ứng dụng phân tích và trực quan hóa phổ tần số âm thanh sử dụng FFT (Fast Fourier Transform). Hỗ trợ cả file video và audio.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Tính năng

- 📁 **Upload đa định dạng**: Hỗ trợ video (MP4, AVI, MOV, MKV, FLV, WMV) và audio (MP3, WAV, AAC, FLAC, OGG, M4A)
- 🔄 **Tự động chuyển đổi**: Tự động trích xuất audio từ video
- 📊 **Phân tích FFT**: Phân tích phổ tần số sử dụng Fast Fourier Transform
- 📈 **Biểu đồ trực quan**: Hiển thị biểu đồ phổ tần số và spectrogram
- ⚙️ **Tùy chỉnh linh hoạt**: Điều chỉnh tham số tần số, thang đo dB, và nhiều hơn nữa
- 🎨 **Giao diện đẹp mắt**: Theme công nghệ hiện đại với hiệu ứng gradient và glow
- 💾 **Lưu kết quả**: Tùy chọn lưu biểu đồ vào thư mục

## 📋 Yêu cầu hệ thống

- Python 3.8 trở lên
- Git (để clone repository)

## 🚀 Cài đặt và chạy

### Bước 1: Clone repository

```bash
git clone https://github.com/justHman/DETECT_HZ_WATERMARK.git
cd DETECT_HZ_WATERMARK
```

### Bước 2: Tạo môi trường ảo (khuyến nghị)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Bước 3: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

**Hoặc cài đặt thủ công:**
```bash
pip install streamlit librosa numpy matplotlib av
```

### Bước 4: Chạy ứng dụng

```bash
streamlit run app\layout.py
```

Ứng dụng sẽ tự động mở trong trình duyệt tại địa chỉ: `http://localhost:8501`

## 📖 Hướng dẫn sử dụng

1. **Tải lên file**: Click vào vùng upload để chọn file video hoặc audio
2. **Cấu hình tham số** (sidebar):
   - **Tần số tối thiểu**: Tần số thấp nhất hiển thị (mặc định: 20 Hz)
   - **Tần số tối đa**: Tần số cao nhất hiển thị (mặc định: 20000 Hz)
   - **Sử dụng thang đo dB**: Hiển thị biên độ theo decibel (mặc định: Bật)
   - **Lưu biểu đồ**: Lưu kết quả vào `results/plots/` (mặc định: Tắt)
3. **Phân tích**: Nhấn nút "🚀 Phân tích tần số"
4. **Xem kết quả**: Xem biểu đồ phổ tần số và spectrogram

## 📊 Thông tin kỹ thuật

### Sample Rate và tần số FFT

| Sample Rate | Max tần số FFT thấy | 30 kHz có thấy không? |
|-------------|---------------------|----------------------|
| 44100 Hz    | 22050 Hz            | ❌ Không              |
| 48000 Hz    | 24000 Hz            | ❌ Không              |
| 96000 Hz    | 48000 Hz            | ✔️ Có                |
| 192000 Hz   | 96000 Hz            | ✔️ Có                |

**Lưu ý:** Tần số tối đa mà FFT có thể phát hiện là **Sample Rate / 2** (Nyquist frequency).

### Mức độ dB

| Mức               | Giá trị (dB) | Ý nghĩa                    |
|-------------------|--------------|----------------------------|
| **Rất to**        | +10 → +60 dB | Rất rõ, peak mạnh          |
| **To**            | 0 → +10 dB   | Rõ ràng                    |
| **Vừa**           | -20 → 0 dB   | Nghe được nếu không bị che |
| **Nhỏ**           | -40 → -20 dB | Nghe khó, FFT thấy rõ      |
| **Rất nhỏ**       | -80 → -40 dB | Hầu như không nghe thấy    |
| **Không tồn tại** | < -100 dB    | Gần noise floor            |

## 📁 Cấu trúc dự án

```
visualize_freq_system/
├── app.py                 # Entry point chính
├── main.py                # Script CLI (không dùng cho Streamlit)
├── requirements.txt       # Danh sách thư viện
├── README.md             # File này
│
├── app/                  # Thư mục ứng dụng Streamlit
│   ├── layout.py        # Giao diện chính
│   ├── css.py           # CSS styling
│   └── backend.py       # Logic xử lý
│
├── utils/               # Thư mục tiện ích
│   ├── processor.py    # Xử lý video/audio
│   └── plotter.py      # Tạo biểu đồ
│
├── data/               # Thư mục dữ liệu
│   └── audio/         # File audio mẫu
│
└── results/           # Thư mục kết quả
    └── plots/        # Biểu đồ đã lưu
```

## 🔧 Thư viện sử dụng

- **Streamlit**: Framework web cho ứng dụng data science
- **Librosa**: Thư viện phân tích âm thanh
- **NumPy**: Tính toán số học
- **Matplotlib**: Tạo biểu đồ
- **PyAV**: Xử lý video/audio (trích xuất audio từ video)

## 🐛 Xử lý lỗi thường gặp

### Lỗi: `ModuleNotFoundError`
**Giải pháp**: Đảm bảo đã cài đặt đầy đủ thư viện:
```bash
pip install -r requirements.txt
```

### Lỗi: Không thể trích xuất audio từ video
**Giải pháp**: Kiểm tra xem file video có luồng audio hợp lệ không.

### Lỗi: Tần số quá cao không hiển thị
**Giải pháp**: Sample rate của file audio phải ít nhất gấp đôi tần số muốn phân tích (Nyquist theorem).

## 📝 Ghi chú

- File upload sẽ được lưu tạm thời trong thư mục `temp` của hệ thống
- Biểu đồ mặc định không được lưu trừ khi bật tùy chọn "Lưu biểu đồ"
- Để phát hiện tần số cao (>22 kHz), cần file audio với sample rate cao (≥96 kHz)

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

## 📄 License

MIT License - Xem file `LICENSE` để biết thêm chi tiết.

## 👨‍💻 Tác giả

**justHman**
- GitHub: [@justHman](https://github.com/justHman)
- Repository: [DETECT_HZ_WATERMARK](https://github.com/justHman/DETECT_HZ_WATERMARK)

---

<div align="center">
  <p>🎵 Built with ❤️ using Python, Streamlit, and FFT 🚀</p>
  <p>⭐ Star this repo if you find it useful!</p>
</div>
