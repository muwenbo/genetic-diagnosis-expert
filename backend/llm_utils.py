from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os
from langchain.callbacks import StreamingStdOutCallbackHandler
#from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

def get_llm(llm_alias):
    """Initialize LLM based on model name."""
    if llm_alias == "chatgpt":
        llm_name = "gpt-4o-mini"
        return ChatOpenAI(
            temperature=0.0,
            model=llm_name,
            streaming=True
        )
    elif llm_alias == "claude":
        llm_name = "claude-3-5-sonnet-20241022"
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            temperature=0.0,
            model=llm_name,
            streaming=True
        )
    elif llm_alias == "doubao":
        llm_name = "ep-20240821102124-nl9ck"
        return ChatOpenAI(temperature = 0.0, 
            model=llm_name,
            openai_api_key=os.environ["ARK_API_KEY"],
            openai_api_base="https://ark.cn-beijing.volces.com/api/v3")
    elif llm_alias == "kimi":
        llm_name = "ep-20241203161719-mpv8s"
        return ChatOpenAI(temperature = 0.0, 
            model=llm_name,
            openai_api_key=os.environ["ARK_API_KEY"],
            openai_api_base="https://ark.cn-beijing.volces.com/api/v3")
    else:
        raise ValueError(f"Unsupported LLM: {llm_alias}")

def hello_world(llm_alias, prompt):
    from IPython.display import display, Markdown
    
    # Initialize LLM
    llm = get_llm(llm_alias)
    
    # Generate response with streaming
    response = llm.invoke(
        prompt,
        config={'callbacks': [StreamingStdOutCallbackHandler()]}
    )
    
    # Display final response as Markdown
    display(Markdown(response.content))
    return response


def generate_gene_description(llm_alias, prompt_template, phenotype, molecular_genetics):
    """Generate description using specified LLM with streaming response."""

    # Initialize LLM
    llm = get_llm(llm_alias)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Create chain with streaming
    chain = prompt | llm | StrOutputParser()
    
    # Generate response with streaming
    response = chain.invoke(
        {
            'phenotype': phenotype,
            'molecular_genetics': molecular_genetics
        },
        config={'callbacks': [StreamingStdOutCallbackHandler()]}
    )
    
    return response

def generate_acmg_intepretation(llm_alias, prompt_template, article_content, variant_name):
    """Generate description using specified LLM with streaming response."""
 
    # Initialize LLM
    llm = get_llm(llm_alias)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Create chain with streaming
    chain = prompt | llm | StrOutputParser()
    
    # Generate response with streaming
    response = chain.invoke(
        {
            'pubmed_article': article_content,
            'genetic_variant': variant_name
        },
        config={'callbacks': [StreamingStdOutCallbackHandler()]}
    )
    
    return response

def generate_acmg_classification(llm_alias, prompt_template, annotation_data, variant_name):
    """Generate ACMG interpretation using specified LLM with streaming response."""
 
    # Initialize LLM
    llm = get_llm(llm_alias)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Create chain with streaming
    chain = prompt | llm | StrOutputParser()
    import streamlit as st
    streaming_container = st.empty()
    # Generate response with streaming
    response = chain.invoke(
        {
            'annotation': annotation_data, 
            'genetic_variant': variant_name
        },
        config={'callbacks': [StreamlitCallbackHandler(streaming_container)]}
    )
    
    return response


def generate_pvs1_justification(llm_alias, prompt_template, variant_annotation, gene_annotation, transcript_annotation):
    """Generate ACMG interpretation using specified LLM with streaming response."""
 
    # Initialize LLM
    llm = get_llm(llm_alias)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Create chain with streaming
    chain = prompt | llm | StrOutputParser()
    import streamlit as st
    streaming_container = st.empty()
    # Generate response with streaming
    response = chain.invoke(
        {
            'variant_annotation': variant_annotation, 
            'gene_annotation': gene_annotation,
            'transcript_annotation': transcript_annotation,
        },
        config={'callbacks': [StreamlitCallbackHandler(streaming_container)]}
    )
    
    return response


# Example usage:
# response = generate_description(
#     llm_name="gpt-4o-mini",
#     prompt_template=template,
#     phenotype=phenotype_markdown_table,
#     molecular_genetics=molecular_genetics
# )
