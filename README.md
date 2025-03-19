# Resume-Screening-Ranking-System
A project for automated resume screening and ranking system
# 🚀 Resume Screening & Ranking System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9-green.svg)
![NLP](https://img.shields.io/badge/NLP-powered-orange.svg)

An intelligent, AI-driven application that automates the tedious process of screening and ranking resumes against job descriptions. Say goodbye to manual resume filtering!

## ✨ Features

- **PDF Text Extraction** - Seamlessly extract text content from uploaded resume PDFs
- **Smart Validation** - Automatically validate job descriptions and resumes for proper formatting and content
- **TF-IDF Ranking** - Rank resumes based on their relevance to job descriptions using TF-IDF and cosine similarity
- **Key Skills Analysis** - Identify and match essential skills between job descriptions and candidate resumes
- **Enhanced Ranking** - Leverage advanced NLP techniques for more accurate candidate matching
- **Interactive Visualization** - View results through intuitive charts and graphs
- **User-Friendly Web Interface** - Easy-to-use Streamlit web application for non-technical users

## 🖥️ Demo

<!-- Replace with actual screenshot when available -->
![Resume Ranking Demo](https://raw.githubusercontent.com/koustav24/Resume-Screening-Ranking-System/main/Screenshots/Home-Page.png)
![Resume Ranking Demo](https://raw.githubusercontent.com/koustav24/Resume-Screening-Ranking-System/main/Screenshots/Data-Input.png)
![Resume Ranking Demo](https://raw.githubusercontent.com/koustav24/Resume-Screening-Ranking-System/main/Screenshots/Data-Output.png)
![Resume Ranking Demo](https://raw.githubusercontent.com/koustav24/Resume-Screening-Ranking-System/main/Screenshots/Data-Output(2).png)
## 🛠️ Technologies

- **Python** - Core programming language
- **Streamlit** - Web application framework
- **PyPDF2** - PDF text extraction
- **NLTK & spaCy** - Natural Language Processing
- **Scikit-learn** - TF-IDF vectorization and similarity metrics
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations
- **Sentence Transformers** - Advanced semantic text processing

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/koustav24/Resume-Screening-Ranking-System.git
   cd Resume-Screening-Ranking-System
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to `http://localhost:8501`

## 📊 How It Works

1. **Upload Job Description** - Paste or upload a detailed job description
2. **Upload Resumes** - Upload multiple candidate resumes in PDF format
3. **Process and Analyze** - The system extracts text, validates documents, and performs multi-factor analysis
4. **View Rankings** - See ranked results with match scores and key skills visualization
5. **Export Results** - Save the analysis for your recruitment process

## 🔍 Ranking Methodology

The system uses a sophisticated multi-factor ranking approach:

- **TF-IDF Vectorization** - Converts text to numerical vectors focusing on important terms
- **Cosine Similarity** - Measures document similarity regardless of document length
- **Key Skills Extraction** - Identifies and matches critical job-specific skills
- **Semantic Analysis** - Uses advanced NLP to understand context beyond keywords
- **Weighted Scoring** - Combines multiple factors for a comprehensive final score

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

Your Name - koustavkamrakar2004@gmail.com

Project Link: [https://github.com/koustav24/Resume-Screening-Ranking-System](https://github.com/koustav24/Resume-Screening-Ranking-System)

---

💼 *Streamline your recruitment process with data-driven candidate selection!*