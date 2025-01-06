import streamlit as st
import requests
import json
from dotenv import load_dotenv
from pathlib import Path

from backend.llm_utils import generate_acmg_classification
from backend.prompts import ACMG_CLASSIFIER_TEMPLATE, ACMG_CLASSIFIER_COMPLETE_TEMPLATE

root_path = Path(__file__).resolve().parent.parent
load_dotenv(root_path / '.env')

def get_variant_annotation(genome_version, position):
    """Query the annotation API."""
    url = "http://localhost:5001/annotate"
    payload = {
        "genome_version": genome_version,
        "position": position
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return json.loads(response.json()["result"])
    except requests.exceptions.RequestException as e:
        st.error(f"Error querying annotation API: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Variant Classification Expert", page_icon="🤖")
    st.title("Variant Classification Expert")
    st.write("Enter variant information for ACMG classification")

    genome_version = st.selectbox(
        "Reference Genome Version:",
        ["hg19", "hg38"]
    )
    
    variant_position = st.text_input(
        label="Genomic Position (format: chr-bp-ref-alt), e.g. chr2-31754395-C-T",
    )

    model_alias = st.selectbox(
        "Select LLM Model:",
        ["claude", "chatgpt", "kimi", "doubao"], 
        placeholder="choose a LLM model"
    )

    prompt_type = st.selectbox(
        "Select Prompt Template:",
        ["Ben", "Kavin"], 
        placeholder="choose an agent"
    )

    if st.button("Submit"):
        with st.spinner("Retrieving variant annotation..."):
            annotation_data = get_variant_annotation(genome_version, variant_position)
            if annotation_data is None:
                st.error("Failed to retrieve variant annotation.")
                st.stop()

        with st.expander("Variant Annotation", expanded=False):
            st.json(annotation_data)

        with st.spinner("Analyzing with AI..."):
            if prompt_type == "Ben":
                acmg_interpretation = generate_acmg_classification(
                    model_alias,
                    ACMG_CLASSIFIER_TEMPLATE,
                    json.dumps(annotation_data, indent=2),
                    variant_position
                )
            elif prompt_type == "Kavin":
                acmg_interpretation = generate_acmg_classification(
                    model_alias,
                    ACMG_CLASSIFIER_COMPLETE_TEMPLATE,
                    json.dumps(annotation_data, indent=2),
                    variant_position
                )

        with st.expander("ACMG Classification by AI", expanded=True):
            st.markdown("### Final Classification")
            st.markdown(acmg_interpretation)
        #    if acmg_interpretation:
        #        st.write(acmg_interpretation)

if __name__ == "__main__":
    main()