#!/usr/bin/env python3
"""
Single Agent Amazon Content Generator

A simplified entry point that uses a single unified agent instead of
the multi-agent sequential pipeline.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.single_content_agent import create_single_content_agent


def main():
    """Main function to run the single agent content generator."""

    parser = argparse.ArgumentParser(
        description="Single Agent Amazon Content Generator - Generate optimized product listings"
    )
    parser.add_argument(
        "--seller-elf",
        type=str,
        default="data/seller_elf.xlsx",
        help="Path to seller_elf.xlsx file (default: data/seller_elf.xlsx)"
    )
    parser.add_argument(
        "--sif",
        type=str,
        default="data/sif.xlsx",
        help="Path to sif.xlsx file (default: data/sif.xlsx)"
    )
    parser.add_argument(
        "--brand-name",
        type=str,
        default="Amazing Cosy",
        help="Brand name (default: Amazing Cosy)"
    )
    parser.add_argument(
        "--product-type",
        type=str,
        default="Women's Slippers",
        help="Product type (default: Women's Slippers)"
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=50,
        help="Number of top keywords to use (default: 50)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/single_agent_output.json",
        help="Path to output JSON file (default: output/single_agent_output.json)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-2.5-flash-lite",
        help="Model to use (default: gemini-2.5-flash-lite)"
    )

    args = parser.parse_args()

    # Validate input files exist
    for file_path, file_name in [
        (args.seller_elf, "seller_elf"),
        (args.sif, "sif")
    ]:
        if not os.path.exists(file_path):
            print(f"Error: {file_name} file not found: {file_path}")
            print(f"Please provide a valid path to the {file_name} XLSX file.")
            sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Print banner
    print("="*70)
    print("Single Agent Amazon Content Generator")
    print("="*70)
    print(f"Model: {args.model}")
    print(f"Brand: {args.brand_name}")
    print(f"Product: {args.product_type}")
    print(f"Top Keywords: {args.top_n}")
    print(f"\nInput Files:")
    print(f"  - Seller ELF: {args.seller_elf}")
    print(f"  - SIF: {args.sif}")
    print(f"\nOutput: {args.output}")
    print("="*70)
    print()

    try:
        # Create agent
        agent = create_single_content_agent(model=args.model)

        # Generate content
        start_time = datetime.now()
        result = agent.generate_content(
            file_seller_elf=args.seller_elf,
            file_sif=args.sif,
            brand_name=args.brand_name,
            product_type=args.product_type,
            top_n=args.top_n
        )
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Add metadata
        result["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "duration_seconds": duration,
            "model": args.model,
            "input_files": {
                "seller_elf": args.seller_elf,
                "sif": args.sif
            },
            "parameters": {
                "brand_name": args.brand_name,
                "product_type": args.product_type,
                "top_n": args.top_n
            }
        }

        # Save output
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Output saved to: {args.output}")
        print(f"✓ Total execution time: {duration:.2f} seconds")

        # Print detailed summary
        print("\n" + "="*70)
        print("CONTENT SUMMARY")
        print("="*70)

        # Market research summary
        print(f"\nMARKET RESEARCH:")
        print(f"  Brand: {result['market_research']['brand_name']}")
        print(f"  Product: {result['market_research']['product_type']}")
        print(f"  Core Keywords: {len(result['market_research']['core_keywords'])}")
        print(f"  Competitor Brands: {', '.join(result['market_research']['competitor_brands'][:3])}")

        # Titles
        print(f"\nTITLES GENERATED: {len(result.get('titles', []))}")
        for i, title in enumerate(result.get('titles', []), 1):
            print(f"  {i}. {title[:80]}{'...' if len(title) > 80 else ''}")

        # Bullet points
        print(f"\nBULLET POINTS:")
        print(f"  Version 1: {len(result.get('bullet_points_version_1', []))} bullets")
        for i, bullet in enumerate(result.get('bullet_points_version_1', [])[:3], 1):
            print(f"    {i}. {bullet[:70]}{'...' if len(bullet) > 70 else ''}")

        print(f"  Version 2: {len(result.get('bullet_points_version_2', []))} bullets")
        for i, bullet in enumerate(result.get('bullet_points_version_2', [])[:3], 1):
            print(f"    {i}. {bullet[:70]}{'...' if len(bullet) > 70 else ''}")

        # Description
        description = result.get('product_description', '')
        print(f"\nPRODUCT DESCRIPTION: {len(description)} characters")
        print(f"  Preview: {description[:150]}{'...' if len(description) > 150 else ''}")

        # Keywords
        keywords = result.get('search_keywords', '')
        keyword_list = [k.strip() for k in keywords.split(',')]
        print(f"\nSEARCH KEYWORDS: {len(keyword_list)} terms")
        print(f"  Top 10: {', '.join(keyword_list[:10])}")

        # Quality check
        quality = result.get('quality_check_results', {})
        print(f"\nQUALITY CHECK: {quality.get('overall_status', 'N/A')}")
        if quality:
            print(f"  Grammar: {quality.get('grammar_score', 'N/A')}/10")
            print(f"  Brand Compliance: {quality.get('brand_compliance_score', 'N/A')}/10")
            print(f"  Amazon Guidelines: {quality.get('amazon_guidelines_score', 'N/A')}/10")
            print(f"  Keyword Optimization: {quality.get('keyword_optimization_score', 'N/A')}/10")
            print(f"  Content Quality: {quality.get('content_quality_score', 'N/A')}/10")

            if quality.get('issues'):
                print(f"\n  Issues Found ({len(quality['issues'])}):")
                for issue in quality['issues'][:3]:
                    print(f"    - {issue}")

            if quality.get('recommendations'):
                print(f"\n  Recommendations ({len(quality['recommendations'])}):")
                for rec in quality['recommendations'][:3]:
                    print(f"    - {rec}")

        # Rationale
        rationale = result.get('rationale', {})
        if rationale:
            print(f"\nRECOMMENDATIONS:")
            print(f"  Recommended Title: {rationale.get('recommended_title', 'N/A')}")
            print(f"  Recommended Bullets: {rationale.get('recommended_bullets', 'N/A')}")
            print(f"\n  SEO Strategy: {rationale.get('seo_strategy', 'N/A')[:120]}{'...' if len(rationale.get('seo_strategy', '')) > 120 else ''}")

        print("\n" + "="*70)
        print("✓ Single agent content generation completed successfully!")
        print("="*70)

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
