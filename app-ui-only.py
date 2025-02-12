#
# Use this to quickly verify that deepseek works
#

import streamlit as st
import ollama
import textwrap

st.set_page_config(page_title="DeepSeek-Coder Chat", layout="wide")

st.title("DeepSeek-Coder Assistant")
st.write("Ask coding-related questions, get explanations, or generate scripts!")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            if "```" in msg["content"]:  # Detects if response contains code
                st.markdown(msg["content"])  
            else:
                st.markdown(textwrap.fill(msg["content"], width=80))  # Wrap text nicely

user_input = st.chat_input("Type your question or code prompt...")
if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ollama.chat(
                model="deepseek-coder",
                messages=st.session_state.messages
            )

            # **Correct Way** → Access the actual text field inside the Pydantic object
            if hasattr(response, "message") and hasattr(response.message, "content"):
                answer = response.message.content  # Access correct text field
            else:
                answer = str(response)  # Fallback (should rarely happen)

            # Ensure proper formatting for readability
            if "```" in answer:
                st.markdown(answer)  # Code output
            else:
                formatted_text = "\n".join(textwrap.wrap(answer, width=80))  # Wrap long text
                st.markdown(formatted_text)  # Regular text output

    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})

