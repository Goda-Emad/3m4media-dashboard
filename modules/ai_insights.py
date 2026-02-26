import streamlit as st
import plotly.express as px
import pandas as pd
import pickle
import numpy as np
from modules.translator import get_text

def show_ai_insights(df, lang="en"):
    t = lambda key: get_text(key, lang)

    st.title(f"🤖 {t('ai_insights')}")
    st.markdown("---")

    # تحميل الموديل
    try:
        with open('models/campaign_model.pkl', 'rb') as f:
            import joblib
            model = joblib.load('models/campaign_model.pkl')
        with open('models/features.pkl', 'rb') as f:
            features = pickle.load(f)
        with open('models/encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)
        model_loaded = True
    except:
        model_loaded = False

    # توصيات AI
    st.subheader(t("ai_recommendation"))

    best_platform = df.groupby('Channel_Used')['ROI'].mean().idxmax()
    best_goal = df.groupby('Campaign_Goal')['ROI'].mean().idxmax()
    best_month = df.groupby('Month')['ROI'].mean().idxmax()
    best_segment = df.groupby('Customer_Segment')['Conversion_Rate'].mean().idxmax()

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ {t('best_platform')}: **{best_platform}**")
        st.info(f"🎯 {t('best_campaign')}: **{best_goal}**")
    with col2:
        st.warning(f"📅 أفضل شهر للنشر: **{best_month}**")
        st.success(f"👥 أفضل شريحة عملاء: **{best_segment}**")

    st.markdown("---")

    # توقعات الشهر الجاي
    st.subheader(f"🔮 {t('prediction')}")
    monthly = df.groupby('Month')['ROI'].mean().reset_index()

    fig = px.line(
        monthly, x='Month', y='ROI',
        markers=True,
        title="ROI Trend & Next Month Prediction",
        color_discrete_sequence=['#00D4FF'],
        template='plotly_dark'
    )

    # إضافة توقع الشهر الجاي
    next_month = monthly['Month'].max() + 1
    next_roi = monthly['ROI'].mean() * 1.05  # توقع 5% زيادة

    fig.add_scatter(
        x=[next_month], y=[next_roi],
        mode='markers',
        marker=dict(size=15, color='#FF6B6B', symbol='star'),
        name='Next Month Prediction'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Feature Importance
    if model_loaded:
        st.subheader("🔑 أهم العوامل في نجاح الحملة")
        importance_df = pd.DataFrame({
            'Feature': features,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=True).tail(8)

        fig2 = px.bar(
            importance_df, x='Importance', y='Feature',
            orientation='h',
            color_discrete_sequence=['#7B2FBE'],
            template='plotly_dark'
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig2, use_container_width=True)
