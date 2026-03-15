# 🏗️ DDR Report Generator

AI-powered system that automatically generates Detailed Diagnostic Reports (DDR) by combining visual inspection reports and thermal imaging data.

---

## 🎯 Overview

This system reads inspection and thermal PDF reports, extracts relevant information and images, detects conflicts between reports, and generates a structured client-ready DDR with embedded images.

---

## ✨ Features

- 📄 Automatic text extraction from PDF reports
- 🖼️ Smart image filtering (removes logos, blank pages)
- 🔍 AI-powered conflict detection between reports
- 📊 Structured DDR generation with 8 required sections
- 🎯 Intelligent image placement in reports

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))

### Setup
```bash
# Clone repository
git clone https://github.com/devsoni0419/ddr_ai_builder.git
cd ddr_ai_builder

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your OPEN_ROUTER_API_KEY in .env file
```

---

## 💻 Usage
```bash
streamlit run app.py
```

1. Upload Inspection Report PDF
2. Upload Thermal Report PDF
3. Click "Generate DDR Report"
4. Download the generated report

---

## 📊 Output Structure

Every generated DDR contains:

1. **Property Issue Summary** - Overview of all issues
2. **Area-wise Observations** - Detailed findings with images
3. **Probable Root Cause** - Analysis of underlying causes
4. **Severity Assessment** - Risk ratings with reasoning
5. **Recommended Actions** - Prioritized remediation steps
6. **Additional Notes** - Supplementary information
7. **Missing or Unclear Information** - Explicitly marked as "Not Available"
8. **Conflicting Information** - Contradictions between reports

---

## 🧠 How It Works

### 5-Step Agent Workflow

1. **Text Extraction** - Extract observations from both PDFs
2. **Image Extraction** - Extract images with metadata
3. **Image Filtering** - Filter relevant images (size, aspect ratio, brightness)
4. **Conflict Detection** - AI detects contradictions between reports
5. **DDR Generation** - LLM generates structured report with image markers

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **PDF Processing**: PyMuPDF (fitz)
- **Image Processing**: Pillow
- **AI/LLM**: OpenRouter API (DeepSeek Chat)
- **Language**: Python 3.10+

---

## 📁 Project Structure
```
ddr_ai_builder/
├── app.py                    # Streamlit UI
├── agent_runner.py           # Main workflow orchestrator
├── tools.py                  # Tool wrapper functions
├── extract.py                # PDF text/image extraction
├── image_filter.py           # Image filtering logic
├── conflict_detector.py      # AI conflict detection
├── generate_report.py        # DDR generation
├── requirements.txt          # Dependencies
└── .env.example              # Environment template
```

---

## ⚠️ Limitations

1. **Image Placement** - Sequential placement based on markers, not semantic matching
2. **Conflict Detection** - May produce false positives, requires human review
3. **Report Formats** - Optimized for similar report structures
4. **API Dependency** - Requires internet connection
5. **Image Quality** - Basic filtering, no blur detection or relevance scoring

---

## 🚀 Future Improvements

### High Priority
1. **Vision-Language Models** - Use CLIP for semantic image-text matching
2. **Structured Output Validation** - JSON schema enforcement for DDR sections
3. **OCR Support** - Handle scanned PDFs

### Medium Priority
4. **Image Quality Scoring** - Blur detection and relevance classification
5. **Batch Processing** - Process multiple report pairs simultaneously
6. **Multi-Format Export** - PDF, DOCX, HTML exports

---

**Dev Soni**

📧 Email: devsoni0419@gmail.com  
🔗 GitHub: [@devsoni0419](https://github.com/devsoni0419)

---
