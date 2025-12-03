"""
Configuration settings for the Amazon Content Generation Pipeline.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Model Configuration
DEFAULT_MODEL = os.getenv("MODEL", "gemini-2.5-flash-lite")

# Agent Configuration
AGENT_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# Content Generation Limits
TITLE_MAX_LENGTH = 200
BULLET_POINT_OPTIMAL_LENGTH = (150, 200)
DESCRIPTION_OPTIMAL_LENGTH = (1500, 2000)
MAX_KEYWORDS = 30

# Quality Check Thresholds
QUALITY_PASS_THRESHOLD = 7
QUALITY_SCORES = {
    "excellent": (9, 10),
    "good": (7, 8),
    "acceptable": (5, 6),
    "poor": (3, 4),
    "unacceptable": (0, 2)
}

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
