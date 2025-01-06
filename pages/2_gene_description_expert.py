import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

from backend.omim_utils import query_omim, omim_xml_extract, omim_xml_to_phenotype_map, list_of_dicts_to_markdown_table
from backend.prompts import GENE_EXPLAINATION_TEMPLATE
from backend.llm_utils import generate_gene_description

root_path = Path(__file__).resolve().parent.parent
load_dotenv(root_path / '.env')

def main():
    st.set_page_config(page_title="Gene Description Expert", page_icon="📈")
    st.title("Gene Description Expert 📈")
    st.write("Enter a Gene OMIM ID to extract information")

    gene_omim_id = st.text_input(label = "Gene OMIM id, e.g. 138140")
    model_alias = st.selectbox(
        "Select LLM Model:",
        ["claude", "chatgpt", "kimi", "doubao"], placeholder="choose a LLM model"
    )

    if st.button("Submit"):
        with st.spinner("Extracting article content..."):
            mg = query_omim(gene_omim_id, "text:molecularGenetics")
            molecular_genetics = omim_xml_extract(mg, "textSectionContent")
            if molecular_genetics is None:
                st.error("No molecular genetics section is found for f{gene_omim_id}, please try a different OMIM ID.")
                st.stop()
            gene_map_raw = query_omim(gene_omim_id, "geneMap")
            phenotype_maps = omim_xml_to_phenotype_map(gene_map_raw)
            phenotype_markdown_table = list_of_dicts_to_markdown_table(phenotype_maps)
        
        with st.spinner("Interact with AI..."):
            gene_description = generate_gene_description(
                model_alias, 
                GENE_EXPLAINATION_TEMPLATE,
                phenotype_markdown_table,
                molecular_genetics
                )

        with st.expander("Extracted OMIM information", expanded=False):
            st.write(molecular_genetics)
            import pandas as pd
            st.write(pd.DataFrame(phenotype_maps).reset_index(drop=True))

        with st.expander("Gene Description by AI", expanded=True):
            if gene_description:
                st.write(f"{gene_description}")

if __name__ == "__main__":
    main()