import streamlit as st
import plotly.express as px
import pandas as pd
from modules.translator import get_text
from modules.pdf_report import generate_pdf

def show_client_view(df, lang="en"):
    t = lambda key: get_text(key, lang)

    # اختيار العميل
    clients = df['Company'].unique().tolist()
    selected = st.selectbox(t("select_client"), clients)
    client_df = df[df['Company'] == selected]

    st.title(f"📊 {selected}")
    st.markdown("---")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t("total_clicks"), f"{client_df['Clicks'].sum():,}")
    with col2:
        st.metric(t("total_impressions"), f"{client_df['Impressions'].sum():,}")
    with col3:
        st.metric(t("avg_roi"), f"{client_df['ROI'].mean():.2f}x")
    with col4:
        st.metric(t("avg_ctr"), f"{client_df['CTR'].mean():.2f}%")

    st.markdown("---")
    col1, col2 = st.columns(2)

    # Platform Performance
    with col1:
        st.subheader(t("platform_comparison"))
        platform = client_df.groupby('Channel_Used')['ROI'].mean().reset_index()
        fig = px.bar(
            platform, x='Channel_Used', y='ROI',
            color='Channel_Used',
            color_discrete_sequence=['#00D4FF', '#7B2FBE', '#FF6B6B', '#51CF66'],
            template='plotly_dark'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Monthly Trend
    with col2:
        st.subheader(t("monthly_trend"))
        monthly = client_df.groupby('Month')['ROI'].mean().reset_index()
        fig2 = px.line(
            monthly, x='Month', y='ROI',
            markers=True,
            color_discrete_sequence=['#00D4FF'],
            template='plotly_dark'
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # PDF Report Button
    st.markdown("---")
    if st.button(t("generate_report"), type="primary"):
        pdf_bytes = generate_pdf(client_df, selected, lang)
        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_bytes,
            file_name=f"{selected}_report.pdf",
            mime="application/pdf"
        )
