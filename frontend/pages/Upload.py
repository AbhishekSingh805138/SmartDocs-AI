import streamlit as st
import requests

st.set_page_config(page_title="Upload Documents - SmartDocs AI", page_icon="📤")

API_URL = st.session_state.get("api_url", "http://localhost:8080")

st.title("Upload Documents")
st.markdown("Upload PDF files to build your knowledge base.")
st.markdown("---")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    help="Upload a PDF document (max 50MB)",
)

if uploaded_file is not None:
    st.info(f"Selected: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

    if st.button("Process Document", type="primary"):
        with st.spinner("Uploading and processing document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/api/v1/upload", files=files, timeout=120)

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Successfully processed **{data['filename']}**")
                    col1, col2 = st.columns(2)
                    col1.metric("Pages Extracted", data["pages"])
                    col2.metric("Chunks Created", data["chunks"])
                else:
                    error = response.json().get("detail", "Unknown error")
                    st.error(f"Upload failed: {error}")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the backend. Make sure the FastAPI server is running.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Show uploaded documents
st.markdown("---")
st.subheader("Uploaded Documents")

try:
    response = requests.get(f"{API_URL}/api/v1/documents", timeout=10)
    if response.status_code == 200:
        docs = response.json().get("documents", [])
        if docs:
            for doc in docs:
                st.markdown(f"- **{doc['filename']}** ({doc['size_mb']} MB)")
        else:
            st.info("No documents uploaded yet.")
    else:
        st.warning("Could not fetch document list.")
except requests.exceptions.ConnectionError:
    st.warning("Backend is not running. Start the FastAPI server to see uploaded documents.")
except Exception:
    st.warning("Could not fetch document list.")
