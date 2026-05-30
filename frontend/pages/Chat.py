import streamlit as st
import requests

st.set_page_config(page_title="Chat - SmartDocs AI", page_icon="💬")

API_URL = st.session_state.get("api_url", "http://localhost:8080")

st.title("Chat with Your Documents")
st.markdown("Ask questions and get answers from your uploaded PDFs.")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.markdown(f"- {source}")

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/v1/chat",
                    json={"question": prompt, "top_k": 5},
                    timeout=60,
                )

                if response.status_code == 200:
                    data = response.json()
                    st.markdown(data["answer"])

                    if data.get("sources"):
                        with st.expander(f"Sources ({data['chunks_used']} chunks used)"):
                            for source in data["sources"]:
                                st.markdown(f"- {source}")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["answer"],
                        "sources": data.get("sources", []),
                    })
                else:
                    error = response.json().get("detail", "Unknown error")
                    st.error(f"Error: {error}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the backend. Make sure the FastAPI server is running.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sidebar controls
with st.sidebar:
    st.header("Chat Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    # Health check
    try:
        health = requests.get(f"{API_URL}/api/v1/health", timeout=5).json()
        st.success(f"Backend: {health['status']}")
        st.metric("Indexed Vectors", health["documents_count"])
    except Exception:
        st.error("Backend is offline")
