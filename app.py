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
    initial_sidebar_state="collapsed"   # collapsed → زرار الفتح يبان على الموبايل
)

# ==============================
# Session State Defaults
# ==============================
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en'
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'

lang  = st.session_state['lang']
theme = st.session_state['theme']

# ==============================
# Viewport Meta — مهم جداً للموبايل
# ==============================
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    /* منع zoom غير مقصود على iOS */
    input, select, textarea { font-size: 16px !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# Theme Colors
# ==============================
if theme == 'dark':
    BG          = "#060B14"
    CARD        = "rgba(0,180,180,0.06)"
    TEXT        = "#FFFFFF"
    SUBTEXT     = "#8899AA"
    BORDER      = "rgba(0,180,180,0.2)"
    ACCENT      = "#00B4B4"
    SIDEBAR_BG  = "#040810"
    GLASS_MAIN  = "rgba(6,11,20,0.45)"
    GLASS_SIDE  = "rgba(4,8,16,0.55)"
    GLASS_CARD  = "rgba(255,255,255,0.04)"
    GLASS_CHART = "rgba(255,255,255,0.03)"
else:
    BG          = "#EEF2F7"
    CARD        = "rgba(0,100,100,0.06)"
    TEXT        = "#0A1628"
    SUBTEXT     = "#4A6080"
    BORDER      = "rgba(0,120,120,0.25)"
    ACCENT      = "#006B6B"
    SIDEBAR_BG  = "#DDE6F0"
    GLASS_MAIN  = "rgba(240,244,248,0.55)"
    GLASS_SIDE  = "rgba(220,232,245,0.65)"
    GLASS_CARD  = "rgba(255,255,255,0.55)"
    GLASS_CHART = "rgba(255,255,255,0.45)"

# ==============================
# Background Image
# ==============================
bg_css = ""
if 'bg_image' in st.session_state:
    bg_css = f"""
    .stApp {{
        background-image: url("{st.session_state['bg_image']}") !important;
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    """

# ==============================
# Inject CSS
# ==============================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* {{ font-family: 'DM Sans', sans-serif; box-sizing: border-box; }}
h1, h2, h3, h4 {{ font-family: 'Syne', sans-serif !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1.2rem !important; padding-bottom: 2rem !important; }}

/* ── Background ── */
{bg_css}

.stApp {{
    background-color: {BG} !important;
    color: {TEXT} !important;
    transition: all 0.5s ease;
    {"background: linear-gradient(135deg,#060B14 0%,#0A0F1E 60%,#060B14 100%) !important;"
     if theme=="dark" and "bg_image" not in st.session_state else ""}
    {"background: linear-gradient(135deg,#EEF2F7 0%,#DDE6F0 100%) !important;"
     if theme=="light" and "bg_image" not in st.session_state else ""}
}}

/* ── Animated top line ── */
.stApp::before {{
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {ACCENT}, transparent);
    animation: scanline 3s linear infinite;
    z-index: 9999;
    pointer-events: none;
}}
@keyframes scanline {{
    0%   {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(100%); }}
}}

/* ── Glass Main Content ── */
.block-container {{
    background: {GLASS_MAIN} !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border-radius: 20px !important;
    border: 1px solid {BORDER} !important;
    padding: 28px 32px !important;
    transition: all 0.4s ease;
}}

/* ── Glass Sidebar ── */
[data-testid="stSidebar"] {{
    background: {GLASS_SIDE} !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border-right: 1px solid {BORDER} !important;
    transition: transform 0.35s cubic-bezier(0.4,0,0.2,1),
                opacity   0.35s ease,
                box-shadow 0.35s ease !important;
}}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
[data-testid="stSidebar"] a {{ text-decoration: none !important; }}

/* Sidebar مفتوح ← shadow درامي */
[data-testid="stSidebar"][aria-expanded="true"] {{
    box-shadow: 8px 0 48px rgba(0,0,0,0.5) !important;
}}

