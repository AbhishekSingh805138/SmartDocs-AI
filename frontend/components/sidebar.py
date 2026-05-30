import streamlit as st
import requests


def render_sidebar(api_url: str = "http://localhost:8080"):
    """Render the shared sidebar component."""
    with st.sidebar:
        st.header("SmartDocs AI")
        st.markdown("Your intelligent document assistant.")
        st.markdown("---")

        # Health check
        try:
            response = requests.get(f"{api_url}/api/v1/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                st.success(f"Status: {health['status']}")
                st.metric("Indexed Vectors", health["documents_count"])
                st.caption(f"Version: {health['version']}")
            else:
                st.error("Backend returned an error")
        except requests.exceptions.ConnectionError:
            st.error("Backend is offline")
        except Exception:
            st.warning("Could not reach backend")

        st.markdown("---")
        st.caption("Built with FastAPI, FAISS, LangChain & Streamlit")
