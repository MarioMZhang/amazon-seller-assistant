#!/usr/bin/env python3
"""
Amazon Content Generation Pipeline - Main Entry Point

This script runs the complete 6-step sequential agent pipeline to generate
optimized Amazon product listings from CSV input files.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.orchestrator import create_orchestrator


def main():
    """Main function to run the Amazon Content Generation Pipeline."""

    parser = argparse.ArgumentParser(
        description="Amazon Content Generation Pipeline - Generate optimized product listings"
    )
    parser.add_argument(
        "--keywords",
        type=str,
        default="data/keywords.csv",
        help="Path to keywords CSV file (default: data/keywords.csv)"
    )
    parser.add_argument(
        "--sellergenie",
        type=str,
        default="data/sellergenie.csv",
        help="Path to sellergenie CSV file (default: data/sellergenie.csv)"
    )
    parser.add_argument(
        "--sif",
        type=str,
        default="data/sif.csv",
        help="Path to sif CSV file (default: data/sif.csv)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/content_output.json",
        help="Path to output JSON file (default: output/content_output.json)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-2.5-flash-lite",
        help="Model to use for agents (default: gemini-2.5-flash-lite)"
    )

    args = parser.parse_args()

    # Validate input files exist
    for file_path, file_name in [
        (args.keywords, "keywords"),
        (args.sellergenie, "sellergenie"),
        (args.sif, "sif")
    ]:
        if not os.path.exists(file_path):
            print(f"Error: {file_name} file not found: {file_path}")
            print(f"Please provide a valid path to the {file_name} CSV file.")
            sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Print banner
    print("="*60)
    print("Amazon Content Generation Pipeline")
    print("Sequential Multi-Agent System (ADK-Based)")
    print("="*60)
    print(f"Model: {args.model}")
    print(f"Input Files:")
    print(f"  - Keywords: {args.keywords}")
    print(f"  - Sellergenie: {args.sellergenie}")
    print(f"  - SIF: {args.sif}")
    print(f"Output: {args.output}")
    print("="*60)
    print()

    try:
        # Create orchestrator
        orchestrator = create_orchestrator(model=args.model)

        # Run pipeline
        start_time = datetime.now()
        result = orchestrator.process_files(
            file1_keywords=args.keywords,
            file2_sellergenie=args.sellergenie,
            file3_sif=args.sif
        )
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Add metadata
        result["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "duration_seconds": duration,
            "model": args.model,
            "input_files": {
                "keywords": args.keywords,
                "sellergenie": args.sellergenie,
                "sif": args.sif
            }
        }

        # Save output
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Output saved to: {args.output}")
        print(f"✓ Total execution time: {duration:.2f} seconds")

        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Brand: {result['input_data']['brand_name']}")
        print(f"Product: {result['input_data']['product_type']}")
        print(f"Titles Generated: {len(result.get('titles', []))}")
        print(f"Bullet Sets: 2 (10 total bullet points)")
        print(f"Description Length: {len(result.get('product_description', ''))} characters")
        print(f"Search Keywords: {len(result.get('search_keywords', '').split(','))} terms")

        quality_results = result.get('quality_check_results', {})
        print(f"\nQuality Check: {quality_results.get('overall_status', 'N/A')}")
        if quality_results:
            print(f"  - Grammar: {quality_results.get('grammar_score', 'N/A')}/10")
            print(f"  - Brand Compliance: {quality_results.get('brand_compliance_score', 'N/A')}/10")
            print(f"  - Amazon Guidelines: {quality_results.get('amazon_guidelines_score', 'N/A')}/10")
            print(f"  - Keyword Optimization: {quality_results.get('keyword_optimization_score', 'N/A')}/10")
            print(f"  - Content Quality: {quality_results.get('content_quality_score', 'N/A')}/10")

        rationale = result.get('rationale', {})
        if rationale:
            print(f"\nRecommended Title: {rationale.get('recommended_title', 'N/A')[:50]}...")
            print(f"Recommended Bullets: {rationale.get('recommended_bullets', 'N/A')[:50]}...")

        print("="*60)
        print("\n✓ Pipeline completed successfully!")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
