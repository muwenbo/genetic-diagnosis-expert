import requests
from bs4 import BeautifulSoup
import re

class PubMedExtractor:
    def __init__(self):
        self.base_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def extract_pmcid(self, url):
        """Extract PMCID from URL."""
        match = re.search(r'PMC\d+', url)
        return match.group(0) if match else None

    def get_article_content(self, url):
        """Extract content from a PMC article."""
        pmcid = self.extract_pmcid(url)
        if not pmcid:
            return {"error": "Invalid PMC URL"}

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract article metadata
            article_data = {
                "pmcid": pmcid,
                "pmid": self._get_pmid(soup),
                "title": self._get_title(soup),
                "abstract": self._get_abstract(soup),
                "keywords": self._get_keywords(soup),
                "sections": self._get_sections(soup),
                "figures": self._get_figures(soup),
                "tables": self._get_tables(soup),
                "references": self._get_references(soup),
                "acknowledgments": self._get_acknowledgments(soup)
            }

            return article_data

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to retrieve article: {str(e)}"}

    def get_article_content_plain_text(self, url):
        content = ""
        article_data = self.get_article_content(url)
        if "error" not in article_data:
            content += "Title:"
            content += f"{article_data['title']}\n"

            content += f"PMCID: {article_data['pmcid']}\n"
            content += f"PMID: {article_data['pmid']}\n"
            
            content += "Abstract:"
            content += f"{article_data['abstract']}\n"
            
            content += "Keywords:"
            content += article_data['keywords'] + "\n"
            
            content += "Sections:"
            for section in article_data['sections']:
                content += f"\n{section['title']}:"
                content += section['content']

            content += "\nTables:"
            for table in article_data.get('tables', []):
                content += f"\nTitle: {table['title']}"
                content += f"Caption: {table['caption']}"
                content += "Markdown Table:"
                content += table['markdown']

            content += "\nFigures:"
            for figure in article_data['figures']:
                content += f"\n{figure['title']}:"
                content += f"Caption: {figure['caption']}"
            
            if article_data['acknowledgments']:
                content += "\nAcknowledgments:"
                content += article_data['acknowledgments']
            
            if article_data['references']:
                content += "\nReferences:"
                for reference in article_data['references']:
                    content += reference + "\n"

        return content

    def _get_pmid(self, soup):
        """Extract PMID."""
        pmid_link = soup.find('a', href=re.compile(r'pubmed\.ncbi\.nlm\.nih\.gov/\d+'))
        if pmid_link:
            return pmid_link.text.strip()
        return ""

    def _get_title(self, soup):
        """Extract article title."""
        #title_elem = soup.find(['h1', 'h2'], class_='content-title')
        title_elem = soup.find('hgroup')
        return title_elem.text.strip() if title_elem else ""

    def _get_abstract(self, soup):
        """Extract article abstract."""
        abstract_section = soup.find('section', class_='abstract')
        if abstract_section:
            # Remove the "Abstract" heading
            abstract_heading = abstract_section.find('h2')
            if abstract_heading:
                abstract_heading.decompose()
            return abstract_section.get_text(strip=True)
        return ""

    def _get_keywords(self, soup):
        """Extract keywords."""
        keywords_section = soup.find('section', class_='kwd-group')
        if keywords_section:
            # Remove the "Keywords:" text
            text = keywords_section.get_text(strip=True)
            return text.replace("Keywords:", "").strip()
        return ""

    def _get_sections(self, soup):
        """Extract article sections."""
        sections = []
        for section in soup.find_all('section', id=re.compile(r'^sec\d+')):
            # Create a copy of the section to modify
            section_copy = BeautifulSoup(str(section), 'html.parser')
            title = ""
            content = ""
            
            # Get section title
            heading = section_copy.find(['h2', 'h3', 'h4', 'h5'], class_='pmc_sec_title')
            if heading:
                title = heading.text.strip()
                heading.decompose()  # Remove heading from content
            
            # Clean em tags
            section_copy = self._clean_em_tags(section_copy)

            # Get section content
            paragraphs = section_copy.find_all('p')
            content = "\n".join(p.get_text(strip=True) for p in paragraphs)
            
            if title or content:
                sections.append({
                    "title": title,
                    "content": content
                })
        return sections

    def _get_tables(self, soup):
        """Extract tables and convert to Markdown format."""
        tables = []
        for table_section in soup.find_all('section', class_='tw'):
            # Get table title and caption
            title = ""
            caption = ""
            
            title_elem = table_section.find(['h3', 'h4'], class_='obj_head')
            if title_elem:
                title = title_elem.get_text(strip=True)
            
            caption_elem = table_section.find('div', class_='caption')
            if caption_elem:
                caption = caption_elem.get_text(strip=True)
            
            # Find the table
            table_elem = table_section.find('table', class_='content')
            if table_elem:
                # Convert table to Markdown
                md_table = self._table_to_markdown(table_elem)
                
                tables.append({
                    "title": title,
                    "caption": caption,
                    "markdown": md_table
                })
        
        return tables

    def _table_to_markdown(self, table_elem):
        """Convert HTML table to Markdown format."""
        rows = []
        header_row = []
        
        # Extract headers
        thead = table_elem.find('thead')
        if thead:
            header_row = [cell.get_text(strip=True) for cell in thead.find_all('td')]
        
        # Extract body rows
        tbody = table_elem.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                row = [cell.get_text(strip=True) for cell in tr.find_all('td')]
                rows.append(row)
        
        # Determine max width of each column
        col_widths = [max(len(str(cell)) for cell in column) 
                      for column in zip(header_row, *rows)]
        
        # Create Markdown table
        md_lines = []
        
        # Header row
        if header_row:
            header_line = "| " + " | ".join(
                f"{header:{width}}" for header, width in zip(header_row, col_widths)
            ) + " |"
            md_lines.append(header_line)
            
            # Separator line
            separator_line = "| " + " | ".join(
                "-" * width for width in col_widths
            ) + " |"
            md_lines.append(separator_line)
        
        # Data rows
        for row in rows:
            row_line = "| " + " | ".join(
                f"{str(cell):{width}}" for cell, width in zip(row, col_widths)
            ) + " |"
            md_lines.append(row_line)
        
        return "\n".join(md_lines)

    def _get_figures(self, soup):
        """Extract figures and their captions."""
        figures = []
        for figure in soup.find_all('figure', class_='fig'):
            fig_data = {
                "id": figure.get('id', ''),
                "title": "",
                "caption": ""
            }
            
            # Get figure title
            title = figure.find(['h3', 'h4', 'h5'], class_='obj_head')
            if title:
                fig_data["title"] = title.text.strip()
            
            # Get figure caption
            caption = figure.find('figcaption')
            if caption:
                fig_data["caption"] = caption.get_text(strip=True)
            
            figures.append(fig_data)
        return figures

    def _get_references(self, soup):
        """Extract article references."""
        references = []
        ref_list = soup.find('section', class_='ref-list')
        if ref_list:
            for ref in ref_list.find_all('li'):
                text = ' '.join(ref.get_text(strip=True).split())
                #references.append(ref.get_text(strip=True))
                references.append(text)

        return references
    
    def _clean_em_tags(self, soup):
        """
        Replace <em> tags with their text content, adding a space around the text
        to prevent word merging.
        """
        for em in soup.find_all('em'):
            em.replace_with(f" {em.get_text(strip=True)} ")
        return soup

    def _get_acknowledgments(self, soup):
        """Extract acknowledgments section."""
        ack_section = soup.find('section', class_='ack')
        heading = ack_section.find(['h2', 'h3'], class_='pmc_sec_title')
        if heading:
            heading.decompose()  # Remove heading from content
        if ack_section:
            return ack_section.get_text(strip=True)
        return ""

