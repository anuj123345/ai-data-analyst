# 🛑 Mistakes Log & Lessons Learned

This file documents the mistakes made during development to prevent repeating them. Review this file before every major task.

## 1. 🔑 API Key Handling
- **Mistake:** Assumed user input API keys were valid based on string presence alone.
- **Lesson:** API keys have specific formats (e.g., `sk-` or `key-`). Always validate key format/length before attempting to use it. Masked keys from dashboards are often incomplete.
- **Action:** Check key format. If key contains `...` or is too short, warn user immediately.

## 2. 🧠 LLM Hallucinations (Column Names)
- **Mistake:** LLM guessed column names (e.g., `'category'`) when they didn't exist in the CSV, causing `KeyError`.
- **Lesson:** LLMs do not know the dataset schema unless explicitly provided.
- **Action:** **ALWAYS** inject `df.columns` and `df.dtypes` into the system prompt so the LLM knows the exact schema.

## 3. 📉 Visualization Clutter
- **Mistake:** Generated charts with overlapping, unreadable x-axis labels for text-heavy data.
- **Lesson:** Standard bar charts fail with many categories or long labels.
- **Action:**
  - Enforce **Horizontal Bar Charts** (`plt.barh`) for categorical data.
  - **Truncate labels** to 30 chars.
  - Limit results to **Top 10-20 items**.

## 4. 💻 Code Deletion Accidents
- **Mistake:** Accidentally removed the `upload_dataset` function when updating the file to fix another function (`code_interpret`).
- **Lesson:** When replacing code blocks, ensure **ALL** dependencies and adjacent functions are preserved.
- **Action:** Double-check the `StartLine` and `EndLine` logic or use `replace_file_content` with extreme caution on large blocks.
- **Update:** I repeated this mistake by deleting `chat_with_llm` and `extract_python_code`.
- **New Rule:** NEVER use `replace_file_content` to replace a huge chunk of code (like lines 30-100) if I am not 100% sure what is in between. Use `view_file` permissions aggressively before editing.

## 6. 🔄 Incomplete Refactoring
- **Mistake:** Renamed `groq_api_key` to `openrouter_api_key` in initialization but missed the usage in the `Analyze` button check.
- **Lesson:** When renaming a core variable, I must `grep` the ENTIRE file to ensuring NO references remain.
- **Action:** Always run `grep` for the old variable name after a refactor.

## 8. ☁️ Model Availability (OpenRouter)
- **Mistake:** Hardcoded `deepseek/deepseek-r1:free` which returned 404 (endpoint not found/unavailable).
- **Lesson:** Free model endpoints on aggregators like OpenRouter can be transient.
- **Action:** Offer standard (paid) models as primary options, or verify free model availability. Don't rely 100% on `:free` suffixes staying valid forever.

## 9. 💰 Token Limits (OpenRouter 402)
- **Mistake:** Did not set `max_tokens`, causing the API to reserve the full model context (e.g., 8192 tokens), exceeding user's free credit.
- **Lesson:** Always set a reasonable `max_tokens` (e.g., 1000-2000) for code generation to avoid reserving expensive buffers.
- **Action:** Set `max_tokens=1500` in `client.chat.completions.create`.

