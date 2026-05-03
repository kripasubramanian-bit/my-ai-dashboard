import streamlit as st
st.set_page_config(layout="wide")
import openai

st.title("🤖 AI Comparison Machine")

# Get the key from the "Safe"
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    st.error("The Safe is empty! Go to Streamlit Settings > Secrets and add your key.")
    st.stop()

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

user_query = st.text_input("Ask a question:", placeholder="e.g. What is 1+1?")

if st.button("Compare Now"):
    if user_query:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("Llama 3.1")
            try:
                res = client.chat.completions.create(
                    model="meta-llama/llama-3.1-8b-instruct:free",
                    messages=[{"role": "user", "content": user_query}]
                )
                st.write(res.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

        with col2:
            st.subheader("Gemini 2.0")
            try:
                # Using the specific name that worked for you!
                res = client.chat.completions.create(
                    model="google/gemini-2.0-flash-001",
                    messages=[{"role": "user", "content": user_query}]
                )
                st.write(res.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

        with col3:
            st.subheader("Mistral")
            try:
                res = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct:free",
                    messages=[{"role": "user", "content": user_query}]
                )
                st.write(res.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

        with col4:
            st.subheader("OpenChat")
            try:
                res = client.chat.completions.create(
                    model="openchat/openchat-7b:free",
                    messages=[{"role": "user", "content": user_query}]
                )
                st.write(res.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
