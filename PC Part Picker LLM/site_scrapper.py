import os
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from urllib.parse import urljoin, urlparse


# Function to scrape website content
def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


# Function to extract title, headers, and paragraphs from the scraped content
def extract_data(soup):
    title = soup.title.string if soup.title else 'No Title'
    headers = [header.get_text() for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    return title, headers, paragraphs


# Function to get pagination and internal links
def get_links(soup, base_url):
    links = set()

    # Pagination links
    pagination = soup.find('div', class_='pagination')  # Adjust selector based on website
    if pagination:
        for link in pagination.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            links.add(full_url)

    # Internal links
    for link in soup.find_all('a', href=True):
        href = link['href']
        if not href.startswith(('http://', 'https://')):
            full_url = urljoin(base_url, href)
            parsed_base = urlparse(base_url)
            parsed_url = urlparse(full_url)
            # Filter to follow only links within the same domain
            if parsed_base.netloc == parsed_url.netloc:
                links.add(full_url)

    return links


# Function to generate a single PDF with aggregated content using reportlab
def generate_pdf(title, headers, paragraphs, output_filename='PC_Hardware_News_Compilation.pdf'):
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    header_style = styles['Heading2']
    normal_style = styles['Normal']

    pdf = SimpleDocTemplate(output_filename, pagesize=letter)
    story = []

    # Title Formatting
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))

    # Header Formatting
    for header in headers:
        story.append(Paragraph(header, header_style))
        story.append(Spacer(1, 6))

    # Paragraph Formatting
    for paragraph in paragraphs:
        story.append(Paragraph(paragraph, normal_style))
        story.append(Spacer(1, 12))

    # Build the PDF
    pdf.build(story)
    print(f"PDF generated successfully and saved as {output_filename}!")


# Main script
if __name__ == '__main__':
    urls = [
        'https://www.anandtech.com/'  # Add more URLs as needed
    ]

    all_headers = []
    all_paragraphs = []
    visited_urls = set()
    page_limit = 600  # Limit the total number of pages to scrape
    total_pages_scraped = 0


    def scrape_all(url, depth=0, max_depth=5):
        global total_pages_scraped
        if url in visited_urls or depth > max_depth or total_pages_scraped >= page_limit:
            return
        visited_urls.add(url)

        print(f"Scraping {url}")
        soup = scrape_website(url)
        if soup:
            title, headers, paragraphs = extract_data(soup)
            all_headers.extend(headers)
            all_paragraphs.extend(paragraphs)
            total_pages_scraped += 1

            # Collect links
            links = get_links(soup, url)
            for link in links:
                if total_pages_scraped >= page_limit:
                    break
                scrape_all(link, depth + 1)  # Recursively scrape internal links with increased depth


    # Start scraping from each URL
    for start_url in urls:
        scrape_all(start_url)

    # Generate a single PDF with aggregated content
    generate_pdf('Aggregated Content from Multiple Pages', all_headers, all_paragraphs,
                 'PC_Hardware_News_Compilation.pdf')
