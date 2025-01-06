import os
import requests
import xml.etree.ElementTree as ET
import textwrap
from typing import Dict, List

def query_omim(mim_number: str, section_name: str) -> bytes:
    omim_api_key = os.getenv("OMIM_API_KEY")
    url = f"https://api.omim.org/api/entry?mimNumber={mim_number}&include={section_name}&apiKey={omim_api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def omim_xml_extract(data: bytes, content_title: str) -> str:
    root = ET.fromstring(data)
    text_section_content = root.find(f'.//{content_title}')
    if text_section_content is None:
        return None
    return text_section_content.text

def omim_xml_to_phenotype_map(data: bytes) -> List[Dict]:
    root = ET.fromstring(data)
    phenotype_maps = []
    for phenotype_map in root.findall('.//phenotypeMap'):
        phenotype_dict = {
            'mimNumber': phenotype_map.find('mimNumber').text,
            'phenotype': phenotype_map.find('phenotype').text,
            'phenotypeMimNumber': phenotype_map.find('phenotypeMimNumber').text,
            'phenotypeMappingKey': phenotype_map.find('phenotypeMappingKey').text,
            'phenotypeInheritance': phenotype_map.find('phenotypeInheritance').text
        }
        phenotype_maps.append(phenotype_dict)
    return phenotype_maps

def list_of_dicts_to_markdown_table(data: List[Dict]) -> str:
    if not data:
        return ""
        
    headers = data[0].keys()
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join(["-" * len(header) for header in headers]) + " |"
    
    rows = []
    for entry in data:
        row = "| " + " | ".join(str(entry[header]) for header in headers) + " |"
        rows.append(row)
    
    markdown_table = "\n".join([header_row, separator_row] + rows)
    return markdown_table
