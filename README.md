# 📊 AI Data Analyst Agent (Powered by NVIDIA NIM)

An intelligent, two-step autonomous data visualization and analysis agent. Simply upload a CSV and ask a question in natural language—the agent will write the code, execute it locally, and provide professional insights alongside interactive tables and charts.

## ✨ Features

- **Two-Step Agent Architecture**: 
  - 🛠️ **Coder Agent**: Reads your query, understands your CSV schema, and generates the exact Python code needed to answer your question.
  - 🧠 **Analyst Agent**: Takes the raw numbers and tables outputted by the executed code and translates them into a highly structured, professional written analysis.
- **Dynamic Recommended Questions**: Automatically scans your uploaded CSV and recommends highly relevant, dataset-specific questions so you don't have to guess what to ask!
- **100% Local Execution**: Python code is executed natively and securely on your local machine using Python's `exec()`. Enjoy zero-latency computations with no third-party cloud sandbox subscriptions required.
- **Advanced Reasoning Models**: Powered by NVIDIA NIM's state-of-the-art reasoning APIs:
  - `deepseek-ai/deepseek-v4-flash` (Default)
  - `moonshotai/kimi-k2.6`
- **Smart Data Formatting**: Dynamically detects when the AI creates Pandas DataFrames and renders them as beautiful, interactive Streamlit tables.

## 📋 Prerequisites

- Python 3.10+
- **NVIDIA NIM API Key**: Get it for free at [build.nvidia.com](https://build.nvidia.com/)

## 🚀 Quick Start

1. **Clone or Download the Project**
```bash
git clone https://github.com/your-username/ai-data-analyst.git
cd ai-data-analyst
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```
*(Requires: `streamlit`, `pandas`, `openai`, `matplotlib`, `seaborn`)*

3. **Run the Application**
```bash
streamlit run ai_data_visualisation_agent.py
```
The application will open in your default browser at `http://localhost:8501`.

## 📖 How to Use

1. **Upload Your Dataset**
   - Click "Browse files" to upload any CSV file.
   - Instantly view dataset statistics, column info, and data types.

2. **Get Smart Recommendations**
   - As soon as your file uploads, the AI scans your schema and generates 4 custom-tailored analytical questions you can ask immediately.

3. **Ask Questions & Analyze**
   - Select a recommended question or type your own natural language query.
   - Click **Analyze**.
   - The AI will execute the math and print a professional **Analytical Insight** paragraph followed by interactive tables and charts!

## 💡 Example Queries

- *"Find all the columns with missing or null values and show me a count of how many nulls each column has."*
- *"Group the data by category and show me the total sum of the financial values for each group in a table."*
- *"Filter the dataset to only show businesses that performed above the overall average, and display the top 5."*
- *"Create a beautiful bar chart showing the total revenue grouped by the top 5 industries."*

## 🗂️ Project Structure

```text
ai_data_visualisation_agent/
├── ai_data_visualisation_agent.py    # Main Streamlit application
├── requirements.txt                  # Python dependencies
├── sample_data.csv                   # Sample dataset for testing
└── README.md                         # This file
```

## 🛠️ Troubleshooting

**Missing Packages / Execution Errors:**
Since the AI executes code locally on your machine, it has access to the libraries you have installed. If the AI tries to use a specialized library that you don't have installed, you may see an execution error. Stick to Pandas, Numpy, Matplotlib, and Seaborn for best results.

**Failed to generate LLM response:**
If you receive a response error from the NVIDIA API, ensure you are connected to the internet and that your NVIDIA API key is valid and has sufficient credits.

## 📝 License
This project is open source and available under the MIT License.

## 🙏 Acknowledgments
Built with:
- **Streamlit** - Web framework
- **NVIDIA NIM** - LLM inference & Reasoning Models
- **Pandas** - Data manipulation
- **Matplotlib & Seaborn** - Visualizations
