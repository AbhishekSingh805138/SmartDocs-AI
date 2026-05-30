import streamlit as st
import requests


def render_chat_window(api_url: str = "http://localhost:8080"):
    """Render the chat interface with message history and input."""
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("Sources"):
                    for src in msg["sources"]:
                        st.markdown(f"- {src}")

    # Handle new input
    if prompt := st.chat_input("Ask a question about your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(
                        f"{api_url}/api/v1/chat",
                        json={"question": prompt, "top_k": 5},
                        timeout=60,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        st.markdown(data["answer"])
                        sources = data.get("sources", [])
                        if sources:
                            with st.expander(f"Sources ({data['chunks_used']} chunks)"):
                                for src in sources:
                                    st.markdown(f"- {src}")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": data["answer"],
                            "sources": sources,
                        })
                    else:
                        error = resp.json().get("detail", "Unknown error")
                        st.error(error)
                except requests.exceptions.ConnectionError:
                    st.error("Backend is offline. Start the FastAPI server first.")
                except Exception as e:
                    st.error(f"Error: {e}")
