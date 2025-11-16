import streamlit as st
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.audio_processor import AudioProcessor
from backend.file_handler import FileHandler

def load_css():
    """Load custom CSS"""
    with open('app/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    # Page config
    st.set_page_config(
        page_title="🎵 Audio Frequency Analyzer",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load CSS
    try:
        load_css()
    except FileNotFoundError:
        pass  # CSS file optional
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎵 Audio Frequency Analyzer</h1>
        <p>Phân tích tần số âm thanh từ video/audio files</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for parameters
    st.sidebar.markdown("## ⚙️ Cài đặt tham số")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "📁 Tải lên file audio/video",
        type=['mp3', 'wav', 'aac', 'flac', 'ogg', 'm4a', 'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'],
        help="Hỗ trợ các định dạng audio và video phổ biến"
    )
    
    # Parameters
    st.sidebar.markdown("### 🎛️ Tham số phân tích")
    
    freq_min = st.sidebar.number_input(
        "Tần số tối thiểu (Hz)",
        min_value=1,
        max_value=100000,
        value=20,
        step=10,
        help="Tần số thấp nhất để phân tích"
    )
    
    freq_max = st.sidebar.number_input(
        "Tần số tối đa (Hz)",
        min_value=freq_min + 1,
        max_value=200000,
        value=20000,
        step=100,
        help="Tần số cao nhất để phân tích"
    )
    
    use_db = st.sidebar.checkbox(
        "Sử dụng thang đo dB",
        value=True,
        help="Hiển thị magnitude theo thang decibel"
    )
    
    save_plots = st.sidebar.checkbox(
        "Lưu plots",
        value=True,
        help="Tự động lưu các biểu đồ vào thư mục results/plots/"
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col2:
            # Information tables
        st.markdown("### 📊 Bảng tham khảo")
        
        # Sample rate table
        st.markdown("#### Sample Rate và tần số tối đa")
        sample_rate_data = {
            "Sample Rate": ["44100 Hz", "48000 Hz", "96000 Hz", "192000 Hz"],
            "Max tần số FFT thấy": ["22050 Hz", "24000 Hz", "48000 Hz", "96000 Hz"],
            "30 kHz có thấy không?": ["❌ Không", "❌ Không", "✔️ Có", "✔️ Có"]
        }
        
        # Add custom styling for tables
        st.markdown("""
        <style>
        .table-container {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.table(sample_rate_data)
        
        # dB level table
        st.markdown("#### Mức độ âm thanh (dB)")
        db_data = {
            "Mức": ["**Rất to**", "**To**", "**Vừa**", "**Nhỏ**", "**Rất nhỏ**", "**Không tồn tại**"],
            "Giá trị (dB)": ["+10 → +60 dB", "0 → +10 dB", "-20 → 0 dB", "-40 → -20 dB", "-80 → -40 dB", "< -100 dB"],
            "Ý nghĩa": ["Rất rõ, peak mạnh", "Rõ ràng", "Nghe được nếu không bị che", "Nghe khó, FFT thấy rõ", "Hầu như không nghe thấy", "Gần noise floor"]
        }
        st.table(db_data)
    
    with col1:
        if uploaded_file is not None:
            # Process file
            with st.spinner('🔄 Đang xử lý file...'):
                try:
                    # Initialize processors
                    file_handler = FileHandler()
                    audio_processor = AudioProcessor()
                    
                    # Save uploaded file
                    file_path = file_handler.save_uploaded_file(uploaded_file)
                    
                    # Check file type and convert if needed
                    file_type = file_handler.check_file_type(file_path)
                    
                    if file_type == "video":
                        st.info("🎬 Phát hiện file video, đang trích xuất âm thanh...")
                        audio_path = file_handler.video_to_audio(file_path)
                    else:
                        audio_path = file_path
                    
                    if audio_path:
                        st.success(f"✅ Đã xử lý thành công file {file_type}!")
                        
                        # Display file info
                        file_info = audio_processor.get_audio_info(audio_path)
                        
                        st.markdown("### 📋 Thông tin file")
                        info_col1, info_col2, info_col3 = st.columns(3)
                        with info_col1:
                            st.metric("Sample Rate", f"{file_info['sample_rate']} Hz")
                        with info_col2:
                            st.metric("Độ dài", f"{file_info['duration']:.2f} s")
                        with info_col3:
                            st.metric("Channels", file_info['channels'])
                        
                        # Generate plots
                        st.markdown("### 📈 Kết quả phân tích")
                        
                        # Frequency plot
                        st.markdown("#### Biểu đồ tần số")
                        freq_fig = audio_processor.plot_frequency(
                            audio_path, 
                            freq_min=freq_min, 
                            freq_max=freq_max, 
                            use_db=use_db,
                            save_path="results/plots/freq_plot.png" if save_plots else None
                        )
                        st.pyplot(freq_fig)
                        
                        # Spectrogram
                        st.markdown("#### Spectrogram")
                        spec_fig = audio_processor.plot_spectrogram(
                            audio_path,
                            freq_max=freq_max,
                            save_path="results/plots/spectrogram.png" if save_plots else None
                        )
                        st.pyplot(spec_fig)
                        
                        # Download buttons
                        if save_plots:
                            st.markdown("### 💾 Tải về")
                            download_col1, download_col2 = st.columns(2)
                            
                            with download_col1:
                                if os.path.exists("results/plots/freq_plot.png"):
                                    with open("results/plots/freq_plot.png", "rb") as file:
                                        st.download_button(
                                            label="📊 Tải biểu đồ tần số",
                                            data=file.read(),
                                            file_name="frequency_plot.png",
                                            mime="image/png"
                                        )
                            
                            with download_col2:
                                if os.path.exists("results/plots/spectrogram.png"):
                                    with open("results/plots/spectrogram.png", "rb") as file:
                                        st.download_button(
                                            label="📈 Tải spectrogram",
                                            data=file.read(),
                                            file_name="spectrogram.png",
                                            mime="image/png"
                                        )
                    
                    else:
                        st.error("❌ Lỗi khi xử lý file")
                        
                except Exception as e:
                    st.error(f"❌ Lỗi: {str(e)}")
        
        else:
            # Welcome message
            st.markdown("""
            <div class="welcome-section">
                <h3>🚀 Chào mừng đến với Audio Frequency Analyzer!</h3>
                <p>Công cụ phân tích tần số âm thanh chuyên nghiệp, hỗ trợ:</p>
                <ul>
                    <li>📁 Upload file audio/video</li>
                    <li>📊 Phân tích phổ tần số</li>
                    <li>📈 Tạo spectrogram</li>
                    <li>⚙️ Tùy chỉnh tham số linh hoạt</li>
                    <li>💾 Lưu và tải về kết quả</li>
                </ul>
                <p><strong>Bắt đầu bằng cách tải lên file trong sidebar! 👈</strong></p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()