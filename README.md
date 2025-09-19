# Website SEO Analyzer by Brandon Tucker 

A comprehensive Python tool for analyzing website SEO performance, extracting keywords, and providing actionable optimization recommendations.

## Features

- **Complete SEO Analysis**: Analyzes title tags, meta descriptions, headings, and content structure
- **Keyword Extraction**: Automatically extracts and ranks keywords from page content
- **Image Analysis**: Checks for missing alt text and optimization opportunities
- **Content Quality Assessment**: Evaluates word count, readability, and content depth
- **Structured Data Detection**: Identifies JSON-LD and schema.org implementations
- **SEO Score Calculation**: Provides an overall SEO score with specific improvement areas
- **Local SEO Focus**: Optimized for local business and service provider websites
- **Detailed Reporting**: Generates both console output and JSON reports

## Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Dependencies

Install required packages:

```bash
pip install requests beautifulsoup4 lxml
```

Or using requirements.txt:

```bash
pip install -r requirements.txt
```

### Clone the Repository

```bash
git clone https://github.com/yourusername/website-seo-analyzer.git
cd website-seo-analyzer
```

## Usage

### Basic Usage

Analyze any website with a simple command:

```bash
python3 seo_analyzer.py https://example.com
```

### Example Output

```
======================================================================
SEO ANALYSIS REPORT FOR: https://wichitacomputersolutions.com
======================================================================

BASIC INFO:
Title: IT Support & Computer Repair Services in Wichita, KS
Title Length: 52 characters
Meta Description: Professional IT support and managed services...
Meta Description Length: 134 characters
Word Count: 847

HEADINGS:
H1: 1 tags
  - Professional IT Support Services in Wichita...
H2: 4 tags
  - Computer Repair Services...
  - Network Setup & Management...
  - Cybersecurity Solutions...

IMAGES:
Total Images: 12
Images Without Alt Text: 3

TOP 10 KEYWORDS:
 1. computer (8 times)
 2. services (7 times)
 3. support (6 times)
 4. network (5 times)
 5. business (4 times)
 6. wichita (4 times)
 7. repair (3 times)
 8. security (3 times)
 9. managed (3 times)
10. solutions (3 times)

STRUCTURED DATA:
Has Structured Data: True
Structured Data Blocks: 2

ISSUES TO FIX:
 1. 3 images missing alt text
 2. Meta description could be longer (134 chars). Aim for 150-160 characters

RECOMMENDATIONS:
 1. Add more local keywords like "Kansas IT support"
 2. Consider adding FAQ schema for better search visibility

SEO SCORE: 80/100
======================================================================

Detailed results saved to: seo_analysis.json
```

## Configuration

### Customizing Keyword Analysis

You can modify the keyword extraction parameters in the `SEOAnalyzer` class:

```python
# Adjust minimum word length and maximum keywords to extract
keywords = self.extract_keywords(text_content, min_length=3, max_keywords=50)
```

### Adding Custom Stop Words

Extend the stop words list for your specific industry:

```python
stop_words = {
    'the', 'a', 'an', 'and', 'or', 'but',
    # Add industry-specific stop words
    'click', 'here', 'more', 'info'
}
```

## Output Files

The tool generates several output files:

- **Console Output**: Immediate SEO analysis and recommendations
- **seo_analysis.json**: Detailed JSON report with all extracted data
- **Error Logs**: Automatic logging of any connection or parsing issues

### JSON Output Structure

```json
{
  "analysis_date": "2025-09-18",
  "page_data": {
    "url": "https://example.com",
    "title": "Page Title",
    "keywords": [["keyword", count], ...],
    "issues": [...],
    "recommendations": [...]
  },
  "report": {
    "score": 85,
    "issues": [...],
    "recommendations": [...]
  }
}
```

## Use Cases

### Local Business SEO
Perfect for analyzing local business websites like:
- IT consulting firms
- Medical practices
- Law offices
- Restaurants
- Service providers

### Content Marketing
- Blog post optimization
- Landing page analysis
- Product page SEO
- Competitor analysis

### SEO Audits
- Comprehensive website audits
- Pre/post optimization comparisons
- Bulk page analysis
- Content gap identification

## Advanced Features

### Batch Analysis

Analyze multiple URLs by modifying the script:

```python
urls = [
    'https://example.com',
    'https://example.com/services',
    'https://example.com/about'
]

for url in urls:
    analyzer = SEOAnalyzer(url)
    # ... analysis code
```

### Custom Scoring

Adjust the scoring algorithm for your specific needs:

```python
def custom_scoring(self, page_data):
    score = 100
    # Custom scoring logic
    if page_data['word_count'] < 500:
        score -= 20  # Penalize short content more heavily
    return score
```

## Troubleshooting

### Common Issues

**Connection Timeouts**
```bash
Error fetching https://example.com: HTTPSConnectionPool timeout
```
*Solution*: Increase timeout in the requests call or check your internet connection.

**SSL Certificate Errors**
```bash
SSL: CERTIFICATE_VERIFY_FAILED
```
*Solution*: Add SSL verification bypass (use cautiously):
```python
response = requests.get(url, headers=headers, verify=False)
```

**Permission Denied**
```bash
PermissionError: [Errno 13] Permission denied: 'seo_analysis.json'
```
*Solution*: Run with appropriate permissions or change output directory.

### Best Practices

1. **Rate Limiting**: Add delays between requests when analyzing multiple pages
2. **User Agent**: Always use a descriptive User-Agent string
3. **Error Handling**: Log errors for debugging rather than stopping execution
4. **Memory Management**: Process large sites in chunks to avoid memory issues

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the Repository**: Create your own fork of the project
2. **Create a Branch**: Make your changes in a feature branch
3. **Test Your Changes**: Ensure all functionality works as expected
4. **Submit a Pull Request**: Describe your changes and their benefits

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/website-seo-analyzer.git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development dependencies

# Run tests
python -m pytest tests/
```

### Code Style

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where appropriate
- Write unit tests for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0 (2025-09-18)
- Initial release
- Core SEO analysis functionality
- Keyword extraction and ranking
- JSON output support
- Command-line interface

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/website-seo-analyzer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/website-seo-analyzer/discussions)
- **Email**: [your-email@example.com]

## Acknowledgments

- Built with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Requests](https://docs.python-requests.org/) for HTTP handling
- Inspired by the need for accessible SEO analysis tools

## Roadmap

### Planned Features

- [ ] GUI interface using Tkinter or web-based dashboard
- [ ] Bulk URL analysis from CSV files
- [ ] Integration with Google Search Console API
- [ ] Page speed analysis integration
- [ ] Mobile-friendliness testing
- [ ] Competitor comparison features
- [ ] Automated report generation (PDF/HTML)
- [ ] WordPress plugin version
- [ ] API endpoint for web service integration

### Performance Improvements

- [ ] Async request handling for faster bulk analysis
- [ ] Caching mechanism for repeated analyses
- [ ] Memory optimization for large websites
- [ ] Progress bars for long-running analyses

--- 


**Star this repository if you find it useful!** ⭐

*Made with 💻 for the SEO community*
