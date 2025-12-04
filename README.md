# Amazon Content Generation System

A powerful AI-powered system for generating optimized Amazon product listings using Google's Gemini AI. Choose between a **Single Agent** (fast, simple) or **Multi-Agent Pipeline** (modular, detailed) approach.

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone git@github.com:MarioMZhang/amazon-seller-assistant.git
cd amazon-seller-assistant

# Install dependencies with Poetry
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

**Get your Google AI API key:** https://aistudio.google.com/app/apikey

### 2. Run Single Agent (Recommended)

```bash
poetry run python3 single_agent_main.py \
  --model gemini-2.5-flash-lite \
  --brand-name "Your Brand" \
  --product-type "Your Product" \
  --top-n 30
```

**Output:** `output/single_agent_output.json`

### 3. Web Interface (Optional)

Use the web interface for a visual, user-friendly experience:

```bash
# Terminal 1: Start backend API
poetry run api-server

# Terminal 2: Start frontend
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser to:
- Upload XLSX files via drag-and-drop
- Configure parameters with visual forms
- View beautifully formatted results
- Download JSON output with one click

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture Options](#architecture-options)
- [Web Interface](#web-interface)
- [Single Agent Usage](#single-agent-usage)
- [Multi-Agent Pipeline](#multi-agent-pipeline)
- [XLSX Data Processing](#xlsx-data-processing)
- [Output Format](#output-format)
- [Requirements & Guidelines](#requirements--guidelines)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

---

## Overview

This system generates complete Amazon product listings including:
- ✅ **3 Title Variations** (optimized for Amazon search)
- ✅ **10 Bullet Points** (2 versions: feature-focused & benefit-focused)
- ✅ **Product Description** (1500-1950 characters, highly persuasive)
- ✅ **Search Keywords** (≤250 characters, no repetition)
- ✅ **Quality Validation** (grammar, compliance, SEO optimization)
- ✅ **SEO Rationale** (strategic recommendations)

**Input:** XLSX files with keyword research and competitor data
**Output:** Production-ready Amazon listing content in JSON format

---

## Architecture Options

### Single Agent System (⚡ Recommended)

**Best for:** Fast content generation, lower API costs, simple workflow

```bash
poetry run python3 single_agent_main.py --model gemini-2.5-flash-lite --top-n 30
```

**Advantages:**
- 🚀 1 API call vs 6 (faster)
- 💰 Lower token usage and cost
- ⚡ 10-15 second execution time
- 🎯 Simple, unified prompt
- ✨ Easier to maintain

**How it works:**
```
XLSX Files → XlsxProcessorTool → Single Agent → Complete Content
```

### Multi-Agent Pipeline (🔧 Advanced) - ⚠️ WIP

> **Note:** The multi-agent system is currently a Work In Progress and may not be fully functional. We recommend using the Single Agent System for production use.

**Best for:** Modular approach, step-by-step control, debugging

```bash
poetry run python3 main.py --model gemini-2.0-flash-exp
```

**Advantages:**
- 🔍 Step-by-step execution visibility
- 🛠️ Fine-grained control per agent
- 📊 Detailed intermediate outputs
- 🧩 Highly modular and extensible

**6-Step Pipeline:**
```
1. DataIngestionAgent → Structures input data
2. TitleAgent → Generates 3 titles
3. BulletPointAgent → Creates 2 bullet sets
4. DescriptionAgent → Writes description + keywords
5. QualityCheckAgent → Validates content
6. ArgumentationAgent → Provides SEO rationale
```

---

## Web Interface

### 🌐 Overview

The web interface provides a beautiful, intuitive way to generate Amazon content without using the command line.

**Features:**
- 📤 Drag-and-drop XLSX file upload
- 🎨 Modern gradient UI with responsive design
- ⚙️ Visual parameter configuration
- 📊 Real-time content generation
- 🔍 Comprehensive result display
- 💾 One-click JSON download
- ✅ Form validation and error handling

### Setup

#### Prerequisites
- Node.js 20+ (recommended) or 16+
- npm 8+

#### Installation

```bash
# Install frontend dependencies
cd frontend
npm install
```

#### Running the Web Interface

**Terminal 1 - Backend API:**
```bash
# From project root
poetry run api-server
# Backend runs at http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
# From project root
cd frontend
npm run dev
# Frontend runs at http://localhost:5173
```

#### Upgrading Node.js (if needed)

If you have Node.js 16 or earlier:

```bash
# Using Homebrew (macOS)
brew install node

