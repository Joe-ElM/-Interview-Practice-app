# This is the UI layer of the Interview Practice App, built with Streamlit.
# It connects the user input to the OpenAI engine cleanly and modularly.

from   openai_client import get_completion
import streamlit as st
import prompts  # this will provide the system messages based on selected strategy
import guards   # for input validation 


st.set_page_config(page_title="Interview Practice App", layout="centered")

# --- UI ---
st.title("Interview Practice App")
st.subheader("Practice interview questions with AI")
st.markdown("Choose a prompt style and enter a topic to begin.")

# --- User Inputs ---
prompt_style = st.selectbox("Select Prompt Style", 
                           ["Zero-shot", "Few-shot", "Chain-of-thought"])

user_input  = st.text_area("Enter your topic, question, or job role:")
temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.5, step=0.1)

# --- Prompt Style Mapping ---
prompt_map = {
    "Zero-shot"       : prompts.get_zero_shot_prompt,
    "Few-shot"        : prompts.get_few_shot_prompt,
    "Chain-of-thought": prompts.get_chain_of_thought_prompt,
}

if st.button("Generate Interview Question"):
    
# Validate the user input using a basic guard function.
# If the input is empty or flagged as inappropriate, show a warning and stop app execution.
    if not guards.validate_input(user_input):
        st.warning("Invalid input. Please enter something meaningful.")
        st.stop()

    system_prompt = prompt_map.get(prompt_style, lambda: "You are an interview coach.")()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user"  , "content": user_input}
    ]

    response = get_completion(
                            messages    = messages,
                            temperature = temperature,
                            model       = "gpt-4o-mini"
                           )

    st.markdown("### AI-Generated Interview Response")
    st.write(response)