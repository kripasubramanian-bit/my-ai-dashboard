import streamlit as st
import pandas as pd
import asyncio
from openai import AsyncOpenAI

# This connects to your secret key (stored in Streamlit, not GitHub)
client = AsyncOpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"], 
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(layout="wide", page_title="AI Comparison Machine")

# These are the "FREE" models so you never get a bill
MODELS = {
    "Llama 3 (Free)": "meta-llama/llama-3-8b-instruct:free",
    "Gemini 1.5 (Free)": "google/gemini-flash-1.5-8b:free",
    "Mistral (Free)": "mistralai/mistral-7b-instruct:free",
    "Qwen 2 (Free)": "qwen/qwen-2-7b-instruct:free"
}

st.title("🤖 My AI Comparison Machine")
st.write("Type a question below to see how different AIs answer at the same time!")

user_prompt = st.text_input("Ask a question:", placeholder="e.g. Why is the sky blue?")

async def get_answer(name, model_id, prompt):
    try:
        resp = await client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}]
        )
        text = resp.choices[0].message.content
        return {"Model": name, "Response": text}
    except:
        return {"Model": name, "Response": "⚠️ Error: Make sure your API Key is correct in Streamlit Secrets!"}

if st.button("Compare Now"):
    if not user_prompt:
        st.error("Please type a question first!")
    else:
        with st.spinner("Asking the AIs..."):
            async def run_all():
                tasks = [get_answer(n, mid, user_prompt) for n, mid in MODELS.items()]
                return await asyncio.gather(*tasks)
            
            results = asyncio.run(run_all())
            
            # This creates the side-by-side columns
            cols = st.columns(len(results))
            for i, res in enumerate(results):
                with cols[i]:
                    st.subheader(res["Model"])
                    st.info(res["Response"])
