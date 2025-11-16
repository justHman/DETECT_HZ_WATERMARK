import streamlit as st
from css import get_custom_css
from backend import process_uploaded_file, generate_plots, get_audio_info


def show_sample_rate_info():
    """Hiển thị bảng thông tin Sample Rate và tần số FFT."""
    st.markdown("### 📊 Bảng thông tin Sample Rate")
    
    sample_rate_data = """
    | Sample Rate | Max tần số FFT thấy | 30 kHz có thấy không? |
    |-------------|---------------------|----------------------|
    | 44100 Hz    | 22050 Hz            | ❌ Không              |
    | 48000 Hz    | 24000 Hz            | ❌ Không              |
    | 96000 Hz    | 48000 Hz            | ✔️ Có                |
    | 192000 Hz   | 96000 Hz            | ✔️ Có                |
    """
    
    st.markdown(sample_rate_data)
    
    st.info("""
    **💡 Lưu ý:** Tần số tối đa mà FFT có thể phát hiện là **Sample Rate / 2** (Nyquist frequency).
    Để phát hiện tần số 30 kHz, bạn cần sample rate ít nhất 60000 Hz.
    """)


def show_db_level_info():
    """Hiển thị bảng thông tin mức dB."""
    st.markdown("### 🔊 Bảng thông tin mức dB")
    
    db_level_data = """
    | Mức               | Giá trị (dB) | Ý nghĩa                    |
    |-------------------|--------------|----------------------------|
    | **Rất to**        | +10 → +60 dB | Rất rõ, peak mạnh          |
    | **To**            | 0 → +10 dB   | Rõ ràng                    |
    | **Vừa**           | -20 → 0 dB   | Nghe được nếu không bị che |
    | **Nhỏ**           | -40 → -20 dB | Nghe khó, FFT thấy rõ      |
    | **Rất nhỏ**       | -80 → -40 dB | Hầu như không nghe thấy    |
    | **Không tồn tại** | < -100 dB    | Gần noise floor            |
    """
    
    st.markdown(db_level_data)
    
    st.info("""
    **💡 Lưu ý:** Thang đo dB (decibel) là thang đo logarit, giúp biểu diễn các giá trị biên độ 
    rất lớn hoặc rất nhỏ một cách dễ nhìn hơn. Giá trị 0 dB thường được chuẩn hóa theo giá trị peak.
    """)


def render_sidebar():
    """Render sidebar với các tùy chọn cấu hình."""
    with st.sidebar:
        st.markdown("# ⚙️ Cấu hình")
        st.markdown("---")
        
        # Tham số tần số
        st.markdown("### 🎵 Tham số tần số")
        freq_min = st.number_input(
            "Tần số tối thiểu (Hz)",
            min_value=0,
            max_value=100000,
            value=20,
            step=10,
            help="Tần số thấp nhất để hiển thị trên biểu đồ"
        )
        
        freq_max = st.number_input(
            "Tần số tối đa (Hz)",
            min_value=100,
            max_value=200000,
            value=20000,
            step=100,
            help="Tần số cao nhất để hiển thị trên biểu đồ"
        )
        
        st.markdown("---")
        
        # Tham số hiển thị
        st.markdown("### 📈 Tham số hiển thị")
        use_db = st.checkbox(
            "Sử dụng thang đo dB",
            value=True,
            help="Hiển thị biên độ theo thang decibel (logarit)"
        )
        
        save_plots = st.checkbox(
            "Lưu biểu đồ vào thư mục results/plots",
            value=False,
            help="Lưu các biểu đồ vào thư mục results/plots thay vì tạm thời"
        )
        
        st.markdown("---")
        
        # Thông tin hướng dẫn
        with st.expander("ℹ️ Hướng dẫn sử dụng"):
            st.markdown("""
            1. **Upload file**: Tải lên file video hoặc audio
            2. **Cấu hình tham số**: Điều chỉnh các tham số bên trái
            3. **Xử lý**: Nhấn nút "🚀 Phân tích tần số"
            4. **Xem kết quả**: Xem biểu đồ và thông tin chi tiết
            
            **Định dạng hỗ trợ:**
            - Video: MP4, AVI, MOV, MKV, FLV, WMV
            - Audio: MP3, WAV, AAC, FLAC, OGG, M4A
            """)
        
        st.markdown("---")
        st.markdown("### 📚 Tài liệu tham khảo")
        
        with st.expander("📊 Thông tin Sample Rate"):
            show_sample_rate_info()
        
        with st.expander("🔊 Thông tin mức dB"):
            show_db_level_info()
    
    return freq_min, freq_max, use_db, save_plots