/* ── KPI Cards ── */
[data-testid="metric-container"] {{
    background: {GLASS_CARD} !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid {BORDER} !important;
    border-radius: 16px !important;
    padding: 22px !important;
    position: relative;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    box-shadow: 0 4px 24px rgba(0,180,180,0.06);
}}
[data-testid="metric-container"]::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, {ACCENT}, transparent);
    border-radius: 16px 0 0 16px;
}}
[data-testid="metric-container"]:hover {{
    transform: translateY(-4px) !important;
    border-color: {ACCENT} !important;
    box-shadow: 0 12px 40px rgba(0,180,180,0.18) !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Syne', sans-serif !important;
    color: {ACCENT} !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}}
[data-testid="stMetricLabel"] {{
    color: {SUBTEXT} !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.8px !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, {ACCENT} 0%, #007A7A 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 16px rgba(0,180,180,0.25) !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0,180,180,0.45) !important;
}}

/* ── Charts ── */
.js-plotly-plot {{
    background: {GLASS_CHART} !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid {BORDER} !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}}
.js-plotly-plot:hover {{
    border-color: {ACCENT} !important;
    box-shadow: 0 8px 32px rgba(0,180,180,0.12) !important;
}}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {{
    background: {GLASS_CARD} !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
}}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {{
    background: {GLASS_CARD} !important;
    backdrop-filter: blur(10px) !important;
    border: 2px dashed {BORDER} !important;
    border-radius: 16px !important;
    padding: 20px !important;
    transition: all 0.3s ease;
}}
[data-testid="stFileUploader"]:hover {{
    border-color: {ACCENT} !important;
    background: rgba(0,180,180,0.08) !important;
}}

/* ── Status ── */
.stSuccess {{
    background: rgba(0,180,180,0.08) !important;
    border: 1px solid rgba(0,180,180,0.35) !important;
    border-radius: 10px !important;
}}
.stInfo {{
    background: rgba(0,100,255,0.06) !important;
    border: 1px solid rgba(0,100,255,0.25) !important;
    border-radius: 10px !important;
}}

/* ── Divider ── */
hr {{ border-color: {BORDER} !important; opacity: 0.6 !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {ACCENT}; border-radius: 4px; }}

/* ── Logo ── */
[data-testid="stSidebar"] img {{
    border-radius: 14px !important;
    border: 2px solid {BORDER} !important;
    padding: 3px !important;
    transition: all 0.3s;
}}
[data-testid="stSidebar"] img:hover {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 20px rgba(0,180,180,0.3) !important;
}}

/* ════════════════════════════════════════
   📱 MOBILE & TABLET RESPONSIVE
   ════════════════════════════════════════ */

/* ── زرار فتح الـ Sidebar — كل الأشكال الممكنة في Streamlit ── */
[data-testid="collapsedControl"],
button[kind="headerNoPadding"],
.st-emotion-cache-1egp75f,
section[data-testid="stSidebar"] + div button,
[aria-label="open sidebar"],
[aria-label="Close sidebar"],
[data-testid="stSidebarCollapsedControl"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 48px !important;
    height: 48px !important;
    min-width: 48px !important;
    background: linear-gradient(135deg, {ACCENT} 0%, #007A7A 100%) !important;
    border-radius: 14px !important;
    border: none !important;
    box-shadow: 0 4px 24px rgba(0,180,180,0.45) !important;
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 999999 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    visibility: visible !important;
    opacity: 1 !important;
}}
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapsedControl"] svg {{
    fill: white !important;
    color: white !important;
    width: 22px !important;
    height: 22px !important;
}}

/* ── Sidebar open state ── */
[data-testid="stSidebar"][aria-expanded="true"] {{
    box-shadow: 8px 0 48px rgba(0,0,0,0.5) !important;
}}

