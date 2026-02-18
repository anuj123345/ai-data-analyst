import os
import re
import io
import contextlib
import warnings
from typing import Optional, List, Any, Tuple
from PIL import Image
import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from openai import OpenAI
from e2b_code_interpreter import Sandbox

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def code_interpret(e2b_code_interpreter: Sandbox, code: str) -> Optional[List[Any]]:
    """Execute Python code in E2B sandbox and return results."""
    with st.spinner('Executing code in E2B sandbox...'):
        try:
            exec_result = e2b_code_interpreter.run_code(code)
            
            if exec_result.error:
                st.error(f"Code execution error: {exec_result.error}")
                return None
            
            return exec_result.results
        except Exception as error:
            st.error(f"Error executing code: {error}")
            return None

def extract_python_code(response_text: str) -> str:
    """Extract Python code from LLM response with robust fallback."""
    # Pattern 1: Standard ```python code ```
    match = re.search(r'```python\s*(.*?)```', response_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
        
    # Pattern 2: Generic ``` code ```
    match = re.search(r'```\s*(.*?)```', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
        
    # Fallback: If no code blocks found, but it looks like code, return it.
    # But often LLM returns raw code without blocks if it's very short.
    # ALSO: Sometimes it returns ```python at start but no end.
    cleaned = response_text.replace("```python", "").replace("```", "").strip()
    return cleaned

def chat_with_llm(e2b_code_interpreter: Sandbox, user_message: str, dataset_path: str, df: pd.DataFrame) -> Tuple[Optional[List[Any]], str]:
    """Interact with OpenRouter LLM to generate and execute visualization code."""
    
    # Get column info for the prompt with SAMPLES
    # Get column info for the prompt with SAMPLES
    columns_list = []
    for col, dtype in zip(df.columns, df.dtypes):
        sample_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else "N/A"
        columns_list.append(f"- {col} ({dtype}) | Sample: '{str(sample_val)[:50]}...'")
    
    columns_info = "\n".join(columns_list)
    
    system_prompt = f"""You're a Python data scientist and visualization expert.

The dataset is available at path '{dataset_path}'.

Available Columns:
{columns_info}

Your task is to:
1. Load the dataset using pandas: df = pd.read_csv('{dataset_path}')
2. Analyze the data based on the user's question
3. Create appropriate visualizations using matplotlib or seaborn
4. Use plt.tight_layout() and plt.savefig() to save plots

IMPORTANT:
- USE ONLY the columns listed above. Do not invent column names.
- Write complete, executable Python code
- Always import: pandas, matplotlib.pyplot, seaborn, numpy
- Use matplotlib (not plotly) for all charts
- SAFETY: Check `if not result.empty:` before plotting/indexing! Print "No data found" if empty.
- DATA CLEANING:
  - Cast columns to string before `.str` ops: `df['c']=df['c'].astype(str)`.
  - Clean Lists: `df['c']=df['c'].str.replace(r'[\[\]"\'\']','',regex=True).str.split(',').explode()`
  - Filter: Remove 'nan', empty, len<2.
- OUTPUT RULES:
  - **DEFAULT:** Generate Table (`results_df`) or PRINT(). **NO CHARTS** unless asked.
  - If user wants Chart: `sns.set_theme(style="whitegrid")`, `plt.figure(figsize=(10,6))`. Concise inputs.
  - If answer is a TABLE:
    - Create a pandas DataFrame named 'results_df'
    - Limit to top 15 rows
    - Round numeric columns to 2 decimal places

Provide ONLY the Python code wrapped in ```python code blocks.
If you create a plot, save it as 'plot.png'.
If you create a table, ensure it is in a variable named 'results_df'.
"""

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=st.session_state.openrouter_api_key
        )

        # Retry logic for 402 Errors (Low Balance)
        token_attempts = [2000, 500, 200]
        llm_response = None # Initialize llm_response outside the loop

        for i, token_limit in enumerate(token_attempts):
            try:
                with st.spinner(f'Generating analysis (Attempt {i+1} with {token_limit} tokens)...'):
                    response = client.chat.completions.create(
                        model=st.session_state.model_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        temperature=0.2, 
                        max_tokens=token_limit, 
                    )
                    # If successful, break format loop
                    llm_response = response.choices[0].message.content
                    break
            except Exception as e:
                error_msg = str(e)
                # ERROR HANDLING MATRIX
                # 1. Credit Limit (402) -> Lower Tokens
                if "402" in error_msg and i < len(token_attempts) - 1:
                    st.warning(f"⚠️ Credit limit reached for {token_limit} tokens. Retrying with lower limit...")
                    continue 
                
                # 2. Rate Limit (429) or Service Unavailable (5xx) -> Switch Model
                elif ("429" in error_msg or "50" in error_msg) and st.session_state.model_name != "google/gemini-2.0-flash-exp:free":
                    st.warning(f"⚠️ Model {st.session_state.model_name} is busy (Rate Limit). Switching to Gemini 2.0 Flash (Free)...")
                    st.session_state.model_name = "google/gemini-2.0-flash-exp:free"
                    # Retry with the SAME token limit (restart logic would be better, but continue works if we interpret 'i' carefully)
                    # Actually, if we switch model, we should retry immediately. 
                    # Simpler hack: specific retry block logic here is messy. 
                    # Let's just switch and allow the loop to continue (it will retry with next token limit, which is fine)
                    continue
                
                else:
                    raise e # Re-raise other errors

        if llm_response is None:
            st.error("Failed to generate LLM response after multiple attempts.")
            return None, "Failed to generate LLM response."

        with st.expander("🔍 View Generated Code", expanded=False):
            st.code(llm_response, language="python")

        python_code = extract_python_code(llm_response)
        code_results = code_interpret(e2b_code_interpreter, python_code)
        return code_results, llm_response

    except Exception as error:
        st.error(f"Error communicating with OpenRouter: {error}")
        return None, str(error)

def upload_dataset(code_interpreter: Sandbox, uploaded_file) -> str:
    """Upload dataset to E2B sandbox."""
    dataset_path = f"./{uploaded_file.name}"
    try:
        with st.spinner('Uploading dataset to sandbox...'):
            file_content = uploaded_file.getvalue()
            code_interpreter.files.write(dataset_path, file_content)
            st.success(f"✅ Dataset uploaded: {uploaded_file.name}")
        return dataset_path
    except Exception as error:
        st.error(f"Error during file upload: {error}")
        raise error

def display_visualization_results(code_results: List[Any]):
    """Display visualization results from code execution."""
    if not code_results:
        # If no direct results, check for plot file is handled by sandbox usually, 
        # but here we rely on returned results. 
        # If code generated a plot but didn't return it, it might be saved as file.
        st.warning("No visualization results to display.")
        return

    st.subheader("📊 Analysis Results")

    for result in code_results:
        # Handle PNG images (plots)
        if hasattr(result, 'png') and result.png:
            try:
                png_data = base64.b64decode(result.png)
                image = Image.open(BytesIO(png_data))
                st.image(image, caption="Generated Visualization", use_container_width=True)
            except Exception as e:
                st.error(f"Error displaying image: {e}")
        
        # Handle DataFrames (tables)
        elif hasattr(result, 'data') and result.data:
            # Check if it looks like a DataFrame data structure
            st.dataframe(result.data, use_container_width=True)
            
        # Handle text output (print statements)
        elif hasattr(result, 'text') and result.text:
            st.text(result.text)

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="AI Data Visualization Agent",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📊 AI Data Visualization Agent")
    st.markdown("Transform your data into insights using natural language — powered by **OpenRouter AI** ⚡")

    # Initialize session state
    for key, default in [
        ('openrouter_api_key', ''),
        ('e2b_api_key', ''),
        ('model_name', 'google/gemini-2.0-flash-exp:free'), # Default to FREE model for testing
        ('is_premium', False) # Track premium status
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    def check_premium_access():
        """Check if user has access to premium models."""
        if st.session_state.is_premium:
            return True
        
        st.warning("🔒 This model is locked for Free users.")
        
        with st.expander("💎 Upgrade to Pro to Unlock", expanded=True):
            st.markdown("""
            ### 🚀 Pro Features
            - Access to **DeepSeek R1** & **GPT-4o**
            - Faster processing speed
            - Priority support
            
            **Pricing:** ₹499 / $5 per month
            """)
            
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("🇮🇳 Pay via Razorpay", "https://razorpay.com/payment-link/placeholder", use_container_width=True)
            with c2:
                st.link_button("🌍 Pay via Stripe", "https://buy.stripe.com/placeholder", use_container_width=True)
            
            st.divider()
            access_code = st.text_input("🔑 Enter License Key", type="password")
            if st.button("Unlock Pro"):
                if access_code == "PRO-2025": # Simple mock validation
                    st.session_state.is_premium = True
                    st.success("🎉 Premium Unlocked!")
                    st.rerun()
                else:
                    st.error("Invalid license key")
        
        return False

    # Sidebar
    with st.sidebar:
        st.header("🔐 API Configuration")

        if st.session_state.is_premium:
            st.success("💎 Premium Active")

        st.session_state.openrouter_api_key = st.text_input(
            "OpenRouter API Key",
            value=st.session_state.openrouter_api_key,
            type="password",
            help="Get your key from https://openrouter.ai/keys"
        )
        st.caption("🆓 Get free access to DeepSeek & Llama at [openrouter.ai](https://openrouter.ai/keys)")

        st.session_state.e2b_api_key = st.text_input(
            "E2B API Key",
            value=st.session_state.e2b_api_key,
            type="password",
            help="Get your key from https://e2b.dev/"
        )

        st.divider()

        # Model selection with LABELS
        model_options = {
            "🦙 [FREE] Llama 3.3 70B": "meta-llama/llama-3.3-70b-instruct:free",
            "⚡ [FREE] Gemini Flash 2.0": "google/gemini-2.0-flash-exp:free",
            "� [FREE] GPT-4o": "openai/gpt-4o",
            "� [PREMIUM] DeepSeek R1": "deepseek/deepseek-r1",
            "🎭 [PREMIUM] Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
        }

        selected_label = st.selectbox(
            "🤖 Select Model",
            options=list(model_options.keys()),
            help="Items marked [PREMIUM] require a Pro license."
        )
        
        # Check access before setting model
        if "[PREMIUM]" in selected_label:
            if check_premium_access():
                st.session_state.model_name = model_options[selected_label]
            else:
                # Revert to default if access denied (optional, or just keep locked state)
                st.session_state.model_name = None # Disable execution
        else:
            st.session_state.model_name = model_options[selected_label]

        st.divider()
        st.markdown("""
        ### 📖 How to Use:
        1. Enter your API keys above
        2. Upload a CSV dataset
        3. Ask a question about your data
        4. Click **Analyze** to get charts!

        ### 📊 Chart Types:
        - Bar, Line, Scatter
        - Pie, Histogram
        - Heatmap, Box Plot
        - And more!
        """)

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📁 Upload Dataset")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type="csv",
            help="Upload your dataset in CSV format"
        )

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            with col2:
                st.subheader("📋 Dataset Info")
                st.metric("Rows", df.shape[0])
                st.metric("Columns", df.shape[1])

            st.divider()

            st.subheader("👀 Data Preview")
            show_full = st.checkbox("Show full dataset", value=False)
            st.dataframe(df if show_full else df.head(10), use_container_width=True)

            with st.expander("📐 Column Information"):
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.values,
                    'Non-Null': df.count().values,
                    'Nulls': df.isnull().sum().values
                })
                st.dataframe(col_info, use_container_width=True)

            st.divider()
            st.subheader("💬 Ask About Your Data")

            example_queries = [
                "Show me the distribution of values in the first numeric column",
                "Create a bar chart comparing categories",
                "Show correlation between numeric columns as a heatmap",
                "What are the top 10 values by frequency?",
                "Create a scatter plot of the two main numeric columns",
            ]

            selected_example = st.selectbox(
                "Choose an example query or type your own below:",
                ["Custom query..."] + example_queries
            )

            default_query = "" if selected_example == "Custom query..." else selected_example

            query = st.text_area(
                "Your question:",
                value=default_query,
                height=100,
                placeholder="E.g., Show me average sales by category as a bar chart"
            )

            if st.button("🚀 Analyze", type="primary", use_container_width=True):
                if not st.session_state.openrouter_api_key:
                    st.error("⚠️ Please enter your OpenRouter API key in the sidebar")
                elif not st.session_state.e2b_api_key:
                    st.error("⚠️ Please enter your E2B API key in the sidebar")
                elif not query:
                    st.error("⚠️ Please enter a question about your data")
                else:
                    code_interpreter = None
                    try:
                        with st.spinner('🔧 Initializing secure sandbox...'):
                            os.environ['E2B_API_KEY'] = st.session_state.e2b_api_key
                            code_interpreter = Sandbox.create()

                        uploaded_file.seek(0)
                        dataset_path = upload_dataset(code_interpreter, uploaded_file)

                        code_results, llm_response = chat_with_llm(
                            code_interpreter,
                            query,
                            dataset_path,
                            df
                        )

                        if code_results:
                            st.success("✅ Analysis complete!")
                            display_visualization_results(code_results)
                        else:
                            st.warning("No visualization generated. Try rephrasing your query.")

                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        st.info("Please check your API keys and try again.")
                    finally:
                        if code_interpreter is not None:
                            try:
                                code_interpreter.kill()
                            except Exception:
                                pass

        except Exception as e:
            st.error(f"Error loading dataset: {e}")

    else:
        st.info("👆 Please upload a CSV file to get started")
        st.markdown("""
        **Don't have a dataset?** Use the included `sample_data.csv` to try it out!
        """)

    st.divider()
    st.markdown(
        "<div style='text-align:center;color:gray;'>Built with ❤️ using Streamlit · OpenRouter AI · E2B Code Interpreter</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
