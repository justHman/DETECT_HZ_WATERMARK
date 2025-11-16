"""
CSS styling cho giao diện Streamlit
Theme: Technology/Audio Analysis
"""

def get_custom_css():
    """
    Trả về custom CSS cho giao diện Streamlit.
    """
    return """
    <style>
    /* Import font công nghệ */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        font-family: 'Roboto', sans-serif;
    }
    
    /* Header styles */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00d4ff !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
    
    h1 {
        font-size: 3rem !important;
        font-weight: 900 !important;
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(90deg, #00d4ff, #7000ff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Card/Container styles */
    .stContainer, .element-container {
        background: rgba(26, 31, 58, 0.6);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* File uploader */
    .stFileUploader {
        background: rgba(0, 212, 255, 0.05);
        border: 2px dashed #00d4ff;
        border-radius: 10px;
        padding: 30px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        background: rgba(0, 212, 255, 0.1);
        border-color: #7000ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #7000ff 100%);
        color: white;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(112, 0, 255, 0.6);
        background: linear-gradient(135deg, #7000ff 0%, #00d4ff 100%);
    }
    
    /* Input fields */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid #00d4ff;
        border-radius: 8px;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #7000ff;
        box-shadow: 0 0 10px rgba(112, 0, 255, 0.5);
    }
    
    /* Checkbox */
    .stCheckbox {
        color: #00d4ff;
    }
    
    .stCheckbox > label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(0, 212, 255, 0.1);
        border-radius: 10px;
        border: 1px solid #00d4ff;
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
    }
    
    .streamlit-expanderContent {
        background: rgba(26, 31, 58, 0.8);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 0 0 10px 10px;
    }
    
    /* Tables */
    table {
        background: rgba(26, 31, 58, 0.8);
        border-radius: 10px;
        overflow: hidden;
        border-collapse: collapse;
        width: 100%;
    }
    
    th {
        background: linear-gradient(135deg, #00d4ff 0%, #7000ff 100%);
        color: white;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        padding: 15px;
        text-align: left;
        border: none;
    }
    
    td {
        background: rgba(0, 212, 255, 0.05);
        color: #ffffff;
        padding: 12px 15px;
        border-bottom: 1px solid rgba(0, 212, 255, 0.1);
    }
    
    tr:hover td {
        background: rgba(0, 212, 255, 0.15);
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess, .stInfo, .stWarning {
        background: rgba(0, 212, 255, 0.1);
        border-left: 4px solid #00d4ff;
        border-radius: 5px;
        padding: 15px;
        color: #ffffff;
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f3a 0%, #0a0e27 100%);
        border-right: 2px solid rgba(0, 212, 255, 0.3);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #00d4ff;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffffff;
        font-weight: 500;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, transparent);
        margin: 30px 0;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #00d4ff !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 31, 58, 0.5);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff 0%, #7000ff 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7000ff 0%, #00d4ff 100%);
    }
    
    /* Glow effect for images */
    img {
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    img:hover {
        box-shadow: 0 0 30px rgba(112, 0, 255, 0.5);
        transform: scale(1.02);
    }
    
    /* Labels */
    label {
        color: #00d4ff !important;
        font-weight: 500 !important;
        font-family: 'Roboto', sans-serif !important;
    }
    
    /* Code blocks */
    code {
        background: rgba(0, 212, 255, 0.1);
        color: #00d4ff;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }
    
    /* Tooltips */
    .stTooltipIcon {
        color: #00d4ff;
    }
    </style>
    """