/* ── MOBILE: max 768px ── */
@media screen and (max-width: 768px) {{

    /* نص KPI أصغر عشان ما يتقطعش */
    [data-testid="stMetricValue"] {{
        font-size: 1.1rem !important;
        word-break: break-all !important;
        overflow-wrap: anywhere !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 0.60rem !important;
        letter-spacing: 1px !important;
    }}
    [data-testid="metric-container"] {{
        padding: 12px 10px !important;
        min-width: 0 !important;
    }}

    /* Main content */
    .block-container {{
        padding: 16px 10px !important;
        border-radius: 14px !important;
        margin: 0 4px !important;
        overflow-x: hidden !important;
    }}

    /* منع overflow أفقي */
    .stApp {{
        overflow-x: hidden !important;
    }}

    /* Sidebar overlay */
    [data-testid="stSidebar"] {{
        position: fixed !important;
        top: 0 !important; left: 0 !important;
        height: 100dvh !important;
        width: 275px !important;
        max-width: 85vw !important;
        z-index: 99998 !important;
        overflow-y: auto !important;
    }}

    /* Charts */
    .js-plotly-plot {{ border-radius: 12px !important; }}

    /* Typography */
    h1 {{ font-size: 1.3rem !important; }}
    h2 {{ font-size: 1.1rem !important; }}
    h3 {{ font-size: 0.95rem !important; }}

    /* Buttons */
    .stButton > button {{
        width: 100% !important;
        min-height: 48px !important;
        font-size: 0.76rem !important;
    }}

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {{
        min-height: 48px !important;
        font-size: 0.85rem !important;
    }}

    /* Columns: stack على موبايل */
    [data-testid="stHorizontalBlock"] {{
        flex-wrap: wrap !important;
    }}
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
        min-width: calc(50% - 8px) !important;
        flex: 1 1 calc(50% - 8px) !important;
    }}
}}

/* ── TABLET: 769px → 1024px ── */
@media screen and (min-width: 769px) and (max-width: 1024px) {{

    .block-container {{
        padding: 20px 20px !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 1.5rem !important;
    }}

    [data-testid="stSidebar"] {{
        min-width: 235px !important;
        max-width: 245px !important;
    }}

    h1 {{ font-size: 1.6rem !important; }}
}}

/* ── LARGE: > 1400px ── */
@media screen and (min-width: 1400px) {{
    .block-container {{
        padding: 32px 40px !important;
    }}
}}

