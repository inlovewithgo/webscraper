# 🔥 Advanced Web Scraping Tool

A powerful, modern web scraping application with a beautiful React frontend and robust FastAPI backend. Extract company data from any website, generate professional PDF reports, and manage scraping tasks through an intuitive dashboard.

![Web Scraping Tool](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![React](https://img.shields.io/badge/React-18+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🚀 **Core Capabilities**
- **Multi-URL Discovery**: Automatically discovers and processes related URLs from target websites
- **Dynamic Content Handling**: Uses Selenium for JavaScript-heavy sites with fallback to requests
- **Intelligent Data Extraction**: Extracts company names, contact information, services, social media, and more
- **Pagination Support**: Automatically handles paginated content across multiple pages
- **Real-time Task Tracking**: Monitor scraping progress with live status updates

### 📊 **Advanced Data Processing**
- **Smart Contact Detection**: Extracts emails, phone numbers, and social media profiles
- **Business Intelligence**: Identifies company taglines, descriptions, services, and industry classification
- **Unicode Text Handling**: Properly processes emojis, special characters, and international text
- **Data Validation**: Filters and validates extracted information for quality assurance

### 📄 **Professional Reporting**
- **PDF Report Generation**: Creates beautifully formatted PDF reports with scraped data
- **Executive Summaries**: Includes extraction statistics and metadata
- **One-Click Downloads**: Download reports directly from the web interface
- **Comprehensive Data Display**: Organized presentation of all extracted information

### 🎨 **Modern User Interface**
- **Glassmorphism Design**: Modern, translucent UI with animated elements
- **Real-time Updates**: Live task status and progress monitoring
- **Responsive Layout**: Works seamlessly on desktop and mobile devices
- **Professional Styling**: Blue gradient themes with smooth animations

## 🛠️ Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Database ORM with SQLite
- **Selenium** - Dynamic content and JavaScript handling
- **BeautifulSoup** - HTML parsing and data extraction
- **FPDF2** - PDF report generation
- **Loguru** - Advanced logging system

### Frontend
- **React** - Modern JavaScript UI framework
- **Vite** - Fast development build tool
- **CSS3** - Custom styling with animations
- **Fetch API** - HTTP client for backend communication

### Data Processing
- **Requests** - HTTP client for static content
- **PyQuery** - jQuery-like HTML manipulation
- **Unicodedata** - Text normalization and sanitization
- **Regex** - Pattern matching for data extraction

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Chrome Browser** (for Selenium)
- **Git** (for cloning)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/inlovewithgo/webscraper.git
cd web-scraping-tool
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create reports directory
mkdir reports

# Start the FastAPI server
python -m uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📦 Installation Dependencies

### Backend Requirements (`requirements.txt`)
```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
selenium==4.15.2
beautifulsoup4==4.12.2
requests==2.31.0
requests-html==0.10.0
lxml==4.9.3
sqlalchemy==2.0.23
pydantic==2.5.0
fpdf2==2.7.6
email-validator==2.1.0
phonenumbers==8.13.26
loguru==0.7.2
python-dateutil==2.8.2
httpx==0.25.2
pyquery==2.0.0
pandas==2.1.3
```

### Frontend Dependencies
```bash
npm install react react-dom @vitejs/plugin-react vite
```

### ChromeDriver Setup
Download ChromeDriver from: https://chromedriver.chromium.org/downloads
Place `chromedriver.exe` in your backend folder or add to PATH.

## 📖 Usage Guide

### Basic Scraping Workflow

1. **Open the dashboard** at http://localhost:3000
2. **Enter a target URL** in the input field
3. **Click "Scrape"** to start the extraction process
4. **Monitor progress** through real-time status updates
5. **Download PDF report** once scraping is complete

### Advanced Features

#### URL Discovery
The system automatically discovers related URLs from the target website:
- Follows internal links
- Identifies relevant pages
- Processes multiple pages efficiently

#### Data Extraction Types
- **Company Information**: Names, descriptions, taglines
- **Contact Details**: Emails, phone numbers, addresses
- **Business Data**: Services, industry classification
- **Social Media**: LinkedIn, Twitter, Facebook profiles
- **Technical Info**: Page metadata and timestamps

#### Task Management
- View all scraping tasks in the dashboard
- Monitor real-time status (queued, running, completed, failed)
- Access historical data and reports
- Download PDF reports for any completed task

## 🔧 Configuration

### Database Setup
The application uses SQLite by default. The database file (`scraper.db`) is created automatically.

### Selenium Configuration
Modify `app/scraper/dynamic.py` to customize browser settings:
```python
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
```

### PDF Report Customization
Edit `app/scraper/engine.py` to modify report formatting:
- Change fonts and colors
- Add custom headers/footers
- Modify data layout and sections

## 📁 Project Structure

```
webscraper/
├── backend/
│   ├── app/
│   │   ├── scraper/
│   │   │   ├── engine.py          # Main scraping logic
│   │   │   ├── extractors.py      # Data extraction functions
│   │   │   ├── dynamic.py         # Selenium handling
│   │   │   ├── pagination.py      # Pagination logic
│   │   │   └── url_discovery.py   # URL discovery
│   │   ├── main.py                # FastAPI application
│   │   ├── models.py              # Database models
│   │   ├── schemas.py             # Pydantic schemas
│   │   ├── database.py            # Database configuration
│   │   └── logging_config.py      # Logging setup
│   ├── reports/                   # Generated PDF reports
│   ├── requirements.txt           # Python dependencies
│   └── scraper.db                 # SQLite database
├── frontend/
│   ├── src/
│   │   ├── Dashboard.jsx          # Main dashboard component
│   │   ├── ScrapeForm.jsx         # URL input form
│   │   ├── ResultsTable.jsx       # Data display table
│   │   ├── TaskStatus.jsx         # Status monitoring
│   │   ├── api.js                 # API client
│   │   ├── main.css               # Custom styling
│   │   └── App.jsx                # Root component
│   ├── package.json               # Node.js dependencies
│   └── vite.config.js             # Vite configuration
└── README.md                      # This file
```

## 🔌 API Reference

### Core Endpoints

#### Start Scraping Task
```http
POST /scrape
Content-Type: application/json

{
  "url": "https://example.com"
}
```

#### Get Task Results
```http
GET /result/{task_id}
```

#### List All Tasks
```http
GET /tasks
```

#### Download PDF Report
```http
GET /download-pdf/{task_id}
```

#### Health Check
```http
GET /health
```

### Response Examples

#### Scraping Response
```json
{
  "task_id": 123,
  "status": "queued"
}
```

#### Results Response
```json
{
  "id": 1,
  "task_id": 123,
  "data": [
    {
      "url": "https://example.com",
      "company": "Example Corp",
      "contacts": {
        "emails": ["contact@example.com"],
        "phones": ["+1-555-123-4567"]
      },
      "tagline": "Leading technology solutions",
      "services": ["Web Development", "Consulting"],
      "social_media": {
        "linkedin": "https://linkedin.com/company/example"
      },
      "industry": "Technology",
      "extracted_at": "2025-07-10T08:30:00.000Z"
    }
  ]
}
```

## 🐛 Troubleshooting

### Common Issues

#### 1. ChromeDriver Not Found
```bash
# Download ChromeDriver and add to PATH or place in project folder
# Error: selenium.common.exceptions.WebDriverException
```

#### 2. Database Connection Issues
```bash
# Delete and recreate database
rm scraper.db
python -m uvicorn app.main:app --reload
```

#### 3. PDF Generation Errors
```bash
# Usually caused by Unicode characters
# The system automatically sanitizes text, but check logs for details
```

#### 4. Port Already in Use
```bash
# Change port in uvicorn command
python -m uvicorn app.main:app --reload --port 8001
```

### Performance Optimization

#### For Large-Scale Scraping
- Implement request rate limiting
- Add concurrent processing
- Use Redis for task queuing
- Implement database indexing

#### Memory Management
- Clear browser cache regularly
- Limit concurrent Selenium instances
- Implement data pagination for large datasets

## 🔒 Security Considerations

### Best Practices
- **Rate Limiting**: Respect website robots.txt and implement delays
- **User Agents**: Use realistic browser user agents
- **Legal Compliance**: Ensure scraping complies with website terms of service
- **Data Privacy**: Handle extracted data according to privacy regulations

### Production Deployment
- Use environment variables for sensitive configuration
- Implement proper authentication and authorization
- Set up HTTPS with SSL certificates
- Configure proper CORS policies
- Use a production database (PostgreSQL/MySQL)

## 🚀 Advanced Usage

### Custom Data Extractors
Create custom extraction logic in `app/scraper/extractors.py`:

```python
def extract_custom_data(html, url):
    soup = BeautifulSoup(html, "html.parser")
    
    # Your custom extraction logic here
    custom_field = soup.select_one(".custom-selector")
    
    return {
        "custom_data": custom_field.text if custom_field else None
    }
```

### Database Migrations
For production, use Alembic for database migrations:

```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Docker Deployment
Create `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📈 Performance Metrics

### Typical Performance
- **Processing Speed**: 3-4 seconds per URL
- **Success Rate**: 90-95% for most websites
- **Memory Usage**: ~100MB for standard operations
- **PDF Generation**: <1 second for reports up to 100 records

### Scalability Features
- Asynchronous task processing
- Database connection pooling
- Automatic error recovery
- Resource cleanup and management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Add tests for new features
- Update documentation as needed

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **React** for the powerful frontend library
- **Selenium** for browser automation capabilities
- **BeautifulSoup** for HTML parsing excellence

## 📞 Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the API documentation
- Contact the development team
- Mail : wilfred.shubham@gmail.com

---

**Built with ❤️ for the web scraping community**

*Happy scraping! 🚀*
