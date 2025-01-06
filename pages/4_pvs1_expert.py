import streamlit as st
import requests
import json
from dotenv import load_dotenv
from pathlib import Path

from backend.llm_utils import generate_pvs1_justification
from backend.prompts import PVS1_EXPERT_TEMPLATE

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

    gene_annotation_file = root_path / 'data/gene_db.json'
    transcript_annotaton_file = root_path / 'data/transcript_db.json'
    with open(gene_annotation_file, "r") as file:
        gene_db = json.load(file)
    with open(transcript_annotaton_file, "r") as file:
        transcript_db = json.load(file)

    if st.button("Submit"):
        with st.spinner("Retrieving variant annotation..."):
            annotation_data = get_variant_annotation(genome_version, variant_position)
            if annotation_data is None:
                st.error("Failed to retrieve variant annotation.")
                st.stop()

        with st.spinner("Retrieving gene annotation..."):
            gene_annotation_data = {}
            transcript_annotaton_data = {}

            for variant in annotation_data["transcript_consequences"]:
                print(variant)
                if "pick" in variant and variant["pick"] == 1:
                    if "gene_id" in variant and variant["gene_id"] in gene_db:
                        gene_annotation_data = gene_db[variant["gene_id"]]
                    if "transcript_id" in variant:
                        transcript_base = variant["transcript_id"].split(".")[0]
                        if transcript_base in transcript_db:
                            transcript_annotaton_data = transcript_db[transcript_base]

        with st.expander("Variant Annotation", expanded=False):
            st.json(annotation_data)
            st.write(gene_annotation_data)
            st.write(transcript_annotaton_data)


        with st.spinner("Analyzing with AI..."):
            acmg_interpretation = generate_pvs1_justification(
                model_alias,
                PVS1_EXPERT_TEMPLATE,
                annotation_data,
                gene_annotation_data,
                transcript_annotaton_data
            )

        with st.expander("ACMG Classification by AI", expanded=True):
            st.markdown("### Final Classification")
            st.markdown(acmg_interpretation)
        #    if acmg_interpretation:
        #        st.write(acmg_interpretation)

if __name__ == "__main__":
    main()