## 10. 💳 OpenRouter Spend Limits (402)
- **Mistake:** User encountered "API key USD spend limit exceeded" error.
- **Cause:** User's OpenRouter key has a configured limit (e.g., $0) that blocks even "free" requests if they route through certain providers.
- **Action:** Advise user to check [OpenRouter Key Settings](https://openrouter.ai/keys) to remove/increase limit. Suggest `google/gemini-2.0-flash-exp:free` as a fallback.

## 11. 🧠 Pricing Hallucination (Premium Models)
- **Mistake:** Implied or stated that `gpt-4o` or similar premium models could be accessed for free or with minimal "free tier" credits in contexts where they cannot.
- **Lesson:** GPT-4o, Claude 3.5 Sonnet, and large DeepSeek models are ALWAYS paid on commercial providers (OpenRouter/OpenAI). They do not have a reliable "free tier" like Llama 3 or Gemini Flash.
- **Action:** Always explicitly label these as `[PREMIUM]` or `[PAID]` in UI and documentation.

## 12. 🧹 Data Cleaning (Date Parsing)
- **Mistake:** Assumed date columns contained valid date strings, leading to `DateParseError` on messy data (e.g., job descriptions in date columns).
- **Lesson:** Real-world data is dirty. LLM-generated code must be defensive.
- **Action:** Added system prompt rule: "When converting dates, ALWAYS use: `pd.to_datetime(df['col'], errors='coerce')`".

## 13. 📚 Library Hallucination (Seaborn Attributes)
- **Mistake:** Prompted LLM to use `sns` style but `plt.barh` logic, leading it to invent `sns.barh` (which doesn't exist).
- **Lesson:** Be precise with library-specific methods in prompts.
- **Action:** Explicitly instructed: "ALWAYS use HORIZONTAL bars: `sns.barplot(x=..., y=..., orient='h')`".

## 14. 🧹 Data Cleaning (Categorical Lists)
- **Mistake:** Treated comma-separated strings (e.g., "Mumbai, Pune") as single categories, leading to messy/confusing charts.
- **Lesson:** Categorical data often needs "exploding".
- **Action:** Added system prompt rule: "If text column has comma-separated values, SPLIT and EXPLODE it before counting frequencies".

## 15. 💰 Token Limits (Safety Margins)
- **Mistake:** Hardcoded `max_tokens=1500` was slightly too high for users with low balances (e.g., 1492 credits), causing 402 blocking errors.
- **Lesson:** Always leave a safety margin.
- **Action:** Lowered `max_tokens` to 1000 to ensure success even with minimal credits.

## 16. 🛡️ Defensive Coding (Empty DataFrames)
- **Mistake:** Generated code accessed `df.iloc[0]` without checking if `df` was empty, leading to `IndexError` on filtered results.
- **Lesson:** Zero results are a common edge case.
- **Action:** Added system prompt rule: "ALWAYS check `if not result.empty:` before accessing elements".

## 17. 🛡️ Defensive Coding (String Types)
- **Mistake:** Applied `.str` accessor to a column that contained non-string values (e.g., NaNs or numbers after explode), causing `AttributeError`.
- **Lesson:** Mixed types break string methods.
- **Action:** Added prompt rule: "Before using `.str` accessor, CAST to string: `df['col'] = df['col'].astype(str)`".

## 18. 🧹 Data Cleaning (List Parsing)
- **Mistake:** Failed to extract skills because standard split/explode didn't handle brackets/quotes or non-standard formats, resulting in empty data.
- **Lesson:** "Lists" in CSVs are widely variable strings. Be aggressive in cleaning.
- **Action:** Added rule: "Remove brackets/quotes -> Split by comma -> Explode -> Filter garbage".

## 19. 📉 Over-Visualization
- **Mistake:** Forced charts for every query, even when the user wanted a simple list or count, wasting tokens and annoying the user.
- **Lesson:** Analysts start with data (tables), then visualize.
- **Action:** Changed policy: "DEFAULT = TABLE. Chart ONLY if explicitly requested."

## 20. 💰 Chasing the Bottom (Credit Limits)
- **Mistake:** Lowered `max_tokens` iteratively (1500->1000->750) as balance dropped, instead of setting a strict minimum immediately.
- **Lesson:** If user hits a 402 error, assume critical low balance and switch to "Low Power Mode" (300 tokens) instantly.
- **Action:** Set `max_tokens` to 300 (Emergency) to allow final queries.

## 21. 📉 Token Exhaustion (Code Truncation)
- **Mistake:** Strict limit (300 tokens) caused valid Python code to be cut off (`SyntaxError`).
- **Lesson:** Code generation needs a minimum viable buffer (~400-500 tokens).
- **Action:** Compressed System Prompt to save input tokens, allowing `max_tokens` to be raised to 400.

## 22. 📉 Survival Mode (300 Tokens)
- **Mistake:** Even 400 tokens failed as user credits dropped further (to 378).
- **Lesson:** When near zero, stop optimizing. Cut to the bone (300) and FORCE a model switch.
- **Action:** Reverted to 300 tokens. Advising user to use Gemini Flash 2.0 (Free).

## 7. 🏗️ E2B Version Compatibility
- **Mistake:** Used `CodeInterpreter` class which was deprecated/changed in version 2.x, then reverted to `Sandbox`.
- **Lesson:** Library versions change rapidly.
- **Action:** Verify installed library version and check documentation/release notes before writing code for external SDKs.

## 6. 📊 Table Formatting
- **Mistake:** Displaying raw dataframes or text tables is unprofessional.
- **Lesson:** Users expect polished, interactive tables.
- **Action:** Use `st.dataframe` with interactive features. Instruct LLM to return structured data (`results_df`) instead of just printing text.
