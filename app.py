import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import html  # 引入 HTML 轉義模組

# --- Page Config ---
st.set_page_config(
    page_title="Bitget Wallet Analytics",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Premium Design System ---
# (保留原本的 CSS 部份，這部分是靜態定義的，安全性無虞)
st.markdown("""
<style>
    /* ... 這裡省略重複的 CSS 代碼 ... */
</style>
""", unsafe_allow_html=True)

# --- Helper Function: Generate HTML Report ---
def create_html_report(df_filtered, summary_text, figs):
    """Generates a standalone HTML file with protection against XSS."""
    
    # 補強：對使用者輸入的文字進行 HTML 轉義，防止 XSS
    safe_summary = html.escape(summary_text).replace('\n', '<br>')
    
    avg_exp = df_filtered['卡片曝光uv'].mean()
    avg_visit = df_filtered['頁面訪問uv'].mean()
    avg_article_rate = df_filtered['文章訪問率'].mean()
    avg_conv_rate = df_filtered['功能轉化率'].mean()
    
    fig_htmls = [fig.to_html(full_html=False, include_plotlyjs='cdn') for fig in figs]
    
    # 使用轉義後的 safe_summary
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bitget Wallet Analysis Report</title>
        <meta charset="utf-8">
        <style>
            /* ... 保留原有樣式 ... */
            body {{ background-color: #050505; color: #e2e8f0; font-family: 'Inter', sans-serif; padding: 40px; }}
            .summary-box {{ background: #0f1115; padding: 25px; border-radius: 12px; border-left: 4px solid #4facfe; line-height: 1.6; }}
        </style>
    </head>
    <body>
        <h1>Bitget Wallet Content Analysis</h1>
        <h2>📝 題材分析小結</h2>
        <div class="summary-box">{safe_summary}</div>
        <h2>📊 數據視覺化</h2>
        {''.join([f'<div class="chart-container">{h}</div>' for h in fig_htmls])}
    </body>
    </html>
    """
    return html_content

# --- Main App Logic ---
# (Sidebar 部份略過，邏輯相同)

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error("❌ 無法讀取 Excel 檔案，請檢查格式是否正確。")
        # st.exception(e)  <-- 移除，不洩漏詳細錯誤資訊

elif sheet_url:
    try:
        # 補強：使用更嚴謹的正則表達式
        match_id = re.search(r"/d/([a-zA-Z0-9-_]{25,})", sheet_url)
        
        if match_id:
            spreadsheet_id = match_id.group(1)
            match_gid = re.search(r"[#&]gid=([0-9]+)", sheet_url)
            
            base_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"
            export_url = f"{base_url}&gid={match_gid.group(1)}" if match_gid else base_url
            
            df = pd.read_csv(export_url)
        else:
            st.error("❌ 無法辨識 Google Sheet 連結，請確認格式。")
    except Exception as e:
        st.error("❌ 讀取雲端資料夾失敗。請確保連結權限已開啟為「知道連結者皆可檢視」。")

# --- 後續數據處理 ---
if df is not None:
    try:
        # 資料清洗補強：強制轉換類型並移除潛在的惡意字元
        for col in ['卡片曝光uv', '頁面訪問uv', '行動點點擊uv (入口+詳情)']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)

        # ... (中間繪圖邏輯保持不變) ...

        # 輸出部分
        st.markdown("### 🧠 Insight Generation")
        # 預設文字也要轉義或確保安全
        analysis_input = st.text_area("Analysis Summary", value=default_summary, height=250)
        
        # 下載按鈕 (HTML Report 已經過安全過濾)
        html_report = create_html_report(df_global_filtered, analysis_input, figs)
        st.download_button(
            label="🌐 下載完整分析報告 (HTML 網頁)",
            data=html_report,
            file_name=f"Bitget_Analysis_Report.html",
            mime="text/html"
        )

    except Exception as e:
        # 補強：不顯示完整的 Exception Traceback
        st.error(f"分析過程中發生預期外的錯誤。")
        # 若需要內部除錯，可使用 st.write(str(e)) 但避免 st.exception(e)
