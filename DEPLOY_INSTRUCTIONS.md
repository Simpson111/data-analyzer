# 🚀 如何將此應用程式發佈為網站 (Deployment Guide)

目前的 `app.py` 是一個 Streamlit 應用程式，若要讓其他人透過連結訪問，最推薦的方式是部署到 **Streamlit Community Cloud** (免費且官方支援)。

## 📋 準備工作 (已完成)

您的專案目錄中已經包含以下必要檔案：
1.  `app.py`: 主程式碼
2.  `requirements.txt`: 依賴套件清單 (包含 streamlit, pandas, plotly 等)
3.  `.streamlit/config.toml`: 設定檔

---

## ☁️ 方法一：使用 Streamlit Community Cloud (推薦)

這是最正規且穩定的方式，支援自動更新 (當您修改 GitHub 程式碼時，網站會自動更新)。

### 步驟 1：上傳程式碼至 GitHub (三種方式)

由於您的電腦可能尚未安裝 Git 指令工具，我們推薦以下兩種簡單方式：

#### 🌟 方式 A：直接在網頁上傳 (最簡單，免安裝)
1.  登入 [GitHub](https://github.com/) 建立一個新的 Repository (例如 `bitget-analyzer`)。
    *   *Public* 或 *Private* 皆可 (Streamlit Community Cloud 支援 Private Repo)。
    *   勾選 "Add a README file" 以便初始化。
2.  在 Repository 頁面，點擊 **"Add file"** -> **"Upload files"**。
3.  直接將本資料夾 (`data-analyzer-st`) 內的所有檔案拖曳進去。
    *   ⚠️ **重要**：請確保 `.streamlit` 資料夾也有拖進去 (這是隱藏資料夾，若看不到請在檔案總管開啟「顯示隱藏項目」)。
4.  在下方 "Commit changes" 處輸入備註 (例如 "Initial commit")，點擊綠色按鈕提交。

#### 🖥️ 方式 B：使用 GitHub Desktop (推薦長期使用)
1.  下載並安裝 [GitHub Desktop](https://desktop.github.com/)。
2.  開啟 GitHub Desktop，登入您的帳號。
3.  點擊 **"File"** -> **"New Repository..."**。
4.  輸入 Name (例如 `bitget-analyzer`)，Local Path 選擇您目前的專案資料夾位置。
5.  點擊 **"Create Repository"**。
6.  點擊 **"Publish repository"** 將其推送到 GitHub 網站。

#### ⌨️ 方式 C：使用 Git指令 (適合工程師)
若您已安裝 Git，請開啟終端機 (Terminal) 並依序執行：
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
# 請先在 GitHub 建立一個空 Repo，並複製其 URL
git remote add origin https://github.com/您的帳號/repo名稱.git
git push -u origin main
```

### 步驟 2：部署到 Streamlit Cloud

### 步驟 2：部署到 Streamlit Cloud
1.  前往 [Streamlit Community Cloud](https://streamlit.io/cloud) 並登入 (建議使用 GitHub 帳號登入)。
2.  點擊右上角的 **"New app"**。
3.  選擇您剛剛建立的 GitHub Repository。
4.  設定如下：
    *   **Main file path**: `app.py`
5.  點擊 **"Deploy!"**。

### 🎉 完成！
部署過程約需 1-2 分鐘。完成後，您會獲得一個專屬網址 (例如 `https://bitget-analyzer.streamlit.app`)，您可以將此連結分享給任何人。

---

## 🤗 方法二：使用 Hugging Face Spaces (免 Git 指令)

如果您不想使用 GitHub 指令，Hugging Face 提供更直覺的網頁上傳介面。

1.  註冊/登入 [Hugging Face](https://huggingface.co/)。
2.  點擊 **New Space**。
3.  **SDK** 選擇 **Streamlit**。
4.  建立後，在該 Space 的頁面中選擇 **"Files"** -> **"Add file"** -> **"Upload files"**。
5.  直接拖曳本機資料夾內的所有檔案上傳。
6.  點擊 **Commit changes**，系統會自動開始建置並產生網址。

---

## ⚡ 方法三：臨時分享 (Ngrok)

若您只是想「暫時」分享給正在開會的同事，不想部署：
1.  安裝 [ngrok](https://ngrok.com/)。
2.  在終端機執行：`ngrok http 8501` (假設您的 Streamlit 運作在 Port 8501)。
3.  複製終端機顯示的 `https://xxxx.ngrok-free.app` 連結給對方即可。
    *   *注意：當您關閉終端機或電腦時，連結即失效。*
