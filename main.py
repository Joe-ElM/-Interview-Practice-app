import streamlit as st
from   openai_client import get_completion
import prompts  # this will provide the system messages based on selected strategy
import guards   # for input validation

st.set_page_config(page_title="Interview Practice App", layout="centered")

# --- UI ---
st.title("Interview Practice App")
st.subheader("Practice interview questions with AI")

user_input = st.text_area("Enter your topic, question, or job role:")

with st.sidebar:
    st.header("Customize AI Behavior")
    prompt_style = st.selectbox("Select Prompt Style", [
        "Zero-shot", "Few-shot", "Chain-of-thought"
    ])
    difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
    response_style = st.selectbox("Response Detail Level", ["Concise", "Detailed"])
    temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.5, step=0.2)

# --- Prompt Style Mapping ---
prompt_map = {
    "Zero-shot": prompts.get_zero_shot_prompt,
    "Few-shot": prompts.get_few_shot_prompt,
    "Chain-of-thought": prompts.get_chain_of_thought_prompt,
}

if st.button("Generate Interview Question"):

    if not guards.validate_input(user_input):
        st.warning("Invalid input. Please enter something meaningful.")
        st.stop()

    # Base system prompt from selected style
    system_prompt = prompt_map.get(prompt_style, lambda: "You are an interview coach.")()

    # Enhance system prompt with difficulty and response style
    system_prompt += f" Generate a {difficulty.lower()} interview question. Respond with a {response_style.lower()} answer."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    response = get_completion(
        messages=messages,
        temperature=temperature,
        model="gpt-4o-mini"
    )

    st.markdown("### AI-Generated Interview Response")
    st.write(response)
