"""
AmazonContentGeneratorAgent - Sequential Agent Orchestrator

This is the main orchestrator that manages the entire 6-step pipeline:
1. DataIngestionAgent
2. TitleAgent
3. BulletPointAgent
4. DescriptionAgent
5. QualityCheckAgent
6. ArgumentationAgent
"""

from google import genai
from google.genai import types
from typing import Dict, Any, List
import json

from src.agents.data_ingestion_agent import create_data_ingestion_agent
from src.agents.title_agent import create_title_agent
from src.agents.bullet_point_agent import create_bullet_point_agent
from src.agents.description_agent import create_description_agent
from src.agents.quality_check_agent import create_quality_check_agent
from src.agents.argumentation_agent import create_argumentation_agent
from src.tools.xlsx_processor_tool import xlsx_processor_tool


class AmazonContentGeneratorOrchestrator:
    """
    Orchestrator class for the Amazon Content Generation Pipeline.

    This class manages the sequential execution of all 6 agents,
    ensuring data flows correctly through the pipeline.
    """

    def __init__(self, model: str = "gemini-2.0-flash-exp"):
        """
        Initialize the orchestrator.

        Args:
            model: The model to use for all agents
        """
        self.model = model
        self.client = genai.Client()

        # Create all agents
        self.data_ingestion_agent = create_data_ingestion_agent(model)
        self.title_agent = create_title_agent(model)
        self.bullet_point_agent = create_bullet_point_agent(model)
        self.description_agent = create_description_agent(model)
        self.quality_check_agent = create_quality_check_agent(model)
        self.argumentation_agent = create_argumentation_agent(model)

    def process_files(
        self,
        file1_keywords: str,
        file2_sellergenie: str,
        file3_sif: str
    ) -> Dict[str, Any]:
        """
        Process CSV files through the entire pipeline.

        Args:
            file1_keywords: Path to keywords CSV file
            file2_sellergenie: Path to sellergenie CSV file
            file3_sif: Path to sif CSV file

        Returns:
            Dictionary containing all generated content and analysis
        """
        try:
            # Step 1: Data Ingestion
            print("Step 1/6: Processing input files...")
            input_data = xlsx_processor_tool.process_input_files(
                file1_keywords,
                file2_sellergenie,
                file3_sif
            )
            print(f"✓ Input data structured: {input_data['brand_name']} - {input_data['product_type']}")

            # Step 2: Generate Titles
            print("\nStep 2/6: Generating title variations...")
            titles_prompt = f"""Using the following input data, generate 3 optimized Amazon product titles:

INPUT_DATA:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

Generate exactly 3 title variations following the requirements in your instructions.
Return ONLY a valid JSON object with the 'titles' key containing an array of 3 strings.
"""
            title_response = self.client.models.generate_content(
                model=self.model,
                contents=titles_prompt
            )
            titles_data = self._extract_json(title_response.text)
            print(f"✓ Generated {len(titles_data.get('titles', []))} title variations")

            # Step 3: Generate Bullet Points
            print("\nStep 3/6: Generating bullet points...")
            bullets_prompt = f"""Using the following input data and generated titles, create 2 sets of 5 bullet points each:

INPUT_DATA:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

TITLES:
{json.dumps(titles_data, indent=2, ensure_ascii=False)}

Generate exactly 2 versions of bullet points (5 bullets each) following the requirements in your instructions.
Return ONLY a valid JSON object with 'bullet_points_version_1' and 'bullet_points_version_2' keys.
"""
            bullets_response = self.client.models.generate_content(
                model=self.model,
                contents=bullets_prompt
            )
            bullets_data = self._extract_json(bullets_response.text)
            print(f"✓ Generated 2 sets of bullet points (10 total)")

            # Step 4: Generate Description and Keywords
            print("\nStep 4/6: Generating product description and search keywords...")
            description_prompt = f"""Using all the following data, create a compelling product description and search keywords:

INPUT_DATA:
{json.dumps(input_data, indent=2, ensure_ascii=False)}

TITLES:
{json.dumps(titles_data, indent=2, ensure_ascii=False)}

BULLET POINTS:
{json.dumps(bullets_data, indent=2, ensure_ascii=False)}

Generate the product description and search keywords following the requirements in your instructions.
Return ONLY a valid JSON object with 'product_description' and 'search_keywords' keys.
"""
            description_response = self.client.models.generate_content(
                model=self.model,
                contents=description_prompt
            )
            description_data = self._extract_json(description_response.text)
            print(f"✓ Generated product description ({len(description_data.get('product_description', ''))} chars)")

            # Step 5: Quality Check
            print("\nStep 5/6: Performing quality validation...")
            all_content = {
                "INPUT_DATA": input_data,
                **titles_data,
                **bullets_data,
                **description_data
            }
            quality_prompt = f"""Perform a comprehensive quality check on all generated content:

{json.dumps(all_content, indent=2, ensure_ascii=False)}

Validate grammar, brand compliance, Amazon guidelines, keyword optimization, and content quality.
Return ONLY a valid JSON object with the 'quality_check_results' key following your instructions.
"""
            quality_response = self.client.models.generate_content(
                model=self.model,
                contents=quality_prompt
            )
            quality_data = self._extract_json(quality_response.text)
            status = quality_data.get('quality_check_results', {}).get('overall_status', 'UNKNOWN')
            print(f"✓ Quality check completed: {status}")

            # Step 6: Argumentation and Analysis
            print("\nStep 6/6: Generating SEO rationale and recommendations...")
            final_content = {
                **all_content,
                **quality_data
            }
            rationale_prompt = f"""Provide comprehensive SEO reasoning and strategic analysis for all generated content:

{json.dumps(final_content, indent=2, ensure_ascii=False)}

Analyze the SEO strategy, competitive positioning, and provide recommendations.
Return ONLY a valid JSON object with the 'rationale' key following your instructions.
"""
            rationale_response = self.client.models.generate_content(
                model=self.model,
                contents=rationale_prompt
            )
            rationale_data = self._extract_json(rationale_response.text)
            print(f"✓ SEO analysis and recommendations completed")

            # Combine all results
            final_output = {
                **titles_data,
                **bullets_data,
                **description_data,
                **quality_data,
                **rationale_data,
                "input_data": input_data
            }

            print("\n" + "="*60)
            print("Pipeline completed successfully!")
            print("="*60)

            return final_output

        except Exception as e:
            raise Exception(f"Error in pipeline execution: {str(e)}")

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
                return json.loads(text[start:end])
            raise Exception(f"Failed to parse JSON from response: {str(e)}")


def create_orchestrator(model: str = "gemini-2.0-flash-exp") -> AmazonContentGeneratorOrchestrator:
    """
    Factory function to create the orchestrator.

    Args:
        model: The model to use for all agents

    Returns:
        AmazonContentGeneratorOrchestrator instance
    """
    return AmazonContentGeneratorOrchestrator(model=model)
