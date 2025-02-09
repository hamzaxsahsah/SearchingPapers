import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
import json

class ResearchDatabaseScraper:
    def __init__(self):
        self.output_dir = "research_papers"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Database configurations
        self.databases = {
            1: {
                'name': 'arXiv',
                'search_url': 'https://arxiv.org/search/advanced',
                'method': self._search_arxiv
            },
            2: {
                'name': 'IEEE Xplore',
                'search_url': 'https://ieeexplore.ieee.org/rest/search',
                'method': self._search_ieee
            },
            3: {
                'name': 'Google Scholar',
                'search_url': 'https://scholar.google.com/scholar',
                'method': self._search_google_scholar
            },
            4: {
                'name': 'Science Direct',
                'search_url': 'https://www.sciencedirect.com/search',
                'method': self._search_science_direct
            },
            5: {
                'name': 'PubMed',
                'search_url': 'https://pubmed.ncbi.nlm.nih.gov/',
                'method': self._search_pubmed
            }
        }

    def _search_arxiv(self, query, max_results):
        """Search arXiv database"""
        try:
            search_query = f"abstract:{query}+OR+title:{query}"
            params = {
                'advanced': '',
                'terms-0-operator': 'OR',
                'terms-0-term': query,
                'terms-0-field': 'title',
                'terms-1-operator': 'OR',
                'terms-1-term': query,
                'terms-1-field': 'abstract',
                'size': max_results,
                'order': '-announced_date_first'
            }
            
            response = requests.get(
                self.databases[1]['search_url'],
                params=params,
                headers=self.headers
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('li', class_='arxiv-result')
            
            papers = []
            for result in results:
                paper = {
                    'database': 'arXiv',
                    'title': result.find('p', class_='title').text.strip(),
                    'authors': result.find('p', class_='authors').text.replace('Authors:', '').strip(),
                    'abstract': result.find('span', class_='abstract-full').text.strip(),
                    'url': f"https://arxiv.org{result.find('a', href=True)['href']}",
                    'date': result.find('p', class_='is-size-7').text.split(';')[0].replace('Submitted', '').strip()
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            print(f"Error searching arXiv: {e}")
            return []

    def _search_ieee(self, query, max_results):
        """Search IEEE Xplore database using public interface"""
        try:
            encoded_query = quote(query)
            url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={encoded_query}"
            
            headers = {
                **self.headers,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all paper entries
            results = soup.find_all('div', class_='List-results-items')
            
            papers = []
            for result in results[:max_results]:
                try:
                    # Extract title and URL
                    title_elem = result.find('h2')
                    if title_elem:
                        title = title_elem.text.strip()
                        link = title_elem.find('a')
                        url = f"https://ieeexplore.ieee.org{link['href']}" if link else 'N/A'
                    else:
                        continue
                    
                    # Extract authors
                    authors_elem = result.find('p', class_='author')
                    authors = authors_elem.text.strip() if authors_elem else 'N/A'
                    
                    # Extract abstract
                    abstract_elem = result.find('div', class_='js-displayer-content')
                    abstract = abstract_elem.text.strip() if abstract_elem else 'N/A'
                    
                    # Extract date
                    date_elem = result.find('div', class_='publisher-info-container')
                    date = date_elem.text.strip() if date_elem else 'N/A'
                    
                    paper = {
                        'database': 'IEEE',
                        'title': title,
                        'authors': authors,
                        'abstract': abstract,
                        'url': url,
                        'date': date
                    }
                    papers.append(paper)
                    
                except Exception as e:
                    print(f"Error parsing IEEE result: {e}")
                    continue
            
            return papers
            
        except Exception as e:
            print(f"Error searching IEEE: {e}")
            return []


    def _search_google_scholar(self, query, max_results):
        """Search Google Scholar"""
        try:
            params = {
                'q': query,
                'hl': 'en',
                'num': max_results
            }
            
            response = requests.get(
                self.databases[3]['search_url'],
                params=params,
                headers=self.headers
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='gs_ri')
            
            papers = []
            for result in results:
                title_elem = result.find('h3', class_='gs_rt')
                authors_elem = result.find('div', class_='gs_a')
                
                paper = {
                    'database': 'Google Scholar',
                    'title': title_elem.text if title_elem else 'N/A',
                    'authors': authors_elem.text if authors_elem else 'N/A',
                    'abstract': result.find('div', class_='gs_rs').text if result.find('div', class_='gs_rs') else 'N/A',
                    'url': title_elem.find('a')['href'] if title_elem and title_elem.find('a') else 'N/A',
                    'date': 'N/A'  # Date format varies in Google Scholar
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            print(f"Error searching Google Scholar: {e}")
            return []

    def _search_science_direct(self, query, max_results):
        """Search Science Direct"""
        try:
            params = {
                'qs': query,
                'show': max_results,
                'sortBy': 'relevance'
            }
            
            response = requests.get(
                self.databases[4]['search_url'],
                params=params,
                headers=self.headers
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='result-item-content')
            
            papers = []
            for result in results:
                title_elem = result.find('h2')
                
                paper = {
                    'database': 'Science Direct',
                    'title': title_elem.text.strip() if title_elem else 'N/A',
                    'authors': result.find('div', class_='authors').text if result.find('div', class_='authors') else 'N/A',
                    'abstract': result.find('div', class_='abstract').text if result.find('div', class_='abstract') else 'N/A',
                    'url': f"https://www.sciencedirect.com{title_elem.find('a')['href']}" if title_elem and title_elem.find('a') else 'N/A',
                    'date': result.find('div', class_='publication-date').text if result.find('div', class_='publication-date') else 'N/A'
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            print(f"Error searching Science Direct: {e}")
            return []

    def _search_pubmed(self, query, max_results):
        """Search PubMed"""
        try:
            params = {
                'term': query,
                'size': max_results,
                'format': 'abstract'
            }
            
            response = requests.get(
                self.databases[5]['search_url'],
                params=params,
                headers=self.headers
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='results-article')
            
            papers = []
            for result in results:
                paper = {
                    'database': 'PubMed',
                    'title': result.find('h1', class_='heading-title').text if result.find('h1', class_='heading-title') else 'N/A',
                    'authors': result.find('div', class_='authors-list').text if result.find('div', class_='authors-list') else 'N/A',
                    'abstract': result.find('div', class_='abstract-content').text if result.find('div', class_='abstract-content') else 'N/A',
                    'url': f"https://pubmed.ncbi.nlm.nih.gov/{result['data-article-id']}" if result.get('data-article-id') else 'N/A',
                    'date': result.find('span', class_='publication-date').text if result.find('span', class_='publication-date') else 'N/A'
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            print(f"Error searching PubMed: {e}")
            return []

    def search_databases(self, query, selected_dbs, max_results=50):
        """
        Perform distributed search across selected databases
        """
        all_papers = []
        
        # Convert string of numbers to list of integers
        if isinstance(selected_dbs, str):
            selected_dbs = [int(db.strip()) for db in selected_dbs.split(',')]
        
        # Validate selected databases
        valid_dbs = [db for db in selected_dbs if db in self.databases]
        
        if not valid_dbs:
            print("No valid databases selected!")
            return []
        
        # Distribute max_results across selected databases
        results_per_db = max_results // len(valid_dbs)
        
        # Use ThreadPoolExecutor for parallel searches
        with ThreadPoolExecutor(max_workers=len(valid_dbs)) as executor:
            future_to_db = {
                executor.submit(
                    self.databases[db]['method'],
                    query,
                    results_per_db
                ): db for db in valid_dbs
            }
            
            for future in future_to_db:
                db_id = future_to_db[future]
                try:
                    papers = future.result()
                    all_papers.extend(papers)
                    print(f"Found {len(papers)} papers in {self.databases[db_id]['name']}")
                except Exception as e:
                    print(f"Error searching {self.databases[db_id]['name']}: {e}")
        
        return all_papers

    def save_results(self, papers, query):
        """Save results to both CSV and Excel"""
        if not papers:
            print("No papers to save")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"research_papers_{query.replace(' ', '_')}_{timestamp}"
        
        # Save to CSV
        csv_path = os.path.join(self.output_dir, f"{base_filename}.csv")
        df = pd.DataFrame(papers)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        # Save to Excel with formatting
        excel_path = os.path.join(self.output_dir, f"{base_filename}.xlsx")
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Research Papers', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Research Papers']
            
            # Formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4F81BD',
                'font_color': 'white',
                'border': 1
            })
            
            # Set column widths and formats
            columns = {
                'database': ('Database', 15),
                'title': ('Title', 40),
                'authors': ('Authors', 30),
                'abstract': ('Abstract', 50),
                'url': ('URL', 40),
                'date': ('Date', 15)
            }
            
            for col_num, (col_name, (header, width)) in enumerate(columns.items()):
                worksheet.write(0, col_num, header, header_format)
                worksheet.set_column(col_num, col_num, width)
        
        print(f"\nResults saved to:")
        print(f"CSV: {csv_path}")
        print(f"Excel: {excel_path}")

def main():
    scraper = ResearchDatabaseScraper()
    
    # Show available databases
    print("Available Databases:")
    for db_id, db_info in scraper.databases.items():
        print(f"{db_id}. {db_info['name']}")
    
    # Get user input
    selected_dbs = input("\nEnter database numbers separated by commas (e.g., 1,2,3): ")
    query = input("Enter search query: ")
    max_results = int(input("Enter maximum total results (default 50): ") or "50")
    
    print(f"\nSearching for '{query}' across selected databases...")
    papers = scraper.search_databases(query, selected_dbs, max_results)
    
    if papers:
        print(f"\nFound total of {len(papers)} papers")
        
        # Show distribution
        db_counts = {}
        for paper in papers:
            db_counts[paper['database']] = db_counts.get(paper['database'], 0) + 1
        
        print("\nResults distribution:")
        for db, count in db_counts.items():
            print(f"- {db}: {count} papers")
        
        # Save results
        scraper.save_results(papers, query)
    else:
        print("No papers found")

if __name__ == "__main__":
    main()