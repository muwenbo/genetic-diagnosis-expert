# Auto Report LLM

A multi page streamlit application that uses LLM models to solve medical genetic diagnosis problems. The goal is to have an agent can classify germline variant and achieve a reasoneable accuracy.

## Features

### 🌐 Paper Reader
- Query genes using OMIM MIM numbers and generate formatied 

### 



- Select from multiple LLM models for description generation
- View generated descriptions, phenotype tables, and molecular genetics data
- Interactive and user-friendly interface


## Installation

### Prerequisites
- Python 3.9+
- OMIM API key
- ARK API key (for LLM access)
- ANTHROPIC API key (for LLM access)
- OPENAI API key (for LLM access)

### Setup

1. Clone the repository
```bash
git clone https://github.com/muwenbo/auto-report-llm
cd auto_report_llm
```

2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

## Usage

### Running the Streamlit Web Interface
```bash
streamlit run home.py
```
Access at: http://localhost:8501

## Available LLM Models

- chatgpt: gpt-4o-mini
- claude: claude-3-5-sonnet-20241022
- kimi: moonshot-v1-128k
- doubao: doubao-pro-32k

## License
This project is licensed under the MIT License