# Or using NVM
nvm install --lts
nvm use --lts
```

### Using the Web Interface

1. **Open Browser**: Navigate to http://localhost:5173

2. **Upload Files**:
   - Click to select or drag-and-drop `seller_elf.xlsx`
   - Click to select or drag-and-drop `sif.xlsx`

3. **Configure Parameters**:
   - **Brand Name**: Your brand (e.g., "Amazing Cosy")
   - **Product Type**: Product category (required, e.g., "Women's Slippers")
   - **Top N Keywords**: Number of keywords to use (default: 50)
   - **AI Model**: Select from available Gemini models

4. **Generate Content**: Click "Generate Content" button

5. **View Results**: Browse through organized sections:
   - Market Research
   - 3 Title Variations
   - Bullet Points (2 versions)
   - Product Description
   - Search Keywords
   - Quality Check Scores
   - SEO Rationale

6. **Download**: Click "Download JSON" to save results

### API Documentation

The backend provides:
- **Endpoint**: `POST /generate`
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Frontend Development

```bash
# Start development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

### Troubleshooting Web Interface

**Backend won't start:**
- Check `.env` file has `GOOGLE_API_KEY`
- Verify port 8000 is not in use
- Run `poetry install` to ensure dependencies are installed

**Frontend won't start:**
- Check Node.js version: `node --version` (need 20+)
- Delete `node_modules` and `package-lock.json`, then run `npm install`
- Verify port 5173 is available

**Can't connect to backend:**
- Ensure backend is running on http://localhost:8000
- Check browser console for CORS errors
- Verify firewall isn't blocking connections

**File upload fails:**
- Ensure files are valid XLSX format
- Check file sizes aren't too large
- Verify files aren't corrupted

---

## Single Agent Usage

### Basic Command

```bash
poetry run python3 single_agent_main.py \
  --seller-elf data/seller_elf.xlsx \
  --sif data/sif.xlsx \
  --brand-name "Amazing Cosy" \
  --product-type "Women's Slippers" \
  --top-n 30 \
  --model gemini-2.5-flash-lite
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--seller-elf` | Path to seller_elf.xlsx file | `data/seller_elf.xlsx` |
| `--sif` | Path to sif.xlsx file | `data/sif.xlsx` |
| `--brand-name` | Your brand name | `"Amazing Cosy"` |
| `--product-type` | Product category | `"Women's Slippers"` |
| `--top-n` | Number of top keywords to use | `50` |
| `--output` | Output JSON file path | `output/single_agent_output.json` |
| `--model` | Gemini model to use | `gemini-2.5-flash-lite` |

### Recommended Models

1. **gemini-2.5-flash-lite** - Best balance (speed + cost) ⭐ Default
2. **gemini-1.5-flash** - Reliable, good limits
3. **gemini-2.0-flash-exp** - Experimental, may hit limits

### Example Output Summary

```
✓ Content generation completed!
  - Titles: 3
  - Bullet points: 2 sets of 5 (10 total)
  - Description: 1847 characters
  - Keywords: 22 terms
  - Quality status: PASS

QUALITY CHECK: PASS
  Grammar: 10/10
  Brand Compliance: 10/10
  Amazon Guidelines: 10/10
  Keyword Optimization: 10/10
  Content Quality: 10/10

RECOMMENDATIONS:
  Recommended Title: version_1
  Recommended Bullets: version_1
```

---

## Multi-Agent Pipeline

