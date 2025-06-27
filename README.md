# TechSalaryToday 🚀

> A comprehensive web scraping and data analysis platform for tech job market insights in the Netherlands

## 🎯 Project Overview

TechSalaryToday is a full-stack application designed to scrape, analyze, and present real-time insights about the Dutch tech job market. This project demonstrates modern web scraping techniques, data processing, and visualization capabilities specifically tailored for the Netherlands technology sector.

## 🛠️ Technology Stack

### Frontend

- **React 18** with **TypeScript** - Modern, type-safe UI development
- **Responsive Design** - Mobile-first approach

### Backend

- **Java 17** with **Spring Boot 3** - Enterprise-grade REST API
- **PostgreSQL** - Robust relational database
- **Python** - Data processing and web scraping scripts

### DevOps & Cloud

- **Docker** - Containerization
- **Azure** - Cloud deployment and services
- **GitHub Actions** - CI/CD pipeline

## 🏗️ Project Structure

```
TechSalaryToday/
├── POC/                          # Proof of Concepts
│   └── poc_scraper/             # Web scraping PoC
│       ├── poc_scraper.py       # Main scraping logic
│       └── structured_job_analysis.json
├── frontend/                     # React TypeScript frontend (coming soon)
├── backend/                      # Spring Boot backend (coming soon)
├── scripts/                      # Python data processing scripts
└── docs/                        # Documentation
```

## 🔍 Current Features (PoC Phase)

### Web Scraping Engine

- **Multi-strategy scraping**: Both `requests + BeautifulSoup` and `Selenium` for dynamic content
- **Intelligent content parsing**: Automatic section detection using regex patterns
- **Robust error handling**: Comprehensive error recovery and retry mechanisms
- **Translation support**: Automated Dutch-to-English translation using Groq API (10x faster than traditional services)

### Data Processing

- **Structured data extraction**: Converts unstructured job postings into clean JSON
- **Content categorization**: Automatically identifies job requirements, benefits, and descriptions
- **Multi-language support**: Handles both Dutch and English content

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or pipenv
- Chrome/Chromium browser (for Selenium)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/miloyiyangsun/TechSalaryToday.git
cd TechSalaryToday
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
# Create .env file and add your API keys
# See CONFIG.md for detailed instructions
export GROQ_API_KEY=your-groq-api-key-here
```

4. Run the scraper PoC:

```bash
cd POC/poc_scraper
python3 test_groq_translation.py  # Test translation first
python3 poc_scraper.py            # Run main scraper
```

## 📊 Sample Output

The scraper extracts structured job information including:

- Company details and location
- Job requirements and qualifications
- Salary ranges and benefits
- Employment conditions
- Translated content for international analysis

## 🎯 Roadmap

### Phase 1: MVP Development (Current)

- [x] Web scraping PoC
- [x] Data structure design
- [ ] Spring Boot REST API
- [ ] React frontend
- [ ] Docker containerization

### Phase 2: Enhanced Features

- [ ] Real-time job alerts
- [ ] Salary trend analysis
- [ ] Company comparison tools
- [ ] Advanced filtering and search

### Phase 3: Production Deployment

- [ ] Azure cloud deployment
- [ ] CI/CD pipeline
- [ ] Performance optimization
- [ ] User authentication

## 🤝 Contributing

This project is currently in active development. Contributions, issues, and feature requests are welcome!

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Yiyang Sun**

- Computer Science Student at VU Amsterdam
- Former Digital Marketing Professional with 5+ years experience
- LinkedIn: [Connect with me](https://linkedin.com/in/yiyang-sun)

---

_Built with ❤️ for the Dutch tech community_
