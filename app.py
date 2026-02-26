import streamlit as st
import pandas as pd
import os
import base64

# ==============================
# Page Config — أول سطر دايماً
# ==============================
st.set_page_config(
    page_title="3M4Media | Smart Marketing Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Session State Defaults
# ==============================
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en'
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

lang = st.session_state['lang']
theme = st.session_state['theme']

# ==============================
# Theme Colors
# ==============================
if theme == 'dark':
    BG = "#060B14"
    BG2 = "#0A0F1E"
    CARD = "rgba(0,180,180,0.06)"
    TEXT = "#FFFFFF"
    SUBTEXT = "#8899AA"
    BORDER = "rgba(0,180,180,0.2)"
    ACCENT = "#00B4B4"
    SIDEBAR_BG = "#040810"
else:
    BG = "#F0F4F8"
    BG2 = "#FFFFFF"
    CARD = "rgba(0,140,140,0.06)"
    TEXT = "#0A0F1E"
    SUBTEXT = "#556677"
    BORDER = "rgba(0,140,140,0.25)"
    ACCENT = "#007A7A"
    SIDEBAR_BG = "#E8EFF5"

# ==============================
# Background Image Style
# ==============================
bg_style = ""
if 'bg_image' in st.session_state:
    bg_style = f"""
    .stApp {{
        background-image: url("{st.session_state['bg_image']}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    .stApp::after {{
        content: '';
        position: fixed;
        inset: 0;
        background: rgba(6, 11, 20, 0.82);
        pointer-events: none;
        z-index: 0;
    }}
    """

# ==============================
# Dynamic CSS
# ==============================
st.markdown(f"<style>{bg_style}</style>", unsafe_allow_html=True)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* {{ font-family: 'DM Sans', sans-serif; }}
h1, h2, h3 {{ font-family: 'Syne', sans-serif !important; }}

#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem !important; }}

.stApp {{
    background-color: {BG} !important;
    color: {TEXT} !important;
    transition: all 0.4s ease;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {SIDEBAR_BG} 0%, {BG} 100%) !important;
    border-right: 1px solid {BORDER} !important;
}}

[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}

[data-testid="metric-container"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 16px !important;
    padding: 20px !important;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}

[data-testid="metric-container"]::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: {ACCENT};
    border-radius: 16px 0 0 16px;
}}

[data-testid="metric-container"]:hover {{
    border-color: {ACCENT} !important;
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,180,180,0.2);
}}

[data-testid="stMetricValue"] {{
    font-family: 'Syne', sans-serif !important;
    color: {ACCENT} !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}}

[data-testid="stMetricLabel"] {{
    color: {SUBTEXT} !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}}

.stButton > button {{
    background: linear-gradient(135deg, {ACCENT}, #007A7A) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(0,180,180,0.3) !important;
}}

.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,180,180,0.5) !important;
}}

[data-testid="stSelectbox"] > div {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
}}

[data-testid="stFileUploader"] {{
    background: {CARD} !important;
    border: 2px dashed {BORDER} !important;
    border-radius: 16px !important;
    padding: 24px !important;
}}

hr {{ border-color: {BORDER} !important; }}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: {ACCENT}; border-radius: 4px; }}

.stApp::before {{
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {ACCENT}, transparent);
    animation: scanline 3s linear infinite;
    z-index: 999;
}}

