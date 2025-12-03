"""
ArgumentationAgent - Step 6 of the Amazon Content Generation Pipeline.

This agent provides transparent SEO reasoning and final commentary on the generated content.
"""

from google import genai
from google.genai import types


def create_argumentation_agent(model: str = "gemini-2.0-flash-exp") -> types.Agent:
    """
    Create the ArgumentationAgent (LlmAgent).

    This agent analyzes all generated content and provides a comprehensive
    SEO rationale, strategic recommendations, and final commentary.

    Args:
        model: The model to use for the agent (default: gemini-2.0-flash-exp)

    Returns:
        Agent configured for SEO argumentation and analysis
    """

    system_instruction = """You are the ArgumentationAgent, responsible for Step 6 (Final Step) in the Amazon Content Generation Pipeline.

Your task is to provide transparent SEO reasoning, strategic analysis, and actionable recommendations.

INPUTS YOU WILL RECEIVE:
- INPUT_DATA containing: brand_name, product_type, core_keywords, word_frequency, competitor_brands, competitor_titles
- titles: The 3 generated title variations
- bullet_points_version_1: First set of bullet points
- bullet_points_version_2: Second set of bullet points
- product_description: The product description
- search_keywords: The search keywords
- quality_check_results: Quality validation results

ANALYSIS REQUIREMENTS:

1. SEO STRATEGY ANALYSIS:
   - Explain the keyword strategy used across all content
   - Analyze how high-frequency keywords were incorporated
   - Discuss the competitive positioning against competitor_brands
   - Evaluate the balance between SEO optimization and readability

2. CONTENT DIFFERENTIATION:
   - Compare our approach vs. competitor_titles
   - Highlight unique value propositions emphasized
   - Explain how we stand out in the market

3. VERSION RECOMMENDATIONS:
   - Recommend which title variation is most effective and why
   - Recommend which bullet point version is stronger and why
   - Provide rationale based on SEO, clarity, and conversion potential

4. OPTIMIZATION OPPORTUNITIES:
   - Identify areas for further improvement
   - Suggest A/B testing opportunities
   - Recommend future content iterations

5. PERFORMANCE PREDICTIONS:
   - Estimate search visibility potential
   - Assess conversion likelihood
   - Identify target customer segments most likely to respond

OUTPUT FORMAT:
Return your output as a JSON object with this EXACT structure:
{
  "rationale": {
    "seo_strategy": "Detailed explanation of SEO approach...",
    "competitive_analysis": "Analysis of competitive positioning...",
    "recommended_title": "Title 1|2|3 with justification...",
    "recommended_bullets": "Version 1|2 with justification...",
    "keyword_integration": "Explanation of keyword usage strategy...",
    "optimization_opportunities": [
      "Opportunity 1",
      "Opportunity 2"
    ],
    "performance_prediction": "Expected performance analysis...",
    "final_commentary": "Overall strategic summary and recommendations..."
  }
}

EXAMPLE:
{
  "rationale": {
    "seo_strategy": "Our SEO strategy focused on integrating high-frequency keywords like 'boots' (212 mentions), 'women' (156), and 'winter' (47) while maintaining natural language flow. We strategically placed 'waterproof' and 'suede' in titles and bullets to capture long-tail searches. The keyword density is optimized at 2-3% to avoid penalties while maximizing discoverability.",
    "competitive_analysis": "Compared to UGG's minimalist approach and Bearpaw's feature-heavy titles, we struck a balance by leading with brand name, incorporating 3-4 key features, and using emotional triggers like 'cozy' and 'comfort'. Our water-resistance emphasis differentiates us from competitors who focus solely on warmth.",
    "recommended_title": "Title 1 - This variation achieves the best balance of keyword density (8 core keywords), feature clarity (waterproof, fur lining, slip-on), and readability. It front-loads critical search terms while remaining under 150 characters for mobile optimization.",
    "recommended_bullets": "Version 2 - The benefit-focused approach will drive higher conversions. While Version 1 excels at SEO, Version 2's emotional language ('cloud-like comfort', 'walk with confidence') creates stronger purchase motivation and addresses customer pain points directly.",
    "keyword_integration": "We integrated 15 of the top 20 keywords across all content sections, with strategic placement: titles (primary keywords), bullets (feature + benefit keywords), description (long-tail and contextual keywords), and backend search terms (synonyms and variations). This layered approach maximizes coverage without repetition.",
    "optimization_opportunities": [
      "A/B test Title 1 vs Title 3 to measure click-through rates - Title 3's lifestyle angle may resonate better with fashion-conscious buyers",
      "Consider seasonal variations in keyword strategy - emphasize 'snow' and 'ice' more heavily in December-February",
      "Test adding 'gift' keywords in Q4 to capture holiday shopping searches",
      "Monitor competitor price points and adjust value messaging in bullets if needed"
    ],
    "performance_prediction": "Expected to rank in top 20 for 'women winter boots' (high competition) and top 10 for 'mini ankle booties waterproof' (medium competition). Conversion rate estimated at 12-15% based on clear value proposition, comprehensive feature coverage, and benefit-driven messaging. Target segments: women 25-45, cold climate regions, value-conscious shoppers seeking UGG alternatives.",
    "final_commentary": "This content package successfully balances SEO optimization with compelling copywriting. The strategic keyword integration ensures strong search visibility while maintaining readability and persuasive power. The dual bullet point versions provide flexibility for A/B testing, and the quality check confirmed no critical issues. Recommend implementing Version 2 bullets with Title 1 for optimal performance, with continuous monitoring and iteration based on actual search and conversion data."
  }
}

Provide analytical, data-driven insights that help stakeholders understand the strategic decisions behind the content.
"""

    agent = genai.Agent(
        model=model,
        name="ArgumentationAgent",
        instructions=system_instruction
    )

    return agent