def render_main_content():
    """Render nội dung chính của ứng dụng."""
    # Header
    st.markdown("# 🎵 Audio Frequency Analyzer")
    st.markdown("### Phân tích và trực quan hóa phổ tần số âm thanh")
    st.markdown("---")
    
    # File uploader
    st.markdown("## 📁 Tải lên file")
    uploaded_file = st.file_uploader(
        "Chọn file video hoặc audio để phân tích",
        type=["mp4", "avi", "mov", "mkv", "flv", "wmv", "mp3", "wav", "aac", "flac", "ogg", "m4a"],
        help="Hỗ trợ các định dạng video và audio phổ biến"
    )
    
    return uploaded_file


def render_analysis_section(uploaded_file, freq_min, freq_max, use_db, save_plots):
    """Render phần phân tích và hiển thị kết quả."""
    
    if uploaded_file is not None:
        # Hiển thị thông tin file
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Tên file", uploaded_file.name)
        with col2:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.metric("💾 Kích thước", f"{file_size_mb:.2f} MB")
        with col3:
            file_type = uploaded_file.name.split('.')[-1].upper()
            st.metric("📝 Định dạng", file_type)
        
        st.markdown("---")
        
        # Nút phân tích
        if st.button("🚀 Phân tích tần số", type="primary", use_container_width=True):
            with st.spinner("🔄 Đang xử lý file..."):
                try:
                    # Xử lý file upload
                    audio_path, detected_type, original_filename = process_uploaded_file(uploaded_file)
                    
                    st.success(f"✅ Đã xử lý file {detected_type}: {original_filename}")
                    
                    # Lấy thông tin audio
                    audio_info = get_audio_info(audio_path)
                    
                    # Hiển thị thông tin audio
                    st.markdown("### 🎧 Thông tin Audio")
                    info_col1, info_col2, info_col3, info_col4 = st.columns(4)
                    
                    with info_col1:
                        st.metric("📊 Sample Rate", f"{audio_info['sample_rate']} Hz")
                    with info_col2:
                        st.metric("⏱️ Thời lượng", f"{audio_info['duration']:.2f} s")
                    with info_col3:
                        st.metric("🔊 Số kênh", audio_info['channels'])
                    with info_col4:
                        st.metric("🎯 Max FFT Freq", f"{audio_info['max_freq_fft']:.0f} Hz")
                    
                    # Kiểm tra xem có thể phát hiện tần số mong muốn không
                    if freq_max > audio_info['max_freq_fft']:
                        st.warning(f"""
                        ⚠️ **Cảnh báo**: Tần số tối đa bạn chọn ({freq_max} Hz) lớn hơn tần số Nyquist 
                        ({audio_info['max_freq_fft']:.0f} Hz). Các tần số trên {audio_info['max_freq_fft']:.0f} Hz 
                        sẽ không được phát hiện chính xác.
                        """)
                    
                    st.markdown("---")
                    
                    # Tạo các biểu đồ
                    with st.spinner("📊 Đang tạo biểu đồ..."):
                        freq_plot_path, spectrogram_path = generate_plots(
                            audio_path, freq_min, freq_max, use_db, save_plots
                        )
                    
                    st.success("✅ Hoàn thành phân tích!")
                    
                    # Hiển thị biểu đồ
                    st.markdown("### 📈 Biểu đồ phổ tần số")
                    st.image(freq_plot_path, use_container_width=True)
                    
                    st.markdown("### 🌈 Spectrogram")
                    st.image(spectrogram_path, use_container_width=True)
                    
                    # Thông tin lưu file
                    if save_plots:
                        st.info(f"""
                        💾 **Biểu đồ đã được lưu tại:**
                        - Phổ tần số: `{freq_plot_path}`
                        - Spectrogram: `{spectrogram_path}`
                        """)
                    
                except Exception as e:
                    st.error(f"❌ Lỗi khi xử lý file: {str(e)}")
                    st.exception(e)
    else:
        # Hướng dẫn khi chưa upload file
        st.info("""
        👆 **Bắt đầu bằng cách tải lên file video hoặc audio**
        
        Ứng dụng sẽ:
        - Tự động chuyển đổi video thành audio (nếu cần)
        - Phân tích phổ tần số sử dụng FFT
        - Tạo biểu đồ trực quan và spectrogram
        - Hiển thị thông tin chi tiết về file audio
        """)
        
        # Hiển thị các bảng thông tin
        col1, col2 = st.columns(2)
        
        with col1:
            show_sample_rate_info()
        
        with col2:
            show_db_level_info()


def render_footer():
    """Render footer."""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #00d4ff; font-family: Orbitron;'>
        <p>🎵 Audio Frequency Analyzer | Powered by Streamlit 🚀</p>
        <p style='font-size: 0.9em; opacity: 0.8;'>
            Built with ❤️ using Python, Librosa, and FFT
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Hàm main để render toàn bộ giao diện."""
    # Cấu hình page
    st.set_page_config(
        page_title="Audio Frequency Analyzer",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Render sidebar và lấy tham số
    freq_min, freq_max, use_db, save_plots = render_sidebar()
    
    # Render main content
    uploaded_file = render_main_content()
    
    # Render analysis section
    render_analysis_section(uploaded_file, freq_min, freq_max, use_db, save_plots)
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