@keyframes scanline {{
    0% {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(100%); }}
}}
</style>
""", unsafe_allow_html=True)

# ==============================
# Translations
# ==============================
TRANSLATIONS = {
    "en": {
        "dashboard_title": "3M4Media Intelligence",
        "overview": "Overview",
        "client_view": "Client View",
        "ai_insights": "AI Insights",
        "upload_data": "Upload Data",
        "total_clicks": "Total Clicks",
        "total_impressions": "Total Impressions",
        "avg_roi": "Average ROI",
        "avg_ctr": "Average CTR",
        "avg_conversion": "Conversion Rate",
        "avg_cost": "Avg Acquisition Cost",
        "best_platform": "Best Platform",
        "best_campaign": "Best Campaign Goal",
        "campaign_performance": "Campaign Performance",
        "platform_comparison": "Platform Comparison",
        "monthly_trend": "Monthly ROI Trend",
        "ai_recommendation": "AI Recommendations",
        "prediction": "Next Month Prediction",
        "generate_report": "📄 Generate PDF Report",
        "select_client": "Select Client",
        "upload_csv": "Upload CSV or Parquet File",
        "dark_mode": "🌙 Dark",
        "light_mode": "☀️ Light",
        "theme": "Theme",
        "language": "Language",
        "live_stats": "Live Stats",
        "total_records": "Total Records",
        "active_clients": "Active Clients",
        "owner": "Founder & CEO",
        "follow_us": "Follow Us",
        "bg_image": "Background Image",
        "reset_bg": "🗑️ Reset Background",
        "bg_updated": "✅ Background updated!",
    },
    "ar": {
        "dashboard_title": "منصة 3M4Media الذكية",
        "overview": "نظرة عامة",
        "client_view": "عرض العميل",
        "ai_insights": "توصيات الذكاء الاصطناعي",
        "upload_data": "رفع بيانات",
        "total_clicks": "إجمالي النقرات",
        "total_impressions": "إجمالي المشاهدات",
        "avg_roi": "متوسط العائد",
        "avg_ctr": "متوسط النقر",
        "avg_conversion": "معدل التحويل",
        "avg_cost": "متوسط تكلفة الاكتساب",
        "best_platform": "أفضل منصة",
        "best_campaign": "أفضل هدف حملة",
        "campaign_performance": "أداء الحملات",
        "platform_comparison": "مقارنة المنصات",
        "monthly_trend": "الاتجاه الشهري للعائد",
        "ai_recommendation": "توصيات الذكاء الاصطناعي",
        "prediction": "توقعات الشهر الجاي",
        "generate_report": "📄 توليد تقرير PDF",
        "select_client": "اختر العميل",
        "upload_csv": "ارفع ملف CSV أو Parquet",
        "dark_mode": "🌙 داكن",
        "light_mode": "☀️ فاتح",
        "theme": "المظهر",
        "language": "اللغة",
        "live_stats": "إحصائيات مباشرة",
        "total_records": "إجمالي السجلات",
        "active_clients": "العملاء النشطين",
        "owner": "المؤسس والرئيس التنفيذي",
        "follow_us": "تابعنا",
        "bg_image": "صورة الخلفية",
        "reset_bg": "🗑️ إزالة الخلفية",
        "bg_updated": "✅ تم تحديث الخلفية!",
    }
}

def t(key):
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_data():
    df = pd.read_parquet('data/campaigns_clean.parquet')
    if 'CTR' not in df.columns:
        df['CTR'] = (df['Clicks'] / df['Impressions'] * 100).round(2)
    if 'Month' not in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month
    return df

df = load_data()

# ==============================
# Sidebar
# ==============================
with st.sidebar:

    # Logo
    if os.path.exists('assets/logo.png'):
        st.image('assets/logo.png', width=160)
    else:
        st.markdown(f"""
        <div style='text-align:center; padding:16px 0;'>
            <span style='font-family:Syne,sans-serif; font-size:2rem;
                         font-weight:800; color:{ACCENT};'>3M</span>
            <span style='font-family:Syne,sans-serif; font-size:1rem;
                         color:{SUBTEXT}; display:block; letter-spacing:4px;'>MEDIA</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Language Toggle
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.72rem; text-transform:uppercase; letter-spacing:2px; margin-bottom:4px;'>🌐 {t('language')}</p>", unsafe_allow_html=True)
    col_en, col_ar = st.columns(2)
    with col_en:
        if st.button("🇬🇧 EN", use_container_width=True):
            st.session_state['lang'] = 'en'
            st.rerun()
    with col_ar:
        if st.button("🇪🇬 AR", use_container_width=True):
            st.session_state['lang'] = 'ar'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Theme Toggle
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.72rem; text-transform:uppercase; letter-spacing:2px; margin-bottom:4px;'>🎨 {t('theme')}</p>", unsafe_allow_html=True)
    col_dark, col_light = st.columns(2)
    with col_dark:
        if st.button(t("dark_mode"), use_container_width=True):
            st.session_state['theme'] = 'dark'
            st.rerun()
    with col_light:
        if st.button(t("light_mode"), use_container_width=True):
            st.session_state['theme'] = 'light'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Background Image Upload
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.72rem; text-transform:uppercase; letter-spacing:2px; margin-bottom:4px;'>🖼️ {t('bg_image')}</p>", unsafe_allow_html=True)

    bg_image = st.file_uploader(
        "",
        type=['png', 'jpg', 'jpeg', 'webp'],
        label_visibility="collapsed",
        key="bg_uploader"
    )

    if bg_image is not None:
        bg_bytes = bg_image.read()
        bg_b64 = base64.b64encode(bg_bytes).decode()
        ext = bg_image.name.split('.')[-1]
        st.session_state['bg_image'] = f"data:image/{ext};base64,{bg_b64}"
        st.success(t("bg_updated"))

    if 'bg_image' in st.session_state:
        if st.button(t("reset_bg"), use_container_width=True):
            st.session_state.pop('bg_image', None)
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Navigation
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.72rem; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px;'>📌 Navigation</p>", unsafe_allow_html=True)

    pages = {
        f"📊 {t('overview')}": "overview",
        f"👤 {t('client_view')}": "client",
        f"🤖 {t('ai_insights')}": "ai",
        f"📁 {t('upload_data')}": "upload"
    }

    page = st.radio("", list(pages.keys()), label_visibility="collapsed")
    current_page = pages[page]

    st.markdown("<hr>", unsafe_allow_html=True)

    # Live Stats
    st.markdown(f"""
    <div style='background:{CARD}; border:1px solid {BORDER};
                border-radius:12px; padding:16px; margin-bottom:12px;'>
        <p style='color:{SUBTEXT}; font-size:0.7rem; text-transform:uppercase;
                  letter-spacing:2px; margin:0 0 10px 0;'>📡 {t('live_stats')}</p>
        <p style='color:{ACCENT}; font-size:1.4rem; font-weight:800;
                  font-family:Syne,sans-serif; margin:0;'>{df.shape[0]:,}</p>
        <p style='color:{SUBTEXT}; font-size:0.72rem; margin:0 0 10px 0;'>{t('total_records')}</p>
        <p style='color:{ACCENT}; font-size:1.4rem; font-weight:800;
                  font-family:Syne,sans-serif; margin:0;'>{df['Company'].nunique()}</p>
        <p style='color:{SUBTEXT}; font-size:0.72rem; margin:0;'>{t('active_clients')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Owner Card
    st.markdown(f"""
    <div style='background:{CARD}; border:1px solid {BORDER};
                border-radius:12px; padding:14px; margin-bottom:12px;'>
        <p style='color:{SUBTEXT}; font-size:0.68rem; text-transform:uppercase;
                  letter-spacing:2px; margin:0 0 6px 0;'>👤 {t('owner')}</p>
        <p style='color:{TEXT}; font-size:0.9rem; font-weight:700;
                  font-family:Syne,sans-serif; margin:0;'>Eng. Issa Mkhaimer</p>
    </div>
    """, unsafe_allow_html=True)

    # Social Links
    st.markdown(f"""
    <div style='background:{CARD}; border:1px solid {BORDER};
                border-radius:12px; padding:14px;'>
        <p style='color:{SUBTEXT}; font-size:0.68rem; text-transform:uppercase;
                  letter-spacing:2px; margin:0 0 10px 0;'>🔗 {t('follow_us')}</p>
        <a href='https://www.instagram.com/3essa.official?igsh=MXF1amV2Mm5uMXE0NQ=='
           target='_blank'
           style='display:flex; align-items:center; gap:8px; text-decoration:none;
                  color:{TEXT}; padding:8px 10px; border-radius:8px;
                  background:rgba(255,255,255,0.03); margin-bottom:6px;
                  border:1px solid rgba(255,255,255,0.06); transition:all 0.2s;'>
            <span style='font-size:1.1rem;'>📸</span>
            <div>
                <p style='margin:0; font-size:0.78rem; font-weight:600;'>Eng. Issa Mkhaimer</p>
                <p style='margin:0; font-size:0.68rem; color:{SUBTEXT};'>@3essa.official</p>
            </div>
        </a>
        <a href='https://www.instagram.com/3m4media?igsh=MThtODI3a2FzMXN0Yw=='
           target='_blank'
           style='display:flex; align-items:center; gap:8px; text-decoration:none;
                  color:{ACCENT}; padding:8px 10px; border-radius:8px;
                  background:rgba(0,180,180,0.06);
                  border:1px solid rgba(0,180,180,0.2); transition:all 0.2s;'>
            <span style='font-size:1.1rem;'>📸</span>
            <div>
                <p style='margin:0; font-size:0.78rem; font-weight:700;'>3M4Media</p>
                <p style='margin:0; font-size:0.68rem; color:{SUBTEXT};'>@3m4media</p>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;'>
        <p style='color:{SUBTEXT}; font-size:0.65rem; margin:0;'>Promote Your Dreams ⭐</p>
        <p style='color:{ACCENT}; font-size:0.75rem; font-weight:700;
                  font-family:Syne,sans-serif; margin:2px 0 0 0;'>www.3m4media.com</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# Active Data
# ==============================
active_df = st.session_state.get('uploaded_df', df)

# ==============================
# Render Page
# ==============================
from modules.overview import show_overview
from modules.client_view import show_client_view
from modules.ai_insights import show_ai_insights
from modules.data_upload import show_data_upload

if current_page == "overview":
    show_overview(active_df, lang)
elif current_page == "client":
    show_client_view(active_df, lang)
elif current_page == "ai":
    show_ai_insights(active_df, lang)
elif current_page == "upload":
    show_data_upload(lang)
