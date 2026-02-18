# 📊 AI Data Analyst (Powered by OpenRouter)

An intelligent data visualization and analysis agent that builds charts, tables, and insights from your CSV/Excel datasets using natural language.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenRouter](https://img.shields.io/badge/AI-OpenRouter-7450f6?style=for-the-badge)

## ✨ Features
- **Natural Language Analysis**: Ask "What are the top skills?" or "Show me a bar chart of salaries".
- **Multi-Model Support** (via OpenRouter):
    -   **[FREE]** Google Gemini 2.0 Flash (Default)
    -   **[FREE]** Llama 3.3 70B
    -   **[PREMIUM]** DeepSeek R1 (Reasoning)
    -   **[PREMIUM]** GPT-4o & Claude 3.5 Sonnet
- **Robustness**:
    -   **Auto-Retry**: Automatically handles API credit limits by optimizing token usage.
    -   **Model Fallback**: Switches to free models if premium ones are busy.
    -   **Smart Cleaning**: Handles messy CSV data (lists, dates, typos) automatically.
- **Secure Execution**: Code runs in a sandboxed environment (E2B).
- **Payment Gateway**: Mock integration for Premium features (Razorpay/Stripe).

## 📋 Prerequisites
-   **Python 3.10+**
-   **OpenRouter API Key**: [Get it here](https://openrouter.ai/keys)
-   **E2B API Key**: [Get it here](https://e2b.dev)

## 🚀 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/ai-data-analyst.git
    cd ai-data-analyst
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**:
    ```bash
    streamlit run ai_data_visualisation_agent.py
    ```

## 🛠️ Configuration
Enter your **OpenRouter API Key** in the sidebar to start. 
The app defaults to the **Free Mode** (Gemini 2.0 Flash) so you can test without cost!

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
cd ai_data_visualisation_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web application framework
- `pandas` - Data manipulation
- `groq` - Fast LLM inference
- `e2b-code-interpreter` - Secure code execution
- `matplotlib`, `seaborn` - Visualization libraries

### 3. Get Your API Keys

#### Groq API Key (Free)
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Create a new API key
4. Copy and save it securely

#### E2B API Key
1. Visit [E2B Documentation](https://e2b.dev/docs)
2. Sign up for an account
3. Generate an API key from your dashboard
4. Copy and save it securely

### 4. Run the Application

```bash
streamlit run ai_data_visualisation_agent.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter API Keys**
   - Open the sidebar
   - Paste your Together AI API key
   - Paste your E2B API key

2. **Select a Model**
   - Choose your preferred LLM model from the dropdown
   - Different models have different strengths (speed vs. accuracy)

3. **Upload Your Dataset**
   - Click "Browse files" to upload a CSV file
   - Or use the included `sample_data.csv` to test

4. **Preview Your Data**
   - View dataset statistics (rows, columns, size)
   - See a preview of your data
   - Check column information and data types

5. **Ask Questions**
   - Type a natural language query about your data
   - Or select from example queries
   - Examples:
     - "Show me the distribution of values in the Price column"
     - "Create a bar chart comparing sales by category"
     - "What are the top 10 products by sales?"
     - "Show correlation between Price and Rating"

6. **Get Visualizations**
   - Click the "Analyze" button
   - The AI will generate and execute code
   - View the generated visualization instantly

## 💡 Example Queries

Here are some queries you can try with the sample dataset:

- **Distribution Analysis**
  - "Show me a histogram of prices"
  - "What's the distribution of ratings across products?"

- **Comparative Analysis**
  - "Compare average sales by category using a bar chart"
  - "Show sales trends by region"

- **Correlation Analysis**
  - "Create a scatter plot of price vs sales"
  - "Show me the correlation matrix for numeric columns"

- **Top/Bottom Analysis**
  - "What are the top 5 products by sales?"
  - "Show the lowest rated products"

- **Custom Visualizations**
  - "Create a bubble chart with price, sales, and ratings"
  - "Show a pie chart of sales distribution by category"

## 🗂️ Project Structure

```
ai_data_visualisation_agent/
├── ai_data_visualisation_agent.py   # Main Streamlit application
├── requirements.txt                  # Python dependencies
├── sample_data.csv                   # Sample dataset for testing
├── .env.example                      # Environment variable template
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

## 🔧 Configuration

### Environment Variables (Optional)

You can set API keys via environment variables instead of the UI:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your keys:
   ```
   TOGETHER_API_KEY=your_together_ai_api_key
   E2B_API_KEY=your_e2b_api_key
   ```

3. Modify the app to load from environment:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   st.session_state.together_api_key = os.getenv('TOGETHER_API_KEY', '')
   st.session_state.e2b_api_key = os.getenv('E2B_API_KEY', '')
   ```

## 🎨 Supported Visualization Types

- **Line Charts** - Time series and trends
- **Bar Charts** - Comparisons and rankings
- **Scatter Plots** - Relationships and correlations
- **Pie Charts** - Proportions and distributions
- **Bubble Charts** - Multi-dimensional data
- **Histograms** - Frequency distributions
- **Box Plots** - Statistical distributions
- **Heatmaps** - Correlation matrices
- **And more!** - The AI can generate custom visualizations

## 🛠️ Troubleshooting

### Common Issues

**1. API Key Errors**
- Verify your API keys are correct
- Check that you have credits/quota remaining
- Ensure there are no extra spaces in the keys

**2. Dataset Upload Fails**
- Ensure your file is in CSV format
- Check that the file size is reasonable (< 10MB)
- Verify the file is not corrupted

**3. Code Execution Errors**
- Try rephrasing your query
- Ensure your dataset has the columns mentioned in the query
- Check the "View Generated Code" expander to see what was generated

**4. No Visualizations Appear**
- Verify both API keys are entered
- Check your internet connection
- Try a simpler query first
- Look for error messages in the UI

### Getting Help

If you encounter issues:
1. Check the error messages in the app
2. Review the generated code in the expander
3. Try with the sample dataset first
4. Verify API keys are valid

## 🚀 Future Enhancements

Potential improvements you could add:

- **More File Formats** - Support for Excel, JSON, SQL databases
- **Visualization Templates** - Pre-built templates for common queries
- **Export Options** - Save visualizations as PNG, PDF, SVG
- **Memory/History** - Remember previous queries and preferences
- **Multi-dataset Support** - Compare multiple datasets
- **Advanced Analytics** - Statistical tests, machine learning models
- **Customization** - Color themes, chart styling options

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [Together AI](https://www.together.ai/) - LLM inference
- [E2B](https://e2b.dev/) - Secure code execution
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [Matplotlib](https://matplotlib.org/), [Plotly](https://plotly.com/), [Seaborn](https://seaborn.pydata.org/) - Visualizations

## 📧 Contact

For questions or feedback, please open an issue or reach out!

---

**Made with ❤️ for data enthusiasts and CV builders**
