import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from modules.translator import get_text

def show_overview(df, lang="en"):
    t = lambda key: get_text(key, lang)

    st.title(t("dashboard_title"))
    st.markdown("---")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t("total_clicks"), f"{df['Clicks'].sum():,}")
    with col2:
        st.metric(t("total_impressions"), f"{df['Impressions'].sum():,}")
    with col3:
        st.metric(t("avg_roi"), f"{df['ROI'].mean():.2f}x")
    with col4:
        st.metric(t("avg_ctr"), f"{df['CTR'].mean():.2f}%")

    st.markdown("---")
    col1, col2 = st.columns(2)

    # Platform Comparison
    with col1:
        st.subheader(t("platform_comparison"))
        platform_data = df.groupby('Channel_Used').agg({
            'Clicks': 'sum',
            'ROI': 'mean',
            'Conversion_Rate': 'mean'
        }).reset_index()

        fig = px.bar(
            platform_data, x='Channel_Used', y='ROI',
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

    # Campaign Goal Performance
    with col2:
        st.subheader(t("campaign_performance"))
        goal_data = df.groupby('Campaign_Goal')['ROI'].mean().reset_index()

        fig2 = px.pie(
            goal_data, values='ROI', names='Campaign_Goal',
            color_discrete_sequence=['#00D4FF', '#7B2FBE', '#FF6B6B', '#51CF66'],
            template='plotly_dark'
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Monthly Trend
    st.subheader(t("monthly_trend"))
    monthly = df.groupby('Month').agg({
        'Clicks': 'sum',
        'ROI': 'mean',
        'Conversion_Rate': 'mean'
    }).reset_index()

    fig3 = px.line(
        monthly, x='Month', y='ROI',
        markers=True,
        color_discrete_sequence=['#00D4FF'],
        template='plotly_dark'
    )
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig3, use_container_width=True)
