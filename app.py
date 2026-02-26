import streamlit as st
import pandas as pd
import os
import base64

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="3M4Media | Smart Marketing Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Session State
# ==============================
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en'
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'
if 'sidebar_open' not in st.session_state:
    st.session_state['sidebar_open'] = True

lang  = st.session_state['lang']
theme = st.session_state['theme']

# ==============================
# Theme Colors
# ==============================
if theme == 'dark':
    BG, TEXT, SUBTEXT = "#060B14", "#FFFFFF", "#8899AA"
    BORDER, ACCENT    = "rgba(0,180,180,0.2)", "#00B4B4"
    GLASS_MAIN        = "rgba(6,11,20,0.45)"
    GLASS_SIDE        = "rgba(4,8,16,0.55)"
    GLASS_CARD        = "rgba(255,255,255,0.04)"
    GLASS_CHART       = "rgba(255,255,255,0.03)"
else:
    BG, TEXT, SUBTEXT = "#EEF2F7", "#0A1628", "#4A6080"
    BORDER, ACCENT    = "rgba(0,120,120,0.25)", "#006B6B"
    GLASS_MAIN        = "rgba(240,244,248,0.55)"
    GLASS_SIDE        = "rgba(220,232,245,0.65)"
    GLASS_CARD        = "rgba(255,255,255,0.55)"
    GLASS_CHART       = "rgba(255,255,255,0.45)"

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
# CSS
# ==============================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* {{ font-family: 'DM Sans', sans-serif; box-sizing: border-box; }}
h1, h2, h3, h4 {{ font-family: 'Syne', sans-serif !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 0.5rem !important; padding-bottom: 2rem !important; }}

/* ── زرار Toggle الـ Sidebar ── */
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:first-child .stButton > button,
button[key="sidebar_toggle"] {{
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 999999 !important;
    width: 44px !important;
    height: 44px !important;
    min-width: 44px !important;
    padding: 0 !important;
    font-size: 1.2rem !important;
    background: linear-gradient(135deg, #00B4B4, #007A7A) !important;
    border: none !important;
    border-radius: 13px !important;
    box-shadow: 0 4px 20px rgba(0,180,180,0.45) !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:first-child .stButton > button:hover {{
    transform: scale(1.1) !important;
    box-shadow: 0 8px 28px rgba(0,180,180,0.6) !important;
}}

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

.stApp::before {{
    content: '';
    position: fixed; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, {ACCENT}, transparent);
    animation: scanline 3s linear infinite;
    z-index: 9999; pointer-events: none;
}}
@keyframes scanline {{
    0%   {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(100%); }}
}}

.block-container {{
    background: {GLASS_MAIN} !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border-radius: 20px !important;
    border: 1px solid {BORDER} !important;
    padding: 28px 32px !important;
    transition: all 0.4s ease;
}}

[data-testid="stSidebar"] {{
    background: {GLASS_SIDE} !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border-right: 1px solid {BORDER} !important;
    transition: all 0.4s ease;
}}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
[data-testid="stSidebar"] a  {{ text-decoration: none !important; }}

/* ═══════════════════════════════════════════════
   ✅ FIX النهائي: زرار السهم يظهر ويشتغل دايماً
   ═══════════════════════════════════════════════

   المشكلة كانت:
   - الـ CSS بتاع الـ sidebar كان بيغطي على زرار السهم
   - [data-testid="stSidebar"] * بيشمل الزرار ويخبيه

   الحل:
   - نخصص الزرار بـ CSS واضح يظهره
   ═══════════════════════════════════════════════ */

/* زرار الفتح (لما الـ sidebar مقفول) */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {{
    display:         flex !important;
    visibility:      visible !important;
    opacity:         1 !important;
    pointer-events:  auto !important;
    align-items:     center !important;
    justify-content: center !important;
    background: linear-gradient(135deg, {ACCENT}, #007A7A) !important;
    border:          none !important;
    border-radius:   12px !important;
    box-shadow:      0 4px 20px rgba(0,180,180,0.4) !important;
    transition:      all 0.3s ease !important;
    cursor:          pointer !important;
}}
[data-testid="stSidebarCollapsedControl"]:hover,
[data-testid="collapsedControl"]:hover {{
    transform:  scale(1.08) !important;
    box-shadow: 0 8px 30px rgba(0,180,180,0.6) !important;
}}
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="collapsedControl"] svg {{
    fill:   white !important;
    color:  white !important;
    width:  18px !important;
    height: 18px !important;
}}

/* زرار الإغلاق (جوا الـ sidebar — السهم «) */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebar"] > div > div > div > button {{
    display:         flex !important;
    visibility:      visible !important;
    opacity:         1 !important;
    pointer-events:  auto !important;
    align-items:     center !important;
    justify-content: center !important;
    background: linear-gradient(135deg, {ACCENT}, #007A7A) !important;
    border:          none !important;
    border-radius:   10px !important;
    width:           36px !important;
    height:          36px !important;
    cursor:          pointer !important;
    box-shadow:      0 2px 12px rgba(0,180,180,0.4) !important;
    transition:      all 0.3s ease !important;
}}
[data-testid="stSidebarCollapseButton"]:hover,
[data-testid="stSidebar"] > div > div > div > button:hover {{
    transform:  scale(1.1) !important;
    box-shadow: 0 4px 20px rgba(0,180,180,0.6) !important;
}}
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebar"] > div > div > div > button svg {{
    fill:   white !important;
    color:  white !important;
    width:  16px !important;
    height: 16px !important;
}}