/* ── Touch devices ── */
@media (hover: none) and (pointer: coarse) {{
    [data-testid="metric-container"]:hover {{
        transform: none !important;
        box-shadow: 0 4px 24px rgba(0,180,180,0.06) !important;
    }}
    .stButton > button:hover {{
        transform: none !important;
    }}
    /* Touch targets */
    .stButton > button,
    [data-testid="stSelectbox"] > div > div {{
        min-height: 48px !important;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ==============================
# Translations
# ==============================
TRANSLATIONS = {
    "en": {
        "dashboard_title": "3M4Media Intelligence",
        "overview":        "Overview",
        "client_view":     "Client View",
        "ai_insights":     "AI Insights",
        "upload_data":     "Upload Data",
        "total_clicks":    "Total Clicks",
        "total_impressions":"Total Impressions",
        "avg_roi":         "Average ROI",
        "avg_ctr":         "Average CTR",
        "avg_conversion":  "Conversion Rate",
        "avg_cost":        "Avg Acquisition Cost",
        "best_platform":   "Best Platform",
        "best_campaign":   "Best Campaign Goal",
        "campaign_performance": "Campaign Performance",
        "platform_comparison":  "Platform Comparison",
        "monthly_trend":   "Monthly ROI Trend",
        "ai_recommendation":"AI Recommendations",
        "prediction":      "Next Month Prediction",
        "generate_report": "📄 Generate PDF Report",
        "select_client":   "Select Client",
        "upload_csv":      "Upload CSV or Parquet File",
        "dark_mode":       "🌙 Dark",
        "light_mode":      "☀️ Light",
        "theme":           "Theme",
        "language":        "Language",
        "live_stats":      "Live Stats",
        "total_records":   "Total Records",
        "active_clients":  "Active Clients",
        "owner":           "Founder & CEO",
        "follow_us":       "Follow Us",
        "bg_image":        "Background Image",
        "reset_bg":        "🗑️ Reset Background",
        "bg_updated":      "✅ Background updated!",
    },
    "ar": {
        "dashboard_title": "منصة 3M4Media الذكية",
        "overview":        "نظرة عامة",
        "client_view":     "عرض العميل",
        "ai_insights":     "توصيات الذكاء الاصطناعي",
        "upload_data":     "رفع بيانات",
        "total_clicks":    "إجمالي النقرات",
        "total_impressions":"إجمالي المشاهدات",
        "avg_roi":         "متوسط العائد",
        "avg_ctr":         "متوسط النقر",
        "avg_conversion":  "معدل التحويل",
        "avg_cost":        "متوسط تكلفة الاكتساب",
        "best_platform":   "أفضل منصة",
        "best_campaign":   "أفضل هدف حملة",
        "campaign_performance": "أداء الحملات",
        "platform_comparison":  "مقارنة المنصات",
        "monthly_trend":   "الاتجاه الشهري للعائد",
        "ai_recommendation":"توصيات الذكاء الاصطناعي",
        "prediction":      "توقعات الشهر الجاي",
        "generate_report": "📄 توليد تقرير PDF",
        "select_client":   "اختر العميل",
        "upload_csv":      "ارفع ملف CSV أو Parquet",
        "dark_mode":       "🌙 داكن",
        "light_mode":      "☀️ فاتح",
        "theme":           "المظهر",
        "language":        "اللغة",
        "live_stats":      "إحصائيات مباشرة",
        "total_records":   "إجمالي السجلات",
        "active_clients":  "العملاء النشطين",
        "owner":           "المؤسس والرئيس التنفيذي",
        "follow_us":       "تابعنا",
        "bg_image":        "صورة الخلفية",
        "reset_bg":        "🗑️ إزالة الخلفية",
        "bg_updated":      "✅ تم تحديث الخلفية!",
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

    # ── Logo ──
    if os.path.exists('assets/logo.png'):
        st.image('assets/logo.png', width=155)
    else:
        st.markdown(f"""
        <div style='text-align:center; padding:16px 0;'>
            <span style='font-family:Syne,sans-serif; font-size:2.2rem;
                         font-weight:800; color:{ACCENT};'>3M</span>
            <span style='font-family:Syne,sans-serif; font-size:0.9rem; color:{SUBTEXT};
                         display:block; letter-spacing:5px; margin-top:-4px;'>MEDIA</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Language ──
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.70rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>🌐 {t('language')}</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🇬🇧 EN", use_container_width=True, key="btn_en"):
            st.session_state['lang'] = 'en'
            st.rerun()
    with c2:
        if st.button("🇪🇬 AR", use_container_width=True, key="btn_ar"):
            st.session_state['lang'] = 'ar'
            st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Theme ──
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.70rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>🎨 {t('theme')}</p>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button(t("dark_mode"), use_container_width=True, key="btn_dark"):
            st.session_state['theme'] = 'dark'
            st.rerun()
    with c4:
        if st.button(t("light_mode"), use_container_width=True, key="btn_light"):
            st.session_state['theme'] = 'light'
            st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Background Upload ──
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.70rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>&#128247; {t('bg_image')}</p>", unsafe_allow_html=True)

    bg_file = st.file_uploader(
        "", type=['png','jpg','jpeg','webp'],
        label_visibility="collapsed",
        key="bg_uploader"
    )
    if bg_file is not None:
        bg_bytes = bg_file.read()
        bg_b64   = base64.b64encode(bg_bytes).decode()
        ext      = bg_file.name.split('.')[-1].lower()
        st.session_state['bg_image'] = f"data:image/{ext};base64,{bg_b64}"
        st.success(t("bg_updated"))
        st.rerun()

    if 'bg_image' in st.session_state:
        if st.button(t("reset_bg"), use_container_width=True, key="btn_reset"):
            st.session_state.pop('bg_image', None)
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Navigation ──
    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.70rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 8px 0;'>&#128204; Navigation</p>", unsafe_allow_html=True)

    pages = {
        f"&#128202;  {t('overview')}":    "overview",
        f"&#128100;  {t('client_view')}": "client",
        f"&#129302;  {t('ai_insights')}": "ai",
        f"&#128193;  {t('upload_data')}": "upload",
    }
    page         = st.radio("", list(pages.keys()), label_visibility="collapsed")
    current_page = pages[page]

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Live Stats ──
    st.markdown(f"""
    <div style='background:{GLASS_CARD}; backdrop-filter:blur(12px);
                border:1px solid {BORDER}; border-radius:14px;
                padding:16px; margin-bottom:12px;'>
        <p style='color:{SUBTEXT}; font-size:0.68rem; text-transform:uppercase;
                  letter-spacing:2px; margin:0 0 10px 0;'>
            &#128225; {t('live_stats')}
        </p>
        <p style='color:{ACCENT}; font-size:1.5rem; font-weight:800;
                  font-family:Syne,sans-serif; margin:0; line-height:1;'>
            {df.shape[0]:,}
        </p>
        <p style='color:{SUBTEXT}; font-size:0.70rem; margin:2px 0 12px 0;'>
            {t('total_records')}
        </p>
        <p style='color:{ACCENT}; font-size:1.5rem; font-weight:800;
                  font-family:Syne,sans-serif; margin:0; line-height:1;'>
            {df['Company'].nunique()}
        </p>
        <p style='color:{SUBTEXT}; font-size:0.70rem; margin:2px 0 0 0;'>
            {t('active_clients')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Owner Card ──
    st.markdown(f"""
    <div style='background:{GLASS_CARD}; backdrop-filter:blur(12px);
                border:1px solid {BORDER}; border-radius:14px;
                padding:14px; margin-bottom:12px;'>
        <p style='color:{SUBTEXT}; font-size:0.66rem; text-transform:uppercase;
                  letter-spacing:2px; margin:0 0 6px 0;'>
            &#128100; {t('owner')}
        </p>
        <p style='color:{TEXT}; font-size:0.92rem; font-weight:700;
                  font-family:Syne,sans-serif; margin:0;'>
            Eng. Issa Mkhaimer
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Social Links ──
    st.markdown(f"""
    <div style='background:{GLASS_CARD}; backdrop-filter:blur(12px);
                border:1px solid {BORDER}; border-radius:14px; padding:14px;'>
        <p style='color:{SUBTEXT}; font-size:0.66rem; text-transform:uppercase;
                  letter-spacing:2px; margin:0 0 10px 0;'>
            &#128279; {t('follow_us')}
        </p>
        <a href='https://www.instagram.com/3essa.official'
           target='_blank'
           style='display:flex; align-items:center; gap:10px;
                  text-decoration:none; padding:8px 10px;
                  border-radius:10px; margin-bottom:8px;
                  background:rgba(255,255,255,0.04);
                  border:1px solid rgba(255,255,255,0.08);'>
            <span style='font-size:1.2rem;'>&#128247;</span>
            <div>
                <p style='margin:0; font-size:0.80rem; font-weight:700; color:{TEXT};'>Eng. Issa Mkhaimer</p>
                <p style='margin:0; font-size:0.68rem; color:{SUBTEXT};'>@3essa.official</p>
            </div>
        </a>
        <a href='https://www.instagram.com/3m4media'
           target='_blank'
           style='display:flex; align-items:center; gap:10px;
                  text-decoration:none; padding:8px 10px;
                  border-radius:10px;
                  background:rgba(0,180,180,0.07);
                  border:1px solid rgba(0,180,180,0.22);'>
            <span style='font-size:1.2rem;'>&#128247;</span>
            <div>
                <p style='margin:0; font-size:0.80rem; font-weight:700; color:{ACCENT};'>3M4Media</p>
                <p style='margin:0; font-size:0.68rem; color:{SUBTEXT};'>@3m4media</p>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center; padding:8px 0;'>
        <p style='color:{SUBTEXT}; font-size:0.62rem; margin:0; letter-spacing:1px;'>
            PROMOTE YOUR DREAMS &#11088;
        </p>
        <p style='color:{ACCENT}; font-size:0.72rem; font-weight:700;
                  font-family:Syne,sans-serif; margin:3px 0 0 0;'>
            www.3m4media.com
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# Active Data
# ==============================
active_df = st.session_state.get('uploaded_df', df)

# ==============================
# Render Page
# ==============================
from modules.overview    import show_overview
from modules.client_view import show_client_view
from modules.ai_insights import show_ai_insights
from modules.data_upload import show_data_upload

if current_page == "overview":
    show_overview(active_df, lang, theme)
elif current_page == "client":
    show_client_view(active_df, lang, theme)
elif current_page == "ai":
    show_ai_insights(active_df, lang, theme)
elif current_page == "upload":
    show_data_upload(lang)
