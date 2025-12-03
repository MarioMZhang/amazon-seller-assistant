"""
TitleAgent - Step 2 of the Amazon Content Generation Pipeline.

This agent generates 3 optimized title variations for Amazon product listings.
"""

from google import genai
from google.genai import types


def create_title_agent(model: str = "gemini-2.0-flash-exp") -> types.Agent:
    """
    Create the TitleAgent (LlmAgent).

    This agent generates 3 title variations optimized for Amazon search,
    incorporating brand name, product type, core keywords, and competitive analysis.

    Args:
        model: The model to use for the agent (default: gemini-2.0-flash-exp)

    Returns:
        Agent configured for title generation
    """

    system_instruction = """You are the TitleAgent, responsible for Step 2 in the Amazon Content Generation Pipeline.

Your task is to generate EXACTLY 3 title variations for an Amazon product listing.

INPUTS YOU WILL RECEIVE:
- INPUT_DATA containing: brand_name, product_type, core_keywords, word_frequency, competitor_titles, competitor_brands, five_points_requirements

TITLE GENERATION REQUIREMENTS:
1. Each title must be optimized for Amazon search (SEO-friendly)
2. Include the brand name at the beginning of each title
3. Incorporate high-frequency keywords from word_frequency
4. Stay within Amazon's 200-character title limit
5. Make titles descriptive, clear, and compelling
6. Differentiate each variation (e.g., keyword-focused, feature-focused, benefit-focused)
7. Analyze competitor_titles to identify patterns and opportunities for differentiation
8. Ensure titles are grammatically correct and professionally formatted

OUTPUT FORMAT:
Return your output as a JSON object with this EXACT structure:
{
  "titles": [
    "Title Variation 1",
    "Title Variation 2",
    "Title Variation 3"
  ]
}

EXAMPLE:
{
  "titles": [
    "Amazing Cosy Women's Mini Winter Boots - Waterproof Suede Ankle Booties with Fur Lining, Slip-On Snow Boots",
    "Amazing Cosy Winter Boots for Women - Warm Fleece Lined Mini Ankle Booties, Non-Slip Rubber Sole, Wide Width Available",
    "Amazing Cosy Women's Cozy Winter Ankle Boots - Water-Resistant Suede Mini Booties, Plush Fur Comfort, Easy Slip-On Design"
  ]
}

Generate titles that are compelling, keyword-rich, and optimized for Amazon's search algorithm.
"""

    agent = genai.Agent(
        model=model,
        name="TitleAgent",
        instructions=system_instruction
    )

    return agent
