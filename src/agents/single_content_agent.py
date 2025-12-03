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
        self.system_prompt = """You are an expert Amazon content writer and SEO specialist. Your task is to generate comprehensive, optimized Amazon product listing content based on keyword research data.

Given input data containing:
- Brand name and product type
- Competitor brands and titles
- Core keywords with frequency data
- Five-point product requirements

You must generate a complete JSON response with the following structure:

{
  "titles": [
    "Title variation 1",
    "Title variation 2",
    "Title variation 3"
  ],
  "bullet_points_version_1": [
    "Bullet point 1",
    "Bullet point 2",
    "Bullet point 3",
    "Bullet point 4",
    "Bullet point 5"
  ],
  "bullet_points_version_2": [
    "Bullet point 1",
    "Bullet point 2",
    "Bullet point 3",
    "Bullet point 4",
    "Bullet point 5"
  ],
  "product_description": "Comprehensive product description (1500-2000 words)",
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
    "seo_strategy": "Explanation of SEO approach",
    "keyword_usage": "Analysis of keyword integration",
    "competitive_positioning": "How content compares to competitors",
    "recommended_title": "version_1 or version_2 or version_3",
    "recommended_bullets": "version_1 or version_2",
    "optimization_notes": "Additional recommendations"
  }
}

REQUIREMENTS:

1. TITLES (3 variations):
   - Maximum 200 characters each
   - Include brand name, product type, and top keywords
   - Optimize for Amazon search algorithm
   - Follow format: Brand + Product Type + Key Features + Keywords
   - Each variation should emphasize different keyword combinations

2. BULLET POINTS (2 versions, 5 bullets each):
   - STRICT REQUIREMENT: Each bullet point MUST be between 150-200 characters (aim for 170-190 for optimal Amazon display)
   - Start with a benefit or feature in CAPS
   - Address the five-point requirements from input data
   - Integrate core keywords naturally
   - Add supporting details and specific benefits to reach the character requirement
   - Version 1: Feature-focused approach with detailed specifications
   - Version 2: Benefit-focused approach with emotional appeal and value propositions

3. PRODUCT DESCRIPTION:
   - STRICT REQUIREMENT: MUST be between 1500-1950 characters (NOT MORE than 1950, NOT LESS than 1500)
   - Highly persuasive and conversion-focused to encourage customers to buy
   - Engaging narrative format that connects emotionally with customers
   - Include brand story and product benefits
   - Integrate high-frequency keywords naturally
   - Address customer pain points and present solutions
   - Highlight unique selling points and value proposition
   - Include strong call-to-action
   - Be concise yet compelling - every sentence should drive value and conversion

4. SEARCH KEYWORDS:
   - STRICT REQUIREMENT: Total string length MUST be ≤250 characters (NOT more than 250!)
   - 15-25 keywords/phrases (reduced count to meet character limit)
   - Comma-separated list (commas and spaces count toward the 250 character limit)
   - Prioritize ONLY the highest-value keywords from input data that are NOT already heavily used
   - Focus on short, impactful keywords (2-3 words max per phrase)
   - STRICT REQUIREMENT: Avoid spelling mistakes
   - STRICT REQUIREMENT: Avoid including other brand names
   - CRITICAL: Avoid repeating keywords or word stems already prominent in bullets and product description
   - Choose complementary keywords that expand discoverability without redundancy 

5. QUALITY CHECK:
   - Validate all content for grammar, spelling, and readability
   - Ensure brand name consistency
   - Check Amazon guidelines compliance (no promotional language, no claims without substantiation)
   - Verify keyword optimization (natural integration, no stuffing)
   - Assess overall content quality
   - CRITICAL: Verify each bullet point is 150-200 characters (flag if any are outside this range)
   - CRITICAL: Verify product description is 1500-1950 characters (flag if outside this range)
   - CRITICAL: Verify search keywords total length is ≤250 characters (flag if over)
   - CRITICAL: Check for keyword repetition between search_keywords and bullets/description
   - Provide scores out of 10 for each category
   - List any issues or recommendations

6. RATIONALE:
   - Explain the SEO strategy and keyword selection
   - Justify content structure and approach
   - Provide competitive analysis insights
   - Recommend which title and bullet point version to use
   - Offer optimization notes for improvement

Return ONLY valid JSON. Do not include any explanatory text outside the JSON object."""

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
