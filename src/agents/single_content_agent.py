"""
Single Content Generation Agent

A unified agent that handles all content generation tasks in one comprehensive prompt:
- Data ingestion via XlsxProcessorTool
- Title generation (3 variations)
- Bullet point generation (2 sets of 5)
- Description and search keywords generation
- Quality validation
- SEO rationale and recommendations
"""

from google import genai
from typing import Dict, Any
import json
import os
from dotenv import load_dotenv

from src.tools.xlsx_processor_tool import xlsx_processor_tool

# Load environment variables
load_dotenv()


class SingleContentAgent:
    """
    Single unified agent for Amazon content generation.

    This agent replaces the 6-step sequential pipeline with a single
    comprehensive prompt that generates all required content at once.
    """

    def __init__(self, model: str = "gemini-2.5-flash-lite"):
        """
        Initialize the single content agent.

        Args:
            model: The model to use for content generation
        """
        self.model = model

        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found in environment variables. "
                "Please set it in your .env file or environment."
            )

        self.client = genai.Client(api_key=api_key)

        # Comprehensive system prompt
        self.system_prompt = """You are an expert Amazon content writer and SEO specialist optimizing for Amazon's A10 search algorithm. Generate content that maximizes search visibility and conversion.

OUTPUT FORMAT - Return ONLY valid JSON with this exact structure:

{
  "titles": ["Title 1", "Title 2", "Title 3"],
  "bullet_points_version_1": ["Bullet 1", "Bullet 2", "Bullet 3", "Bullet 4", "Bullet 5"],
  "bullet_points_version_2": ["Bullet 1", "Bullet 2", "Bullet 3", "Bullet 4", "Bullet 5"],
  "product_description": "Description text...",
  "search_keywords": "keyword1, keyword2, keyword3, ...",
  "quality_check_results": {
    "overall_status": "PASS or FAIL",
    "grammar_score": 10,
    "brand_compliance_score": 10,
    "amazon_guidelines_score": 10,
    "keyword_optimization_score": 10,
    "content_quality_score": 10,
    "issues": [],
    "recommendations": []
  },
  "rationale": {
    "seo_strategy": "SEO approach explanation",
    "keyword_usage": "Keyword integration analysis",
    "competitive_positioning": "Competitive comparison",
    "recommended_title": "version_1 or version_2 or version_3",
    "recommended_bullets": "version_1 or version_2",
    "optimization_notes": "Additional recommendations"
  }
}

AMAZON A10 SEO STRATEGY - Follow these 7 ranking factors:

1. KEYWORD RESEARCH & TARGETING:
   • Mix short-tail keywords (broad, high volume) with long-tail keywords (specific, high conversion)
   • Prioritize keywords by search volume and relevance from input data
   • Analyze competitor titles/listings to identify high-performing keyword patterns
   • Use natural variations of keywords throughout content (avoid exact repetition)

2. TITLE OPTIMIZATION:
   • Primary focus: Product type, brand name, and top-performing keywords
   • Keep concise (aim for 60-80 characters for best visibility, max 200 allowed)
   • Front-load most important keywords that customers actually search for
   • Example format: "Brand + Product Type + Key Attribute + Primary Keyword"

3. BULLET POINT OPTIMIZATION:
   • Start each bullet with 1-2 CAPITALIZED descriptive words
   • Keep concise: 100-150 characters per bullet for optimal readability
   • Focus on customer benefits and problem-solving, not just features
   • Include specific product details: materials, dimensions, colors, quantities, sizes
   • Address the five-point requirements from input data

4. DESCRIPTION OPTIMIZATION:
   • Length: 1500-1950 characters (strictly enforced)
   • Include comprehensive product details: materials, colors, sizes, dimensions, care instructions, warranty
   • Integrate secondary keywords naturally - NO keyword stuffing
   • Vary keyword usage (synonyms, related terms) for better ranking
   • Create persuasive narrative with emotional appeal and clear value proposition
   • Strong call-to-action to drive conversions

5. BACK-END SEARCH TERMS (Hidden Keywords):
   • These are the "search_keywords" field - not visible to customers but crucial for ranking
   • Maximum length: ≤250 characters (including commas/spaces)
   • Include synonyms, alternate spellings, and related terms NOT already in title/bullets/description
   • Prioritize high-value keywords that expand product discoverability
   • No brand names, no misspellings, no redundancy with visible content

6. CONTENT QUALITY FOR A10 ALGORITHM:
   • Write naturally for customers first, SEO second (algorithm detects stuffing)
   • Use fragments in bullets (full sentences unnecessary)
   • Capitalize first letter of each bullet point
   • Include specific, factual information that helps purchase decisions
   • Ensure all claims can be substantiated (Amazon compliance)

7. LISTING QUALITY SIGNALS:
   • Grammar and spelling perfection (impacts conversion rate and ranking)
   • Complete, accurate product information builds customer trust
   • Strategic keyword placement: most important in title > bullets > description > backend

GLOBAL RULES:
• CRITICAL BRAND RULE: ONLY use the brand name from input data - NEVER mention competitor brands in ANY content (titles, bullets, description, keywords)
• Competitor data is for market research context only, NOT for inclusion in generated content
• Avoid keyword stuffing - Amazon's algorithm penalizes this
• Follow Amazon guidelines - no promotional language, unsubstantiated claims

CONTENT REQUIREMENTS:

1. TITLES (3 variations):
   • Target length: 60-80 characters (optimal for visibility)
   • Maximum: 200 characters
   • Format: Brand + Product Type + Key Features + Primary Keywords
   • Each variation tests different high-value keyword combinations
   • Front-load most important search terms

2. BULLET POINTS (2 versions, 5 bullets each):
   • Length: 100-150 characters per bullet (optimal readability)
   • Start with CAPITALIZED 1-2 word benefit/feature descriptor
   • Include: materials, dimensions, colors, sizes, quantities, care instructions
   • Version 1: Feature-focused with detailed specifications
   • Version 2: Benefit-focused with customer value propositions

3. PRODUCT DESCRIPTION:
   • Character count: 1500-1950 (strictly enforced)
   • Comprehensive product details: materials, colors, sizes, dimensions, care, warranty
   • Natural secondary keyword integration with variations
   • Persuasive narrative addressing customer needs and pain points
   • Clear value proposition and strong call-to-action

4. BACK-END SEARCH KEYWORDS:
   • Total length: ≤250 characters (including commas/spaces)
   • 15-25 comma-separated keywords/phrases
   • Focus on synonyms and related terms NOT in visible content
   • Include both short-tail and long-tail variations
   • No spelling errors, no brand names, no exact duplicates from content

5. QUALITY CHECK - Validate and score (0-10 each):
   • Grammar, spelling, readability (impacts conversion rate)
   • Brand consistency (no competitor names anywhere)
   • Amazon A10 optimization (keyword variety, natural integration)
   • Character counts: titles (60-80 optimal), bullets (100-150), description (1500-1950), keywords (≤250)
   • Keyword strategy: short-tail + long-tail mix, natural variations
   • CRITICAL: Verify NO competitor brand names appear in titles, bullets, description, or keywords
   • Flag all issues and provide recommendations

6. RATIONALE:
   • Explain keyword targeting strategy (short-tail vs long-tail)
   • Justify which keywords placed in title vs bullets vs description vs backend
   • Competitive positioning against competitor listings
   • Recommended title and bullet version with A10 optimization reasoning
   • Conversion optimization insights

Return ONLY valid JSON - no explanatory text outside the JSON object."""

    def generate_content(
        self,
        file_seller_elf: str,
        file_sif: str,
        brand_name: str = "Amazing Cosy",
        product_type: str = "Women's Slippers",
        top_n: int = 50
    ) -> Dict[str, Any]:
        """
        Generate complete Amazon listing content from input files.

        Args:
            file_seller_elf: Path to seller_elf.xlsx file
            file_sif: Path to sif.xlsx file
            brand_name: Brand name for the product
            product_type: Product type/category
            top_n: Number of top keywords to use

        Returns:
            Dictionary containing all generated content
        """
        try:
            # Step 1: Process input files using XlsxProcessorTool
            print("Processing input files...")
            input_data = xlsx_processor_tool.process_input_files(
                file_seller_elf=file_seller_elf,
                file_sif=file_sif,
                brand_name=brand_name,
                product_type=product_type,
                top_n=top_n
            )
            print(f"✓ Input data processed: {input_data['brand_name']} - {input_data['product_type']}")
            print(f"  - Core keywords: {len(input_data['core_keywords'])}")
            print(f"  - Competitor brands: {len(input_data['competitor_brands'])}")

            # Step 2: Generate all content in one comprehensive prompt
            print("\nGenerating complete Amazon listing content...")

            user_prompt = f"""Generate complete Amazon product listing content based on the following input data:

INPUT_DATA:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

Generate all required content following the structure and requirements specified in your instructions.
Return ONLY a valid JSON object with all required fields."""

            # Call the model
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    {"role": "user", "parts": [{"text": self.system_prompt}]},
                    {"role": "user", "parts": [{"text": user_prompt}]}
                ],
                config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 8192,
                }
            )

            # Extract and parse JSON response
            result = self._extract_json(response.text)

            # Add market research data to result (excluding word_frequency to keep output clean)
            input_data_filtered = {k: v for k, v in input_data.items() if k != 'word_frequency'}
            result["market_research"] = input_data_filtered

            # Print summary
            print(f"\n✓ Content generation completed!")
            print(f"  - Titles: {len(result.get('titles', []))}")
            print(f"  - Bullet points: 2 sets of 5 ({len(result.get('bullet_points_version_1', [])) + len(result.get('bullet_points_version_2', []))} total)")
            print(f"  - Description: {len(result.get('product_description', ''))} characters")
            print(f"  - Keywords: {len(result.get('search_keywords', '').split(','))} terms")
            print(f"  - Quality status: {result.get('quality_check_results', {}).get('overall_status', 'N/A')}")

            return result

        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON from model response text.

        Args:
            text: Response text that may contain JSON

        Returns:
            Parsed JSON dictionary
        """
        # Remove markdown code blocks if present
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            # Try to find JSON object in text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass

            # If still failing, print the response for debugging
            print("\n!!! JSON Parse Error !!!")
            print("Response text:")
            print(text[:500])
            print("...")
            raise Exception(f"Failed to parse JSON from response: {str(e)}")


def create_single_content_agent(model: str = "gemini-2.5-flash-lite") -> SingleContentAgent:
    """
    Factory function to create a single content agent.

    Args:
        model: The model to use for content generation

    Returns:
        SingleContentAgent instance
    """
    return SingleContentAgent(model=model)
