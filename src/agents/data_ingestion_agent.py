"""
DataIngestionAgent - Step 1 of the Amazon Content Generation Pipeline.

This agent is responsible for ingesting CSV files using XlsxProcessorTool
and structuring the data into INPUT_DATA for downstream agents.
"""

from google import genai
from google.genai import types


def create_data_ingestion_agent(model: str = "gemini-2.0-flash-exp") -> types.Agent:
    """
    Create the DataIngestionAgent (LlmAgent).

    This agent uses XlsxProcessorTool to process three CSV files and
    structure the data into the INPUT_DATA format required by the pipeline.

    Args:
        model: The model to use for the agent (default: gemini-2.0-flash-exp)

    Returns:
        Agent configured for data ingestion
    """

    system_instruction = """You are the DataIngestionAgent, responsible for the first step in the Amazon Content Generation Pipeline.

Your task is to:
1. Use the xlsx_processor_tool to process three CSV files
2. Extract and structure data into the INPUT_DATA format
3. Ensure all required fields are present and properly formatted
4. Return the structured data for downstream agents

The INPUT_DATA must contain:
- brand_name: The brand name of the product
- product_type: The type/category of the product
- competitor_brands: List of competitor brand names
- core_keywords: List of important keywords for SEO
- word_frequency: Dictionary mapping keywords to their frequency counts
- competitor_titles: List of competitor product titles
- five_points_requirements: List of 5 key product features/requirements

Always validate that the data is complete and properly structured before returning it.
"""

    # Note: Tools will be registered when creating the orchestrator agent
    # as ADK handles tool binding at the orchestrator level

    agent = genai.Agent(
        model=model,
        name="DataIngestionAgent",
        instructions=system_instruction
    )

    return agent
