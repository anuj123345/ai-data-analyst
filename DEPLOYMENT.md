# 🚀 Deployment Guide (Streamlit Community Cloud)

Since `git` is not installed on your local machine, we will deploy using the **Manual Upload** method.

## Phase 1: Upload Code to GitHub
1.  **Log in** to your [GitHub Account](https://github.com/).
2.  **Create a New Repository**:
    -   Go to [github.com/new](https://github.com/new).
    -   **Repository Name:** `ai-data-analyst` (or any name you like).
    -   **Public/Private:** Public is easier, Private works too.
    -   **Initialize:** Leave everything unchecked.
    -   Click **Create repository**.
3.  **Upload Files**:
    -   On the next screen, look for the link: *"uploading an existing file"*. Click it.
    -   **Open your local folder:** `c:\Users\anujb\.gemini\antigravity\playground\crystal-kuiper\ai_data_visualisation_agent`
    -   **Select ALL files** (`ai_data_visualisation_agent.py`, `requirements.txt`, etc.) and **Drag & Drop** them into the GitHub page.
    -   Wait for upload to finish.
    -   **Commit changes:** Type "Initial deploy" in the box and click **Commit changes**.

## Phase 2: Deploy on Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **New app**.
3.  **Connect to GitHub** (if asked).
4.  **Select Repository:** Choose `ai-data-analyst` (the one you just made).
5.  **Main file path:** `ai_data_visualisation_agent.py`
6.  Click **Deploy!** 🎈

## Phase 3: Configure Secrets (Crucial!)
The app needs your API keys to work.
1.  On your deployed app, click the **Settings menu** (3 dots at top-right or bottom-right) -> **Settings**.
2.  Go to **Secrets**.
3.  Paste the following content:
    ```toml
    OPENROUTER_API_KEY = "your-key-here"
    ```
4.  Click **Save**.

## ✅ Done!
Your app is now live and can be shared with anyone.