/* ── KPI Cards ── */
[data-testid="metric-container"] {{
    background: {GLASS_CARD} !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid {BORDER} !important;
    border-radius: 16px !important;
    padding: 22px !important;
    position: relative; overflow: hidden;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    box-shadow: 0 4px 24px rgba(0,180,180,0.06);
}}
[data-testid="metric-container"]::before {{
    content: '';
    position: absolute; top:0; left:0;
    width:3px; height:100%;
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

hr {{ border-color: {BORDER} !important; opacity: 0.6 !important; }}

::-webkit-scrollbar {{ width:4px; height:4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {ACCENT}; border-radius:4px; }}

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

/* ── Mobile ── */
@media screen and (max-width: 768px) {{
    .block-container {{
        padding: 14px 10px !important;
        border-radius: 14px !important;
        margin: 0 4px !important;
    }}
    [data-testid="stMetricValue"] {{ font-size: 1.2rem !important; }}
    [data-testid="metric-container"] {{ padding: 12px 10px !important; }}
    h1 {{ font-size: 1.3rem !important; }}
    .stButton > button {{
        min-height: 48px !important;
        width: 100% !important;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ==============================
# Translations
# ==============================
TRANSLATIONS = {
    "en": {
        "dashboard_title":      "3M4Media Intelligence",
        "overview":             "Overview",
        "client_view":          "Client View",
        "ai_insights":          "AI Insights",
        "upload_data":          "Upload Data",
        "total_clicks":         "Total Clicks",
        "total_impressions":    "Total Impressions",
        "avg_roi":              "Average ROI",
        "avg_ctr":              "Average CTR",
        "avg_conversion":       "Conversion Rate",
        "avg_cost":             "Avg Acquisition Cost",
        "best_platform":        "Best Platform",
        "best_campaign":        "Best Campaign Goal",
        "campaign_performance": "Campaign Performance",
        "platform_comparison":  "Platform Comparison",
        "monthly_trend":        "Monthly ROI Trend",
        "ai_recommendation":    "AI Recommendations",
        "prediction":           "Next Month Prediction",
        "generate_report":      "📄 Generate PDF Report",
        "select_client":        "Select Client",
        "upload_csv":           "Upload CSV or Parquet File",
        "dark_mode":            "🌙 Dark",
        "light_mode":           "☀️ Light",
        "theme":                "Theme",
        "language":             "Language",
        "live_stats":           "Live Stats",
        "total_records":        "Total Records",
        "active_clients":       "Active Clients",
        "owner":                "Founder & CEO",
        "follow_us":            "Follow Us",
        "bg_image":             "Background Image",
        "reset_bg":             "🗑️ Reset Background",
        "bg_updated":           "✅ Background updated!",
    },
    "ar": {
        "dashboard_title":      "منصة 3M4Media الذكية",
        "overview":             "نظرة عامة",
        "client_view":          "عرض العميل",
        "ai_insights":          "توصيات الذكاء الاصطناعي",
        "upload_data":          "رفع بيانات",
        "total_clicks":         "إجمالي النقرات",
        "total_impressions":    "إجمالي المشاهدات",
        "avg_roi":              "متوسط العائد",
        "avg_ctr":              "متوسط النقر",
        "avg_conversion":       "معدل التحويل",
        "avg_cost":             "متوسط تكلفة الاكتساب",
        "best_platform":        "أفضل منصة",
        "best_campaign":        "أفضل هدف حملة",
        "campaign_performance": "أداء الحملات",
        "platform_comparison":  "مقارنة المنصات",
        "monthly_trend":        "الاتجاه الشهري للعائد",
        "ai_recommendation":    "توصيات الذكاء الاصطناعي",
        "prediction":           "توقعات الشهر الجاي",
        "generate_report":      "📄 توليد تقرير PDF",
        "select_client":        "اختر العميل",
        "upload_csv":           "ارفع ملف CSV أو Parquet",
        "dark_mode":            "🌙 داكن",
        "light_mode":           "☀️ فاتح",
        "theme":                "المظهر",
        "language":             "اللغة",
        "live_stats":           "إحصائيات مباشرة",
        "total_records":        "إجمالي السجلات",
        "active_clients":       "العملاء النشطين",
        "owner":                "المؤسس والرئيس التنفيذي",
        "follow_us":            "تابعنا",
        "bg_image":             "صورة الخلفية",
        "reset_bg":             "🗑️ إزالة الخلفية",
        "bg_updated":           "✅ تم تحديث الخلفية!",
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
# Sidebar Toggle — Python Button
# الحل الوحيد المضمون على Streamlit Cloud
# ==============================

# زرار الفتح/الغلق في أعلى يسار الصفحة
col_toggle, col_space = st.columns([0.04, 0.96])
with col_toggle:
    toggle_icon = "✕" if st.session_state['sidebar_open'] else "☰"
    if st.button(toggle_icon, key="sidebar_toggle"):
        st.session_state['sidebar_open'] = not st.session_state['sidebar_open']
        st.rerun()

# حالة الـ sidebar بناءً على session_state
sidebar_state = "expanded" if st.session_state['sidebar_open'] else "collapsed"

# ==============================
# Sidebar
# ==============================
with st.sidebar:

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

    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.70rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>🌐 {t('language')}</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🇬🇧 EN", use_container_width=True, key="btn_en"):
            st.session_state['lang'] = 'en'; st.rerun()
    with c2:
        if st.button("🇪🇬 AR", use_container_width=True, key="btn_ar"):
            st.session_state['lang'] = 'ar'; st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.70rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>🎨 {t('theme')}</p>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        if st.button(t("dark_mode"), use_container_width=True, key="btn_dark"):
            st.session_state['theme'] = 'dark'; st.rerun()
    with c4:
        if st.button(t("light_mode"), use_container_width=True, key="btn_light"):
            st.session_state['theme'] = 'light'; st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown(f"<p style='color:{SUBTEXT}; font-size:0.70rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>&#128247; {t('bg_image')}</p>", unsafe_allow_html=True)
    bg_file = st.file_uploader("", type=['png','jpg','jpeg','webp'],
                                label_visibility="collapsed", key="bg_uploader")
    if bg_file is not None:
        bg_bytes = bg_file.read()
        bg_b64   = base64.b64encode(bg_bytes).decode()
        ext      = bg_file.name.split('.')[-1].lower()
        st.session_state['bg_image'] = f"data:image/{ext};base64,{bg_b64}"
        st.success(t("bg_updated"))
        st.rerun()
    if 'bg_image' in st.session_state:
        if st.button(t("reset_bg"), use_container_width=True, key="btn_reset"):
            st.session_state.pop('bg_image', None); st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

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

    st.markdown(f"""
    <div style='background:{GLASS_CARD}; border:1px solid {BORDER}; border-radius:14px; padding:16px; margin-bottom:12px;'>
        <p style='color:{SUBTEXT}; font-size:0.68rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 10px 0;'>&#128225; {t('live_stats')}</p>
        <p style='color:{ACCENT}; font-size:1.5rem; font-weight:800; font-family:Syne,sans-serif; margin:0; line-height:1;'>{df.shape[0]:,}</p>
        <p style='color:{SUBTEXT}; font-size:0.70rem; margin:2px 0 12px 0;'>{t('total_records')}</p>
        <p style='color:{ACCENT}; font-size:1.5rem; font-weight:800; font-family:Syne,sans-serif; margin:0; line-height:1;'>{df['Company'].nunique()}</p>
        <p style='color:{SUBTEXT}; font-size:0.70rem; margin:2px 0 0 0;'>{t('active_clients')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:{GLASS_CARD}; border:1px solid {BORDER}; border-radius:14px; padding:14px; margin-bottom:12px;'>
        <p style='color:{SUBTEXT}; font-size:0.66rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 6px 0;'>&#128100; {t('owner')}</p>
        <p style='color:{TEXT}; font-size:0.92rem; font-weight:700; font-family:Syne,sans-serif; margin:0;'>Eng. Issa Mkhaimer</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:{GLASS_CARD}; border:1px solid {BORDER}; border-radius:14px; padding:14px;'>
        <p style='color:{SUBTEXT}; font-size:0.66rem; text-transform:uppercase; letter-spacing:2px; margin:0 0 10px 0;'>&#128279; {t('follow_us')}</p>
        <a href='https://www.instagram.com/3essa.official' target='_blank'
           style='display:flex; align-items:center; gap:10px; text-decoration:none; padding:8px 10px;
                  border-radius:10px; margin-bottom:8px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);'>
            <span style='font-size:1.2rem;'>&#128247;</span>
            <div>
                <p style='margin:0; font-size:0.80rem; font-weight:700; color:{TEXT};'>Eng. Issa Mkhaimer</p>
                <p style='margin:0; font-size:0.68rem; color:{SUBTEXT};'>@3essa.official</p>
            </div>
        </a>
        <a href='https://www.instagram.com/3m4media' target='_blank'
           style='display:flex; align-items:center; gap:10px; text-decoration:none; padding:8px 10px;
                  border-radius:10px; background:rgba(0,180,180,0.07); border:1px solid rgba(0,180,180,0.22);'>
            <span style='font-size:1.2rem;'>&#128247;</span>
            <div>
                <p style='margin:0; font-size:0.80rem; font-weight:700; color:{ACCENT};'>3M4Media</p>
                <p style='margin:0; font-size:0.68rem; color:{SUBTEXT};'>@3m4media</p>
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align:center; padding:12px 0;'>
        <p style='color:{SUBTEXT}; font-size:0.62rem; margin:0; letter-spacing:1px;'>PROMOTE YOUR DREAMS &#11088;</p>
        <p style='color:{ACCENT}; font-size:0.72rem; font-weight:700; font-family:Syne,sans-serif; margin:3px 0 0 0;'>www.3m4media.com</p>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# Active Data & Render
# ==============================
active_df = st.session_state.get('uploaded_df', df)

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
