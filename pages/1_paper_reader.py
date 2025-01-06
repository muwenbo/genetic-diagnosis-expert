import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional, Dict
from backend.publication_extractor import PubMedExtractor
from backend.llm_utils import generate_acmg_intepretation
from backend.prompts import PUBMED_ACMG_READER_TEMPLATE, TEST_TEMPLATE
import xml.etree.ElementTree as ET

# Add these lines at the top after imports
# Load .env from project root
root_path = Path(__file__).resolve().parent.parent
load_dotenv(root_path / '.env')

def extract_article(url: str) -> Optional[Dict]:
    """
    Placeholder for your article extraction function.
    Replace this with your actual implementation.
    """
    extractor = PubMedExtractor()
    article_data = extractor.get_article_content_plain_text(url)
    return article_data
    

def main():
    st.set_page_config(page_title="Paper Reader", page_icon="📊")
    st.title("Paper Reader for ACMG Intepretation 📊")
    st.write("Enter a URL to extract article content. Support PMC full article only.")
    
    # URL input
    url = st.text_input(label = "Article URL, e.g. https://pmc.ncbi.nlm.nih.gov/articles/PMC5938503/")
    variant_name = st.text_input(label = "Variant Information, e.g. CYP27A1 c.410G>A")
    model_alias = st.selectbox(
        "Select LLM Model:",
        ["claude", "chatgpt", "kimi", "doubao"], placeholder="choose a LLM model"
    )

    if st.button("Submit"):
        # Show spinner while processing
        with st.spinner("Extracting article content..."):
            article_content = extract_article(url)
            
        with st.spinner("Interact with AI..."):
            intepretation = generate_acmg_intepretation(
                model_alias, 
                PUBMED_ACMG_READER_TEMPLATE, 
                article_content,
                #TEST_TEMPLATE,
                #article_content[:500],
                variant_name
                )

        # Display article content in an expandable container
        with st.expander("Extracted Content", expanded=True):
            st.write(f"{intepretation}")
                

if __name__ == "__main__":
    main()