def main():
    extractor = PubMedExtractor()
    url = "https://pmc.ncbi.nlm.nih.gov/articles/PMC5938503/"
    article_data = extractor.get_article_content(url)
    
    # Print extracted content in a structured format
    if "error" not in article_data:
        print("Title:")
        print(article_data['title'], "\n")

        print(f"PMCID: {article_data['pmcid']}")
        print(f"PMID: {article_data['pmid']}\n")
        
        print("Abstract:")
        print(article_data['abstract'], "\n")
        
        print("Keywords:")
        print(article_data['keywords'], "\n")
        
        print("Sections:")
        for section in article_data['sections']:
            print(f"\n{section['title']}:")
            print(section['content'])

        print("\nTables:")
        for table in article_data.get('tables', []):
            print(f"\nTitle: {table['title']}")
            print(f"Caption: {table['caption']}")
            print("Markdown Table:")
            print(table['markdown'])

        print("\nFigures:")
        for figure in article_data['figures']:
            print(f"\n{figure['title']}:")
            print(f"Caption: {figure['caption']}")
        
        if article_data['acknowledgments']:
            print("\nAcknowledgments:")
            print(article_data['acknowledgments'])
        
        if article_data['references']:
            print("\nReferences:")
            for reference in article_data['references']:
                print(reference)

    else:
        print(f"Error: {article_data['error']}")

if __name__ == "__main__":
    main()