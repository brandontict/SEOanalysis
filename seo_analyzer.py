#!/usr/bin/env python3
"""
Local SEO Website Analyzer
Run this on your server to analyze your website's SEO performance
Usage: python3 seo_analyzer.py https://wichitacomputersolutions.com
"""

import requests
from bs4 import BeautifulSoup
import sys
import re
from collections import Counter
from urllib.parse import urljoin, urlparse
import json

class SEOAnalyzer:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.results = {}
        
    def fetch_page(self, url):
        """Fetch page content with error handling"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; SEO-Analyzer/1.0)'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_keywords(self, text, min_length=3, max_keywords=50):
        """Extract and rank keywords from text content"""
        # Remove HTML and normalize text
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text.lower())
        
        # Common stop words to filter out
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 
            'can', 'may', 'might', 'this', 'that', 'these', 'those', 'i', 'you', 
            'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'get', 'go', 'come', 'see', 'know', 'think', 'want', 'need', 'use',
            'work', 'call', 'try', 'ask', 'feel', 'become', 'leave', 'put'
        }
        
        # Extract words
        words = re.findall(r'\b[a-z]{' + str(min_length) + ',}\b', text)
        words = [word for word in words if word not in stop_words]
        
        # Count and return top keywords
        return Counter(words).most_common(max_keywords)
    
    def analyze_page(self, url):
        """Analyze a single page for SEO elements"""
        html = self.fetch_page(url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract basic SEO elements
        title = soup.find('title')
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        
        # Extract headings
        headings = {
            'h1': [h.get_text().strip() for h in soup.find_all('h1')],
            'h2': [h.get_text().strip() for h in soup.find_all('h2')],
            'h3': [h.get_text().strip() for h in soup.find_all('h3')]
        }
        
        # Extract images and check alt attributes
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'has_alt': bool(img.get('alt'))
            })
        
        # Extract text content for keyword analysis
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text_content = soup.get_text()
        keywords = self.extract_keywords(text_content)
        
        # Check for structured data
        structured_data = soup.find_all('script', type='application/ld+json')
        
        return {
            'url': url,
            'title': title.get_text() if title else None,
            'title_length': len(title.get_text()) if title else 0,
            'meta_description': meta_desc.get('content') if meta_desc else None,
            'meta_desc_length': len(meta_desc.get('content')) if meta_desc else 0,
            'meta_keywords': meta_keywords.get('content') if meta_keywords else None,
            'headings': headings,
            'images': images,
            'images_without_alt': len([img for img in images if not img['has_alt']]),
            'total_images': len(images),
            'keywords': keywords,
            'word_count': len(text_content.split()),
            'has_structured_data': len(structured_data) > 0,
            'structured_data_count': len(structured_data)
        }
    
    def generate_seo_issues(self, page_data):
        """Identify SEO issues and recommendations"""
        issues = []
        recommendations = []
        
        # Title analysis
        if not page_data['title']:
            issues.append("Missing title tag")
        elif page_data['title_length'] < 30:
            issues.append(f"Title too short ({page_data['title_length']} chars). Aim for 30-60 characters")
        elif page_data['title_length'] > 60:
            issues.append(f"Title too long ({page_data['title_length']} chars). Aim for 30-60 characters")
        
        # Meta description analysis
        if not page_data['meta_description']:
            issues.append("Missing meta description")
        elif page_data['meta_desc_length'] < 120:
            issues.append(f"Meta description too short ({page_data['meta_desc_length']} chars). Aim for 120-160 characters")
        elif page_data['meta_desc_length'] > 160:
            issues.append(f"Meta description too long ({page_data['meta_desc_length']} chars). Aim for 120-160 characters")
        
        # Heading analysis
        if not page_data['headings']['h1']:
            issues.append("Missing H1 tag")
        elif len(page_data['headings']['h1']) > 1:
            issues.append(f"Multiple H1 tags ({len(page_data['headings']['h1'])}). Use only one H1 per page")
        
        # Image analysis
        if page_data['images_without_alt'] > 0:
            issues.append(f"{page_data['images_without_alt']} images missing alt text")
        
        # Content analysis
        if page_data['word_count'] < 300:
            issues.append(f"Low word count ({page_data['word_count']}). Aim for at least 300 words")
        
        # Structured data
        if not page_data['has_structured_data']:
            recommendations.append("Add structured data (JSON-LD) for better search visibility")
        
        # Keyword recommendations for IT consulting
        it_keywords = ['computer', 'repair', 'support', 'network', 'security', 'managed', 'services', 'business', 'wichita']
        found_keywords = [kw[0] for kw in page_data['keywords'][:10]]
        missing_it_keywords = [kw for kw in it_keywords if kw not in ' '.join(found_keywords)]
        
        if missing_it_keywords:
            recommendations.append(f"Consider adding IT-related keywords: {', '.join(missing_it_keywords[:5])}")
        
        return issues, recommendations
    
    def generate_report(self, page_data):
        """Generate comprehensive SEO report"""
        issues, recommendations = self.generate_seo_issues(page_data)
        
        print("=" * 70)
        print(f"SEO ANALYSIS REPORT FOR: {page_data['url']}")
        print("=" * 70)
        
        print(f"\nBASIC INFO:")
        print(f"Title: {page_data['title']}")
        print(f"Title Length: {page_data['title_length']} characters")
        print(f"Meta Description: {page_data['meta_description']}")
        print(f"Meta Description Length: {page_data['meta_desc_length']} characters")
        print(f"Word Count: {page_data['word_count']}")
        
        print(f"\nHEADINGS:")
        for level, headings in page_data['headings'].items():
            print(f"{level.upper()}: {len(headings)} tags")
            for heading in headings[:3]:  # Show first 3
                print(f"  - {heading[:60]}...")
        
        print(f"\nIMAGES:")
        print(f"Total Images: {page_data['total_images']}")
        print(f"Images Without Alt Text: {page_data['images_without_alt']}")
        
        print(f"\nTOP 10 KEYWORDS:")
        for i, (keyword, count) in enumerate(page_data['keywords'][:10], 1):
            print(f"{i:2d}. {keyword} ({count} times)")
        
        print(f"\nSTRUCTURED DATA:")
        print(f"Has Structured Data: {page_data['has_structured_data']}")
        print(f"Structured Data Blocks: {page_data['structured_data_count']}")
        
        if issues:
            print(f"\nISSUES TO FIX:")
            for i, issue in enumerate(issues, 1):
                print(f"{i:2d}. {issue}")
        
        if recommendations:
            print(f"\nRECOMMENDations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"{i:2d}. {rec}")
        
        # Calculate SEO score
        score = 100
        score -= len(issues) * 10  # -10 points per issue
        score = max(0, score)  # Don't go below 0
        
        print(f"\nSEO SCORE: {score}/100")
        print("=" * 70)
        
        return {
            'score': score,
            'issues': issues,
            'recommendations': recommendations
        }

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 seo_analyzer.py <website_url>")
        print("Example: python3 seo_analyzer.py https://wichitacomputersolutions.com")
        sys.exit(1)
    
    url = sys.argv[1]
    analyzer = SEOAnalyzer(url)
    
    print(f"Analyzing website: {url}")
    print("Please wait...")
    
    # Analyze the main page
    page_data = analyzer.analyze_page(url)
    
    if page_data:
        report = analyzer.generate_report(page_data)
        
        # Save detailed results to JSON file
        with open('seo_analysis.json', 'w') as f:
            json.dump({
                'analysis_date': str(sys.version),  # Using sys.version as a timestamp substitute
                'page_data': page_data,
                'report': report
            }, f, indent=2)
        
        print(f"\nDetailed results saved to: seo_analysis.json")
    else:
        print("Failed to analyze the website. Check the URL and try again.")

if __name__ == "__main__":
    main()
