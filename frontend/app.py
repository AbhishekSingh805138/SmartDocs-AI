import streamlit as st

st.set_page_config(
    page_title="SmartDocs AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("SmartDocs AI")
st.markdown("**RAG-powered personal assistant for PDF document Q&A**")
st.markdown("---")
st.markdown(
    """
    ### Getting Started

    1. **Upload** — Go to the **Upload Documents** page to upload your PDF files.
    2. **Chat** — Go to the **Chat** page to ask questions about your documents.

    Use the sidebar to navigate between pages.
    """
)

# Sidebar
with st.sidebar:
    st.header("SmartDocs AI")
    st.markdown("Your intelligent document assistant.")
    st.markdown("---")

    api_url = st.text_input(
        "Backend API URL",
        value="http://localhost:8080",
        help="URL of the FastAPI backend server",
    )
    st.session_state["api_url"] = api_url

    st.markdown("---")
    st.caption("Built with FastAPI, FAISS, LangChain & Streamlit")
