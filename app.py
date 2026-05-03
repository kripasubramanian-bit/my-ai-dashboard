import streamlit as st
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
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Llama 3")
            try:
                res1 = client.chat.completions.create(
                    model="meta-llama/llama-3-8b-instruct:free",
                    messages=[{"role": "user", "content": user_query}]
                )
                st.write(res1.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

        with col2:
            st.subheader("Gemini 1.5")
            try:
                res2 = client.chat.completions.create(
                    model="google/gemini-flash-1.5-8b:free",
                    messages=[{"role": "user", "content": user_query}]
                )
                st.write(res2.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