> ⚠️ **Work In Progress:** This multi-agent pipeline is currently under development and may not be fully functional. Please use the [Single Agent System](#single-agent-usage) for production workloads.

### Run the Pipeline

```bash
poetry run python3 main.py \
  --keywords data/keywords.csv \
  --sellergenie data/sellergenie.csv \
  --sif data/sif.csv \
  --model gemini-2.0-flash-exp
```

### Agent Details

#### 1. DataIngestionAgent
- Processes XLSX files using XlsxProcessorTool
- Filters top N keywords by relevance
- Structures data for downstream agents

#### 2. TitleAgent
- Generates 3 optimized title variations
- Maximum 200 characters each
- Incorporates brand + product type + keywords

#### 3. BulletPointAgent
- Creates 2 versions of 5 bullet points
- **Strict requirement:** 150-200 characters per bullet
- Version 1: Feature-focused
- Version 2: Benefit-focused

#### 4. DescriptionAgent
- Writes persuasive product description (1500-1950 chars)
- Generates search keywords (≤250 chars total)
- Emotionally engaging, conversion-focused

#### 5. QualityCheckAgent
- Validates grammar, spelling, readability
- Checks Amazon guidelines compliance
- Verifies keyword optimization
- Provides 0-10 scores per category

#### 6. ArgumentationAgent
- Explains SEO strategy
- Provides competitive positioning analysis
- Recommends best title/bullet versions
- Offers optimization suggestions

---

## XLSX Data Processing

### XlsxProcessorTool Features

The tool automatically processes and cleans your data:

**seller_elf.xlsx:**
- ✅ Filters out null keywords
- ✅ Converts columns to proper numeric types
- ✅ Sorts by monthly search volume (descending)
- ✅ Cleans ASIN lists
- ✅ Normalizes percentage columns

**sif.xlsx:**
- ✅ Auto-detects header row (row 1)
- ✅ Converts percentages: `'3.45%'` → `0.0345`
- ✅ Sorts by weekly search volume
- ✅ Filters invalid rows

### Input File Requirements

Your XLSX files should contain:

**seller_elf.xlsx** (keyword metrics):
- `关键词` (keyword)
- `月搜索量` (monthly search volume)
- `月购买量` (monthly purchases)
- `购买率` (purchase rate)
- `前十ASIN` (top 10 ASINs)

**sif.xlsx** (search intelligence):
- `关键词` (keyword)
- `周搜索量` (weekly search volume)
- `在售商品数` (products count)
- `周搜索量排名` (search rank)
- ASIN columns (percentage data)

### Programmatic Usage

```python
from src.tools.xlsx_processor_tool import xlsx_processor_tool

# Read as markdown for LLM
markdown = xlsx_processor_tool(
    file_path='data/seller_elf.xlsx',
    format='markdown',
    max_rows=50,
    preprocess=True
)

# Read as JSON for API
json_data = xlsx_processor_tool(
    file_path='data/sif.xlsx',
    format='json',
    format_type='sif',
    max_rows=100
)

# Read multiple files
combined = xlsx_processor_tool.read_multiple_files(
    file_configs=[
        {'file_path': 'data/seller_elf.xlsx', 'format_type': 'seller_elf'},
        {'file_path': 'data/sif.xlsx', 'format_type': 'sif'}
    ],
    format='markdown'
)
```

---

## Output Format

### JSON Structure

```json
{
  "titles": [
    "Title variation 1",
    "Title variation 2",
    "Title variation 3"
  ],
  "bullet_points_version_1": [
    "FEATURE 1: Description with benefits and details (150-200 chars)",
    "FEATURE 2: Description with benefits and details (150-200 chars)",
    "FEATURE 3: Description with benefits and details (150-200 chars)",
    "FEATURE 4: Description with benefits and details (150-200 chars)",
    "FEATURE 5: Description with benefits and details (150-200 chars)"
  ],
  "bullet_points_version_2": [
    "BENEFIT 1: Emotional appeal and value proposition (150-200 chars)",
    "BENEFIT 2: Emotional appeal and value proposition (150-200 chars)",
    "BENEFIT 3: Emotional appeal and value proposition (150-200 chars)",
    "BENEFIT 4: Emotional appeal and value proposition (150-200 chars)",
    "BENEFIT 5: Emotional appeal and value proposition (150-200 chars)"
  ],
  "product_description": "Compelling 1500-1950 character description...",
  "search_keywords": "keyword1, keyword2, keyword3 (≤250 chars total)",
  "quality_check_results": {
    "overall_status": "PASS",
    "grammar_score": 10,
    "brand_compliance_score": 10,
    "amazon_guidelines_score": 10,
    "keyword_optimization_score": 10,
    "content_quality_score": 10,
    "issues": [],
    "recommendations": []
  },
  "rationale": {
    "seo_strategy": "Strategy explanation...",
    "keyword_usage": "Keyword integration analysis...",
    "competitive_positioning": "Competitive analysis...",
    "recommended_title": "version_1",
    "recommended_bullets": "version_1",
    "optimization_notes": "Additional recommendations..."
  },
  "market_research": {
    "brand_name": "Your Brand",
    "product_type": "Product Type",
    "competitor_brands": ["Brand1", "Brand2"],
    "core_keywords": ["keyword1", "keyword2", ...],
    "competitor_titles": [...],
    "five_points_requirements": [...],
    "metadata": {...}
  },
  "metadata": {
    "generated_at": "2025-12-02T...",
    "duration_seconds": 11.48,
    "model": "gemini-2.5-flash-lite"
  }
}
```

---

## Requirements & Guidelines

### Content Requirements

#### Titles (3 variations)
- ✅ Maximum 200 characters each
- ✅ Include: Brand + Product Type + Key Features + Keywords
- ✅ Each variation emphasizes different keyword combinations

#### Bullet Points (2 versions × 5 bullets)
- ✅ **STRICT: 150-200 characters per bullet** (aim for 170-190)
- ✅ Start with benefit/feature in CAPS
- ✅ Include supporting details and specific benefits
- ✅ Version 1: Feature-focused with specifications
- ✅ Version 2: Benefit-focused with emotional appeal

#### Product Description
- ✅ **STRICT: 1500-1950 characters** (NOT more, NOT less)
- ✅ Highly persuasive and conversion-focused
- ✅ Emotionally engaging narrative
- ✅ Addresses customer pain points
- ✅ Strong call-to-action

#### Search Keywords
- ✅ **STRICT: ≤250 characters total** (including commas)
- ✅ 15-25 keywords/phrases
- ✅ Short keywords (2-3 words max per phrase)
- ✅ No brand names (except genericized terms like "ugg")
- ✅ No spelling mistakes
- ✅ **CRITICAL:** No repetition of words from bullets/description

### Quality Standards

All content must:
- ✅ Perfect grammar and spelling
- ✅ Consistent brand name usage
- ✅ Amazon guidelines compliant (no promotional language)
- ✅ Natural keyword integration (no stuffing)
- ✅ Professional tone and readability

---

## Troubleshooting

### API Quota Exceeded (429 Error)

**Error:** `RESOURCE_EXHAUSTED`

**Solutions:**
1. **Wait 60 seconds** and retry
2. **Use different model:** `gemini-2.5-flash-lite` or `gemini-1.5-flash`
3. **Reduce keywords:** Use `--top-n 20` instead of 50
4. **Upgrade plan:** Visit https://ai.google.dev/pricing

### Missing API Key

**Error:** `GOOGLE_API_KEY not found`

**Fix:**
1. Create `.env` file: `cp .env.example .env`
2. Add your key: `GOOGLE_API_KEY=AIzaSyD...your_key`
3. Get key from: https://aistudio.google.com/app/apikey

### File Not Found

**Error:** `seller_elf.xlsx not found`

**Fix:**
```bash
# Check files exist
ls -la data/seller_elf.xlsx data/sif.xlsx

# Or specify custom path
poetry run python3 single_agent_main.py \
  --seller-elf /path/to/your/file.xlsx
```

### Content Not Meeting Requirements

**Issue:** Bullets too short, description too long, etc.

**Cause:** AI didn't follow strict requirements

**Fix:** The prompt has been updated with STRICT requirements and self-validation. Regenerate content:
```bash
poetry run python3 single_agent_main.py --model gemini-2.5-flash-lite --top-n 30
```

---

## Development

### Project Structure

```
amazon-seller-assistant/
├── src/
│   ├── agents/
│   │   ├── single_content_agent.py    # Single agent system
│   │   ├── data_ingestion_agent.py    # Multi-agent: Step 1
│   │   ├── title_agent.py             # Multi-agent: Step 2
│   │   ├── bullet_point_agent.py      # Multi-agent: Step 3
│   │   ├── description_agent.py       # Multi-agent: Step 4
│   │   ├── quality_check_agent.py     # Multi-agent: Step 5
│   │   ├── argumentation_agent.py     # Multi-agent: Step 6
│   │   └── orchestrator.py            # Pipeline coordinator
│   ├── tools/
│   │   └── xlsx_processor_tool.py     # Data processing
│   └── config/
│       └── settings.py                # Configuration
├── frontend/                           # React web interface
│   ├── src/
│   │   ├── App.jsx                    # Main React component
│   │   ├── App.css                    # Application styles
│   │   └── main.jsx                   # Entry point
│   ├── package.json                   # Frontend dependencies
│   └── README.md                      # Frontend documentation
├── data/                               # Input XLSX files
├── output/                             # Generated content
├── tests/                              # Test suite
├── api_server.py                      # FastAPI backend server
├── single_agent_main.py               # Single agent CLI
├── main.py                            # Multi-agent CLI
├── pyproject.toml                     # Poetry dependencies
└── README.md                          # This file
```

### Running Tests

```bash
# All tests
poetry run pytest tests/ -v

# XLSX processor tests
poetry run pytest tests/test_xlsx_processor_tool.py -v

# Translation tests
poetry run pytest tests/test_translation.py -v

# Specific test
poetry run pytest tests/test_xlsx_processor_tool.py::TestPreprocessing -v
```

### Adding Custom Processing

```python
# src/custom_processor.py
from src.tools.xlsx_processor_tool import xlsx_processor_tool

def process_custom_data(file_path):
    # Read and process
    data = xlsx_processor_tool(
        file_path=file_path,
        format='dict',
        max_rows=100,
        preprocess=True
    )

    # Custom logic
    filtered = [row for row in data if row['月搜索量'] > 10000]

    return filtered
```

---

## Performance Comparison

| Metric | Single Agent | Multi-Agent (WIP) |
|--------|--------------|-------------------|
| **API Calls** | 1 | 6 |
| **Execution Time** | 10-15 sec | 45-60 sec |
| **Token Usage** | ~5,000 | ~20,000 |
| **Cost** | $ | $$$$ |
| **Complexity** | Simple | Complex |
| **Debugging** | Moderate | Easy |
| **Modularity** | Low | High |
| **Status** | ✅ Production Ready | ⚠️ WIP |

**Recommendation:** Use the Single Agent system for all production use cases. The multi-agent pipeline is currently under development.

---

## Best Practices

### Data Preparation
1. ✅ Ensure XLSX files are clean and well-formatted
2. ✅ Use high-quality keyword research data
3. ✅ Verify competitor data is current

### Content Generation
1. ✅ Use `gemini-2.5-flash-lite` for best balance
2. ✅ Start with `--top-n 30` keywords
3. ✅ Review quality check results carefully
4. ✅ Test both bullet point versions

### Optimization
1. ✅ A/B test different title variations
2. ✅ Monitor keyword performance
3. ✅ Iterate based on quality feedback
4. ✅ Update keyword data regularly

---

## License

MIT License - See LICENSE file for details.

## Support

- **Issues:** https://github.com/MarioMZhang/amazon-seller-assistant/issues
- **Documentation:** See individual *_GUIDE.md files for detailed guides
- **API Docs:** https://ai.google.dev/gemini-api/docs

## Acknowledgments

Built with:
- [Google Gemini AI](https://ai.google.dev/) - AI content generation
- [Google ADK](https://ai.google.dev/adk) - Agent Development Kit
- [Poetry](https://python-poetry.org/) - Dependency management
- [pandas](https://pandas.pydata.org/) - Data processing

---

**Last Updated:** December 2025
**Version:** 1.0.0
