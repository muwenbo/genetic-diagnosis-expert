import streamlit as st

st.set_page_config(
    page_title="AI for Genetic Analysis",
    page_icon="👋",
    layout="wide"
)

st.title("Welcome to Genetic Analysis AI !👋")
with st.sidebar:
    st.sidebar.success("Select an AI agent above.")
    st.write("""
    **AI Specifications**:
    - chatgpt: gpt-4o-mini
    - claude: claude-3-5-sonnet-20241022
    - kimi: moonshot-v1-128k
    - doubao: doubao-pro-32k
""")

st.markdown("""
This is a AI assistant for Genetic Analysis
           
### Features:
- 📊 Paper Reader
- 📈 Gene Description Expert
- 🤖 Variant Classification Expert

Navigate through the pages using the sidebar on the left!
""")
