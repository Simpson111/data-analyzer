
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

# --- Page Config ---
# --- Page Config ---
st.set_page_config(
    page_title="Bitget Wallet Analytics",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Premium Design System (Bitget Card Style) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* Global Reset & Background */
    .stApp {
        background-color: #050505; /* Deep Black */
        background-image: radial-gradient(circle at 50% 10%, #1a1f2e 0%, #050505 50%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Typography */
    h1, h2, h3, h4, .stMarkdown {
        color: #ffffff !important;
    }
    
    h1 {
        font-weight: 800 !important;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(79, 172, 254, 0.3);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #1f1f1f;
    }
    
    /* Cards (Glassmorphism) */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.2);
    }
    
    .metric-card:hover {
        border-color: #4facfe;
        box-shadow: 0 0 30px rgba(79, 172, 254, 0.15);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    /* Inputs */
    .stTextArea textarea, .stTextInput input {
        background-color: #0f1115 !important;
        border: 1px solid #2d3748 !important;
        color: white !important;
        border-radius: 8px;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #4facfe !important;
        box-shadow: 0 0 0 1px #4facfe !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        transition: opacity 0.3s;
    }
    .stButton > button:hover {
        opacity: 0.9;
        box-shadow: 0 0 20px rgba(0, 198, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- Colors for Charts ---
# Cyan -> Blue -> Purple palette to match the card
COLOR_PALETTE = ['#00f2fe', '#4facfe', '#a18cd1', '#fbc2eb', '#43e97b', '#38f9d7']

# --- Helper Function: Generate HTML Report ---
def create_html_report(df_filtered, summary_text, figs):
    """Generates a standalone HTML file with the dashboard content."""
    
    # Calculate metrics for the report
    avg_exp = df_filtered['卡片曝光uv'].mean()
    avg_visit = df_filtered['頁面訪問uv'].mean()
    avg_article_rate = df_filtered['文章訪問率'].mean()
    avg_conv_rate = df_filtered['功能轉化率'].mean()
    
    # Convert plots to HTML divs
    fig_htmls = [fig.to_html(full_html=False, include_plotlyjs='cdn') for fig in figs]
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bitget Wallet Analysis Report</title>
        <meta charset="utf-8">
        <style>
            body {{
                background-color: #050505;
                color: #e2e8f0;
                font-family: 'Inter', sans-serif;
                padding: 40px;
                max-width: 1200px;
                margin: 0 auto;
            }}
            h1 {{
                background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 40px;
                font-size: 2.5rem;
            }}
            h2 {{ border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 40px; color: #fff; }}
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-bottom: 40px;
            }}
            .metric-card {{
                background: rgba(255, 255, 255, 0.05);
                padding: 20px;
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.1);
                text-align: center;
            }}
            .metric-value {{
                font-size: 2rem;
                font-weight: bold;
                color: #4facfe;
            }}
            .metric-label {{ color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; }}
            .summary-box {{
                background: #0f1115;
                padding: 25px;
                border-radius: 12px;
                border-left: 4px solid #4facfe;
                margin-bottom: 40px;
                white-space: pre-wrap;
                line-height: 1.6;
            }}
            .chart-container {{
                margin-bottom: 50px;
                background: #0f1115;
                padding: 20px;
                border-radius: 12px;
            }}
        </style>
    </head>
    <body>
        <h1>Bitget Wallet Content Analysis</h1>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">平均卡片曝光</div>
                <div class="metric-value">{avg_exp:,.0f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">平均頁面訪問</div>
                <div class="metric-value">{avg_visit:,.0f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">平均文章訪問率 (CTR)</div>
                <div class="metric-value">{avg_article_rate:.2%}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">平均功能轉化率 (CVR)</div>
                <div class="metric-value">{avg_conv_rate:.2%}</div>
            </div>
        </div>

        <h2>📝 題材分析小結 (Theme Analysis)</h2>
        <div class="summary-box">{summary_text}</div>

        <h2>📊 數據視覺化 (Visualizations)</h2>
        {''.join([f'<div class="chart-container">{html}</div>' for html in fig_htmls])}
        
        <div style="text-align: center; margin-top: 50px; color: #666; font-size: 0.8rem;">
            Generated by Bitget Wallet Data Analyzer
        </div>
    </body>
    </html>
    """
    return html_content

# --- Sidebar ---
with st.sidebar:
    st.image("https://cryptologos.cc/logos/bitget-token-bgb-logo.png", width=60)
    st.title("Data Engine")
    st.caption("v2.2 • Premium Edition")
    st.markdown("---")
    
    # Data Source Selection
    source_type = st.radio("資料來源 (Data Source)", ["Excel Upload", "Google Sheets URL"])
    
    uploaded_file = None
    sheet_url = None
    
    if source_type == "Excel Upload":
        uploaded_file = st.file_uploader("📂 Upload Data (.xlsx)", type=["xlsx", "xls"])
    else:
        sheet_url = st.text_input("🔗 Google Sheets Link", help="請確保連結權限已開啟為 '知道連結者皆可檢視' (Anyone with the link can view)")
        st.caption("Auto-converts /edit to /export")

    st.info("支援模糊欄位匹配：\n- dt, title\n- 曝光, 訪問, 點擊, 轉化")

# --- Main App Logic ---
st.title("Bitget Wallet Analytics")

df = None

# 1. Load Data Logic
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ 無法讀取 Excel: {e}")
        
elif sheet_url:
    try:
        # Regex to extract Spreadsheet ID
        # Matches patterns like /d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
        match_id = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url)
        
        if match_id:
            spreadsheet_id = match_id.group(1)
            
            # Regex to extract GID (Sheet ID)
            # Matches gid=0, gid=123456
            match_gid = re.search(r"[#&]gid=([0-9]+)", sheet_url)
            
            # Construct Export URL
            base_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"
            
            if match_gid:
                gid = match_gid.group(1)
                export_url = f"{base_url}&gid={gid}"
            else:
                # If no GID is specified, let Google default to the first sheet
                export_url = base_url
            
            # st.info(f"正在讀取 Google Sheet (ID: {spreadsheet_id})...")
            df = pd.read_csv(export_url)
            
        else:
             st.error("❌ 無法辨識 Google Sheet 連結格式。請確認連結包含 '/d/' 與 ID。")
             
    except Exception as e:
        st.error(f"❌ 無法讀取 Google Sheet。請確認：\n1. 連結權限已開啟為 '知道連結者皆可檢視' (Anyone with the link can view)\n2. 該分頁 (Sheet) 確實存在\n錯誤訊息: {e}")

if df is not None:
    try:
        # Data Cleaning: Normalize columns
        df.columns = df.columns.astype(str).str.strip()
        
        # Fuzzy Match Columns
        col_keyword_map = {
            'dt': 'dt',
            'title': 'title',
            '卡片曝光uv': '卡片曝光',
            '頁面訪問uv': '頁面訪問',
            '文章訪問率': '文章訪問',
            '行動點點擊uv (入口+詳情)': '行動點點擊',
            '功能轉化率': '功能轉化'
        }
        
        missing_cols = []
        for standard_col, keyword in col_keyword_map.items():
            match = next((col for col in df.columns if keyword.lower() in col.lower()), None)
            if match:
                df.rename(columns={match: standard_col}, inplace=True)
            else:
                missing_cols.append(f"{standard_col} (keyword: {keyword})")
        
        if missing_cols:
            st.error("❌ 欄位缺失")
            st.write(missing_cols)
            st.write("偵測到的欄位:", list(df.columns))
            st.stop()
            
        # Type Conversion
        for col in ['卡片曝光uv', '頁面訪問uv', '行動點點擊uv (入口+詳情)']:
            # Remove arrows or commas if present
            df[col] = df[col].astype(str).str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        def convert_pct(val):
            if isinstance(val, str) and '%' in val:
                return float(val.replace('%', '')) / 100
            return float(val)

        df['文章訪問率'] = df['文章訪問率'].apply(convert_pct)
        df['功能轉化率'] = df['功能轉化率'].apply(convert_pct)
        
        # --- Layout Split ---
        col_main, col_settings = st.columns([3.5, 1.2], gap="large")

        # --- Right Settings Panel (Per-Chart Settings) ---
        with col_settings:
            st.header("🛠️ 圖表設定")
            
            # Global Filter
            with st.expander("🌍 全域資料篩選", expanded=True):
                min_exposure = st.slider("最低卡片曝光", 0, 5000, 400, step=100)
                df_global_filtered = df[df['卡片曝光uv'] > min_exposure].copy()
                st.write(f"樣本數: {len(df_global_filtered)}")

            # 1. Overview Chart Settings
            with st.expander("📊 1. 數據總覽設定"):
                show_overview = st.toggle("顯示總覽", value=True)
                ov_chart_type = st.selectbox("圖表類型", ["Bar (長條)", "Line (折線)"], index=0, key="ov_type")
                ov_color = st.color_picker("主色調", "#4facfe", key="ov_color")

            # 2. Custom Charts Gallery (Slots 1-4)
            with st.expander("📊 自定義圖表區 (Custom Charts)", expanded=True):
                st.info("開啟下方圖表槽位，即可在主畫面新增分析圖表。")
                
                chart_configs = []
                
                # --- Slots 1-3: Generic Single Metric ---
                for i in range(1, 4):
                    st.markdown(f"#### 🔹 圖表 {i} (單一指標)")
                    enable = st.toggle(f"啟用圖表 {i}", value=(i<=2), key=f"enable_{i}") # Default enable 1 & 2
                    
                    if enable:
                        metric_col = st.selectbox(
                            f"指標 {i}", 
                            ['功能轉化率', '文章訪問率', '卡片曝光uv', '頁面訪問uv', '行動點點擊uv (入口+詳情)'],
                            index=(i-1) % 5,
                            key=f"metric_{i}"
                        )
                        top_n = st.number_input(f"顯示 Top {i}", 3, 50, 6, key=f"top_n_{i}")
                        c_type = st.selectbox(f"圖表類型 {i}", ["Bar (長條)", "Line (折線)"], key=f"type_{i}")
                        
                        # Individual Filter
                        with st.popover(f"設定圖表 {i} 篩選條件"):
                            st.markdown("**(AND 邏輯)**")
                            filter_candidates = [c for c in df.columns if c not in ['dt', 'title']]
                            selected_filters = st.multiselect(f"篩選欄位 {i}", filter_candidates, key=f"filters_{i}")
                            current_filters = {}
                            for f_col in selected_filters:
                                default_val = 400.0 if '曝光' in f_col else 0.0
                                val = st.number_input(f"{f_col} >", value=default_val, key=f"fv_{i}_{f_col}")
                                current_filters[f_col] = val
                        
                        chart_configs.append({
                            "id": i,
                            "type": "generic",
                            "metric": metric_col,
                            "top_n": top_n,
                            "chart_type": c_type,
                            "filters": current_filters
                        })
                    st.markdown("---")

                # --- Slot 4: Fully Custom Combo Chart ---
                st.markdown(f"#### 🔸 圖表 4 (自由組合分析)")
                st.info("可自行新增多個指標，並設定類型 (Bar/Line) 與座標軸。")
                enable_4 = st.toggle(f"啟用圖表 4", value=True, key="enable_4")
                
                if enable_4:
                    top_n_4 = st.number_input(f"顯示 Top (圖4)", 3, 50, 10, key="top_n_4")
                    
                    # 1. Select Metrics
                    metric_options = ['卡片曝光uv', '頁面訪問uv', '行動點點擊uv (入口+詳情)', '文章訪問率', '功能轉化率']
                    selected_metrics_4 = st.multiselect(
                        "選擇要顯示的指標 (多選)", 
                        metric_options, 
                        default=['卡片曝光uv', '功能轉化率'],
                        key="combo_metrics_4"
                    )
                    
                    # 2. Configure each metric
                    combo_config = {}
                    if selected_metrics_4:
                        st.markdown("**指標細項設定:**")
                        for m_idx, m in enumerate(selected_metrics_4):
                            with st.popover(f"⚙️ 設定: {m}"):
                                c1, c2 = st.columns(2)
                                c_type = c1.selectbox(f"類型", ["Bar", "Line"], index=0 if '曝光' in m else 1, key=f"c4_type_{m_idx}")
                                c_axis = c2.selectbox(f"軸向", ["左軸 (主)", "右軸 (副)"], index=0 if '曝光' in m else 1, key=f"c4_axis_{m_idx}")
                                combo_config[m] = {'type': c_type, 'axis': c_axis}

                    # 3. Filter
                    with st.popover(f"設定圖表 4 篩選條件"):
                        st.markdown("**(AND 邏輯)**")
                        filter_candidates_4 = [c for c in df.columns if c not in ['dt', 'title']]
                        selected_filters_4 = st.multiselect(f"篩選欄位 (圖4)", filter_candidates_4, default=['卡片曝光uv'], key="filters_4")
                        current_filters_4 = {}
                        for f_col in selected_filters_4:
                            default_val = 400.0 if '曝光' in f_col else 0.0
                            val = st.number_input(f"{f_col} >", value=default_val, key=f"fv_4_{f_col}")
                            current_filters_4[f_col] = val
                    
                    chart_configs.append({
                        "id": 4,
                        "type": "custom_combo",
                        "top_n": top_n_4,
                        "metrics_config": combo_config,
                        "filters": current_filters_4
                    })

            # 3. Correlation Settings
            with st.expander("🔥 3. 關聯分析設定"):
                show_correlation = st.toggle("顯示關聯分析", value=True)
                corr_color_exp = st.color_picker("曝光顏色", "#00f2fe", key="corr_c1")
                corr_color_conv = st.color_picker("轉化顏色", "#fbc2eb", key="corr_c2")

        # --- Main Dashboard (Left Column) ---
        with col_main:
            # 1. Custom Metric Cards (Based on Global Filter)
            m1, m2, m3, m4 = st.columns(4)
            
            def metric_card(col, label, value):
                col.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)
                
            avg_exp = df_global_filtered['卡片曝光uv'].mean()
            avg_visit = df_global_filtered['頁面訪問uv'].mean()
            # Handle empty data case
            if len(df_global_filtered) == 0:
                st.warning("⚠️ 篩選條件過於嚴格，無數據可顯示。")
                st.stop()
                
            avg_article_rate = df_global_filtered['文章訪問率'].mean()
            avg_conv_rate = df_global_filtered['功能轉化率'].mean()

            metric_card(m1, "平均卡片曝光", f"{avg_exp:,.0f}")
            metric_card(m2, "平均頁面訪問", f"{avg_visit:,.0f}")
            metric_card(m3, "平均文章訪問 (CTR)", f"{avg_article_rate:.2%}")
            metric_card(m4, "平均功能轉化 (CVR)", f"{avg_conv_rate:.2%}")

            st.markdown("<br>", unsafe_allow_html=True)

            # 2. Charts
            figs = []
            
            # Helper for standard chart layout
            def update_chart_layout(fig, title_text=""):
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        showgrid=False, 
                        tickangle=-45,  # Rotate labels to prevent squeezing
                        automargin=True,
                        title=None
                    ),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
                    legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center", font=dict(size=12)),
                    margin=dict(t=60, b=100, r=50), # Extra margins
                    uniformtext_minsize=8, 
                    uniformtext_mode='hide',
                    hovermode="x unified" # Enable unified tooltip for combo charts
                )
                if title_text:
                    fig.update_layout(title=dict(text=title_text, x=0.5, xanchor='center'))
                return fig

            # Overview
            if show_overview:
                st.markdown("### 📈 Performance Overview (Dual Axis)")
                
                # Sort by Exposure
                df_ov = df_global_filtered.sort_values(by='卡片曝光uv', ascending=False)
                
                fig_overview = make_subplots(specs=[[{"secondary_y": True}]])
                
                # Big Numbers: Exposure (Left Axis, Bar)
                fig_overview.add_trace(
                    go.Bar(
                        x=df_ov['title'], y=df_ov['卡片曝光uv'], name='Exp. (L)', 
                        marker_color='#4facfe', opacity=0.7,
                        text=df_ov['卡片曝光uv'], textposition='outside', texttemplate='<b>%{y:.0f}</b>',
                        textfont=dict(color='white', size=12),
                        offsetgroup=1,
                        hovertemplate="%{y:.0f}" # Simplified for unified view
                    ),
                    secondary_y=False
                )

                # Smaller Numbers: Visits & Clicks (Right Axis, Lines/Scatter)
                # Visits
                fig_overview.add_trace(
                    go.Scatter(
                        x=df_ov['title'], y=df_ov['頁面訪問uv'], name='Visits (R)',
                        line=dict(color='#a18cd1', width=3), mode='lines+markers+text',
                        text=df_ov['頁面訪問uv'], textposition='top center', texttemplate='<b>%{y:.0f}</b>',
                        textfont=dict(color='white', size=12),
                        hovertemplate="%{y:.0f}"
                    ),
                    secondary_y=True
                )
                
                # Clicks
                fig_overview.add_trace(
                    go.Scatter(
                        x=df_ov['title'], y=df_ov['行動點點擊uv (入口+詳情)'], name='Clicks (R)',
                        line=dict(color='#ff9f43', width=3), mode='lines+markers+text',
                        text=df_ov['行動點點擊uv (入口+詳情)'], textposition='bottom center', texttemplate='<b>%{y:.0f}</b>',
                        textfont=dict(color='white', size=12),
                        hovertemplate="%{y:.0f}"
                    ),
                    secondary_y=True
                )
                
                update_chart_layout(fig_overview)
                
                # Adjust Axes
                fig_overview.update_layout(
                    yaxis=dict(title="Exposure", side="left", showgrid=True),
                    yaxis2=dict(title="Visits & Clicks", side="right", overlaying="y", showgrid=False),
                    barmode='group' 
                )
                st.plotly_chart(fig_overview, use_container_width=True)
                figs.append(fig_overview)

            # Customizable Charts (Slots 1-4)
            if chart_configs:
                # Layout: 2 cols per row
                chart_cols = st.columns(2)
                
                for idx, config in enumerate(chart_configs):
                    with chart_cols[idx % 2]:
                        # --- Apply Specific Filters ---
                        df_chart = df.copy()
                        mask = pd.Series([True] * len(df_chart), index=df_chart.index)
                        filter_txt = []
                        
                        for f_col, f_val in config['filters'].items():
                             if pd.api.types.is_numeric_dtype(df_chart[f_col]):
                                mask = mask & (df_chart[f_col] > f_val)
                                filter_txt.append(f"{f_col}>{f_val}")
                        
                        df_chart = df_chart[mask]
                        
                        # --- Render ---
                        if len(df_chart) == 0:
                            st.warning(f"圖表 {config['id']}: 無符合數據")
                            continue
                            
                        top_n = config['top_n']
                        
                        if config['type'] == 'generic':
                            metric = config['metric']
                            st.markdown(f"### 📊 Chart {config['id']}: {metric}")
                            if filter_txt: st.caption(f"Filter: {', '.join(filter_txt)}")
                            
                            # Sort Descending
                            top_data = df_chart.nlargest(min(top_n, len(df_chart)), metric)
                            
                            # Simple High Contrast Color
                            chart_color = '#00f2fe' if idx % 2 == 0 else '#fbc2eb'
                            
                            is_rate = '率' in metric
                            fmt = '.1%' if is_rate else '.0f'
                            
                            if "Bar" in config['chart_type']:
                                fig = px.bar(
                                    top_data, x='title', y=metric, 
                                    text=metric
                                )
                                fig.update_traces(
                                    marker_color=chart_color,
                                    texttemplate=f'<b>%{{y:{fmt}}}</b>',
                                    textposition='outside',
                                    cliponaxis=False,
                                    textfont=dict(color='white', size=12),
                                    hovertemplate=f"%{{y:{fmt}}}<extra></extra>"
                                )
                            else:
                                fig = px.line(
                                    top_data, x='title', y=metric, 
                                    markers=True, text=metric
                                )
                                fig.update_traces(
                                    line_color=chart_color,
                                    texttemplate=f'<b>%{{y:{fmt}}}</b>',
                                    textposition='top center',
                                    cliponaxis=False,
                                    textfont=dict(color='white', size=12),
                                    hovertemplate=f"%{{y:{fmt}}}<extra></extra>"
                                )
                                
                            update_chart_layout(fig)
                            st.plotly_chart(fig, use_container_width=True)
                            figs.append(fig)
                            
                        elif config['type'] == 'custom_combo':
                            st.markdown(f"### 🔸 Chart {config['id']}: Multi-Metric Combo")
                            if filter_txt: st.caption(f"Filter: {', '.join(filter_txt)}")
                            
                            # Sort Logic: Sort by the first Bar chart metric found, else first Line metric.
                            metrics_cfg = config['metrics_config']
                            if not metrics_cfg:
                                st.warning("請至少選擇一個指標")
                                continue
                                
                            # Determine Sort Column (First Bar or First Metric)
                            sort_col = list(metrics_cfg.keys())[0]
                            for m, cfg in metrics_cfg.items():
                                if cfg['type'] == 'Bar':
                                    sort_col = m
                                    break
                            
                            # Sort Descending
                            top_data = df_chart.nlargest(min(top_n, len(df_chart)), sort_col)
                            
                            fig = make_subplots(specs=[[{"secondary_y": True}]])
                            
                            # Color Palette generator
                            colors = ['#00f2fe', '#fbc2eb', '#4facfe', '#ff9f43', '#a18cd1']
                            
                            # Track Scaling for range adjustment
                            max_l, max_r = 0, 0
                            
                            for m_i, (metric_name, m_cfg) in enumerate(metrics_cfg.items()):
                                color = colors[m_i % len(colors)]
                                is_sec = (m_cfg['axis'] == "右軸 (副)")
                                is_rate = '率' in metric_name
                                fmt = '.1%' if is_rate else '.0f'
                                
                                # Update Max for range
                                current_max = top_data[metric_name].max()
                                if is_sec:
                                    max_r = max(max_r, current_max)
                                else:
                                    max_l = max(max_l, current_max)
                                
                                # Visual adjustments
                                if m_cfg['type'] == 'Bar':
                                    fig.add_trace(
                                        go.Bar(
                                            x=top_data['title'], y=top_data[metric_name], 
                                            name=f"{metric_name} ({'R' if is_sec else 'Main'})",
                                            marker_color=color, opacity=0.8,
                                            text=top_data[metric_name], textposition='outside', 
                                            texttemplate=f'<b>%{{y:{fmt}}}</b>',
                                            textfont=dict(color='white', size=12), # Reduced slightly for density
                                            hovertemplate=f"%{{y:{fmt}}}" # Clean for unified
                                        ),
                                        secondary_y=is_sec
                                    )
                                else:
                                    fig.add_trace(
                                        go.Scatter(
                                            x=top_data['title'], y=top_data[metric_name],
                                            name=f"{metric_name} ({'R' if is_sec else 'Main'})",
                                            mode='lines+markers+text',
                                            line=dict(color=color, width=4),
                                            marker=dict(size=10, line=dict(width=2, color='white')), # Pop markers
                                            text=top_data[metric_name], textposition='top center',
                                            texttemplate=f'<b>%{{y:{fmt}}}</b>',
                                            textfont=dict(color='white', size=12),
                                            hovertemplate=f"%{{y:{fmt}}}"
                                        ),
                                        secondary_y=is_sec
                                    )
                            
                            update_chart_layout(fig)
                            
                            # Axis Titles & Range Padding (to fit 'outside' text)
                            fig.update_layout(
                                yaxis=dict(title="Main Axis", showgrid=True, range=[0, max_l * 1.25]),
                                yaxis2=dict(title="Secondary Axis", showgrid=False, overlaying='y', side='right', range=[0, max_r * 1.25]),
                                barmode='group',
                                # Unified hover enabled in update_chart_layout
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            figs.append(fig)

        # 3. Summary Section
        st.markdown("---")
        st.markdown("### 🧠 Insight Generation")
        
        # Ensure df_global_filtered is used for summary if df_filtered is not defined elsewhere
        # Assuming df_filtered should be df_global_filtered for consistency with metric cards
        top_titles_conv = df_global_filtered.nlargest(3, '功能轉化率')['title'].tolist()
        default_summary = f"""**本期數據洞察 (Automated Insights)：**

1. **高轉化 (High CVR)**：
   - 「{top_titles_conv[0] if top_titles_conv else 'N/A'}」表現最佳。
   - 建議：分析該篇的 Call-to-Action 與排版結構。

2. **策略建議 (Strategy)**：
   - (在此輸入您的觀察...)
"""
        analysis_input = st.text_area("Analysis Summary", value=default_summary, height=250)
        
        # 4. Export Options
        st.markdown("---")
        st.subheader("📤 匯出與分享 (Export & Share)")
        st.info("💡 **如何分享報告？**\n下載下方的 **HTML 網頁報告**，您可以直接將檔案傳送給同事，或上傳至 Google Drive / 公司內網，即可生成分享連結。")
        
        col_dl1, col_dl2 = st.columns(2)
        
        # Option 1: Markdown
        with col_dl1:
            report_md = f"# Bitget Data Report\n{analysis_input}"
            st.download_button("📝 下載 Markdown 筆記", report_md, "report.md")
            
        # Option 2: HTML Output (Web Link Equivalent)
        with col_dl2:
            html_report = create_html_report(df_global_filtered, analysis_input, figs)
            st.download_button(
                label="🌐 下載完整分析報告 (HTML 網頁)",
                data=html_report,
                file_name=f"Bitget_Analysis_Report_{pd.Timestamp.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                help="下載後可直接用瀏覽器開啟，保留所有互動圖表功能。"
            )

    except Exception as e:
        st.error(f"Error: {e}")
        st.exception(e)

else:
    # Landing Page
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 20px;'>Data Intelligence</h1>
        <p style='color: #94a3b8; font-size: 1.2rem;'>Advanced Analytics for Bitget Wallet Content</p>
    </div>
    """, unsafe_allow_html=True)
