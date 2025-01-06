# Genetics Diagnosis Expert

A multi-page Streamlit application that uses LLM models to assist with medical genetic diagnosis. The goal is to develop an agent that can classify germline variants with reasonable accuracy.

## Features

### Paper Reader
Supports extraction and analysis of full-text articles from PMC (PubMed Central) according to ACMG requirements. Conclusions of **de_novo_occurrence**, **functional_studies**, **prevalence_and_observation**, **cosegregation**, **phenotype_specificity**, **trans_cis_occurrence**, **alternative_molecular_basis** are provided 

### Gene Description Expert
Query genes using OMIM MIM numbers and generate formatted description in Chinese.

### Variant Classification Expert
Variant classification expert allows users to input genomic variant information (genome version and position) and provides ACMG classification analysis . Integration with a local annotation API to fetch variant annotation data. Support for multiple LLM models (claude, chatgpt, kimi, doubao) and different prompt templates (Ben, Kavin etc.) for ACMG classification.

### PVS1 Expert
PVS1 experts is a special prompts that specifically designed to provides ACMG PVS1 analysis for a variant.

## Installation

### Prerequisites
- Python 3.9+
- OMIM API key
- ARK API key (for LLM access)
- ANTHROPIC API key (for LLM access)
- OPENAI API key (for LLM access)
- Variant Annotation API

### Setup

1. Clone the repository
```bash
git clone https://github.com/muwenbo/auto-report-llm
cd auto_report_llm
```

2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root
```env
OMIM_API_KEY=your_omim_key
ARK_API_KEY=your_ark_key
ANTHROPIC_API_KEY=your_antropic_key
OPENAI_API_KEY=your_openai_key
```

### Data Preparation
- gene_db.json: a comprehensive gene database where each entry is keyed by NCBI gene ID. For each gene, the following information is stored.
  - Basic Gene Information: Symbol, Gene_type, Cyto_location etc.
  - Clinical Information: inheritance, associated phenotypes
  - Constraint Metrics: pLI, oe_lof_upper, syn_z etc.
  - Haploinsufficiency/Triplosensitivity Information: HI_Score_ClinGen, TS_Score_ClinGen etc.

- transcript_db.json: a comprehensive transcript database is keyed by RefSeq transcript id. For each transcript, gene symbol, location, protein id, strand, NMD location, exon counts and length, CDS counts and length is stored.

## Usage

### Running the Streamlit Web Interface
```bash
streamlit run home.py
```
Access at: http://localhost:8501

## Available LLM Models
Defined in 
- chatgpt: gpt-4o-mini
- claude: claude-3-5-sonnet-20241022
- kimi: moonshot-v1-128k
- doubao: doubao-pro-32k

## License
This project is licensed under the MIT License
