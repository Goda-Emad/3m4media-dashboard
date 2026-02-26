import streamlit as st
import pandas as pd
from modules.translator import get_text

def show_data_upload(lang="en"):
    t = lambda key: get_text(key, lang)

    st.title(f"📁 {t('upload_data')}")
    st.markdown("---")

    st.info("ارفع ملف CSV لعميل جديد وهيظهر في الداشبورد فوراً")

    uploaded_file = st.file_uploader(
        t("upload_csv"),
        type=['csv', 'parquet']
    )

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_parquet(uploaded_file)

            # تحقق من الأعمدة المطلوبة
            required_cols = ['Clicks', 'Impressions', 'ROI', 
                           'Channel_Used', 'Campaign_Goal', 'Company']
            missing = [c for c in required_cols if c not in df.columns]

            if missing:
                st.error(f"❌ أعمدة ناقصة: {missing}")
            else:
                # حساب CTR لو مش موجود
                if 'CTR' not in df.columns:
                    df['CTR'] = (df['Clicks'] / df['Impressions'] * 100).round(2)
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])
                    df['Month'] = df['Date'].dt.month

                st.success(f"✅ الملف اتحمل! {df.shape[0]:,} صف")
                st.dataframe(df.head())

                # حفظ في session
                st.session_state['uploaded_df'] = df
                st.session_state['uploaded_name'] = uploaded_file.name

        except Exception as e:
            st.error(f"❌ Error: {e}")
