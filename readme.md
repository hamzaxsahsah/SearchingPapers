# Research Paper Scraper

A Python tool for searching and downloading research papers from multiple academic databases simultaneously.

## Features

- **Multi-Database Support:**
  - arXiv
  - IEEE Xplore
  - Google Scholar
  - Science Direct
  - PubMed

- **Key Capabilities:**
  - Parallel searching across multiple databases
  - Customizable search parameters
  - Export to both CSV and Excel formats
  - Automatic metadata extraction
  - Search in titles and abstracts
  - Results distribution statistics

## Installation

### 1. Prerequisites
Make sure you have Python 3.7+ installed on your system.

### 2. Required Packages
Install the required Python packages using pip:

```bash
pip install requests
pip install beautifulsoup4
pip install pandas
pip install xlsxwriter
```

### 3. Download
Download the script `research_scraper.py` to your local machine.

## Usage

### Basic Usage

1. Run the script:
```bash
python research_scraper.py
```

2. Select databases when prompted:
```
Available Databases:
1. arXiv
2. IEEE Xplore
3. Google Scholar
4. Science Direct
5. PubMed

Enter database numbers separated by commas (e.g., 1,2,3):
```

3. Enter your search query when prompted:
```
Enter search query:
```

4. Specify maximum results:
```
Enter maximum total results (default 50):
```

### Output Files

The script creates two types of output files in a `research_papers` directory:

1. CSV file (`research_papers_[query]_[timestamp].csv`)
2. Excel file (`research_papers_[query]_[timestamp].xlsx`)

Both files contain:
- Database source
- Paper title
- Authors
- Abstract
- URL
- Publication date

## Database-Specific Notes

### arXiv
- Most reliable and fastest
- No authentication required
- Includes full abstracts
- Best for computer science, physics, and mathematics

### IEEE Xplore
- Uses public web interface
- May have rate limiting
- Best for engineering and computer science papers
- Some content might require institutional access

### Google Scholar
- Wide coverage across disciplines
- May have CAPTCHA challenges
- Limited abstract availability
- Best for initial broad searches

### Science Direct
- Focuses on published journal articles
- Some content requires subscription
- Good abstract availability
- Best for peer-reviewed research

### PubMed
- Specialized in medical and biological sciences
- Free access to metadata
- Reliable abstract availability
- Best for biomedical research

## Common Issues and Solutions

### Rate Limiting
**Problem:** Too many requests in short time
**Solution:** 
- Reduce number of databases searched simultaneously
- Add delays between searches
- Use proxy rotation (advanced)

### No Results
**Problem:** Empty search results
**Solutions:**
1. Check your search query
2. Try fewer databases first
3. Reduce maximum results
4. Check internet connection

### Parse Errors
**Problem:** Error parsing results
**Solutions:**
1. Try updating the required packages
2. Check for website layout changes
3. Report issues to maintainers

### Access Denied
**Problem:** Database blocks access
**Solutions:**
1. Wait before retrying
2. Use different databases
3. Check if database requires authentication

## Best Practices

1. **Search Query Tips:**
   - Use specific keywords
   - Combine related terms
   - Use quotes for exact phrases
   - Start with fewer keywords

2. **Database Selection:**
   - Start with arXiv for testing
   - Add databases gradually
   - Match databases to your field
   - Consider combining complementary databases

3. **Results Management:**
   - Review distribution statistics
   - Check for duplicates
   - Verify paper availability
   - Save important searches

## Advanced Usage

### Customizing Search Parameters

Modify the script to:
- Add custom filters
- Change sort order
- Adjust timeouts
- Add proxy support

### Adding New Databases

To add a new database:
1. Create new search method
2. Add database config
3. Implement result parsing
4. Add error handling

## Limitations

1. **Access Restrictions:**
   - Some papers require subscriptions
   - Database access may be limited
   - CAPTCHA challenges possible

2. **Data Availability:**
   - Abstract availability varies
   - Full text usually not included
   - Metadata completeness varies

3. **Technical Limitations:**
   - Rate limiting
   - Parse errors possible
   - Network dependencies

## Contributing

Feel free to contribute by:
- Reporting issues
- Suggesting improvements
- Adding new databases
- Enhancing documentation

## License

This project is open-source and available under the MIT License.

## Disclaimer

Use this tool responsibly and in accordance with each database's terms of service. The script is for educational and research purposes only.