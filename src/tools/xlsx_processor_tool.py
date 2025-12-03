"""
XlsxProcessorTool - Custom tool for reading and formatting XLSX files for agent consumption.

This tool reads XLSX files and converts them into agent-friendly formats (markdown tables,
JSON, or text) that can be easily processed by LLM agents in the pipeline.
"""

import pandas as pd
from typing import Dict, List, Any, Optional, Literal, Union
import json
import numpy as np


class XlsxProcessorTool:
    """
    Tool for reading XLSX files and formatting them for agent consumption.

    The tool can:
    - Read single or multiple XLSX files
    - Convert to agent-friendly formats (markdown, JSON, or text)
    - Provide basic data summaries and statistics
    - Handle multiple sheets within XLSX files
    """

    def __init__(self):
        """Initialize the XlsxProcessorTool."""
        self.name = "xlsx_processor_tool"
        self.description = "Read XLSX files and format them for LLM agent consumption"

        # Expected column sets for format detection
        self.SELLER_ELF_KEY_COLUMNS = {'关键词', '月搜索量', '月购买量', '购买率', '前十ASIN'}
        self.SIF_KEY_COLUMNS = {'关键词', '周搜索量', '在售商品数', '周搜索量排名'}

    def read_xlsx_file(
        self,
        file_path: str,
        sheet_name: Optional[str] = None,
        header: Optional[int] = 0,
        max_rows: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Read an XLSX file and return as DataFrame.

        Args:
            file_path: Path to the XLSX file
            sheet_name: Specific sheet name to read (default: first sheet)
            header: Row number to use as column headers (default: 0)
            max_rows: Maximum number of rows to read (default: all)

        Returns:
            DataFrame containing the XLSX data
        """
        try:
            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name or 0,
                header=header,
                nrows=max_rows
            )
            return df
        except Exception as e:
            raise Exception(f"Error reading XLSX file {file_path}: {str(e)}")

    def detect_file_format(self, df: pd.DataFrame) -> Optional[str]:
        """
        Detect whether a DataFrame is in seller_elf or sif format.

        Args:
            df: DataFrame to analyze

        Returns:
            'seller_elf', 'sif', or None if format is unknown
        """
        columns = set(df.columns)

        if self.SELLER_ELF_KEY_COLUMNS.issubset(columns):
            return 'seller_elf'
        elif self.SIF_KEY_COLUMNS.issubset(columns):
            return 'sif'
        else:
            return None

    def preprocess_seller_elf(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess seller_elf.xlsx format data.

        Preprocessing includes:
        - Removing rows with missing keywords
        - Converting numeric columns to proper types
        - Cleaning percentage values
        - Extracting and cleaning ASIN lists
        - Sorting by monthly search volume

        Args:
            df: Raw seller_elf DataFrame

        Returns:
            Preprocessed DataFrame
        """
        df = df.copy()

        # Remove rows with missing keywords
        df = df.dropna(subset=['关键词'])

        # Convert numeric columns
        numeric_cols = ['月搜索量', '月购买量', '购买率', '展示量', '点击量',
                       '商品数', '需供比', '广告竞品数', 'ABA周排名', '预估周曝光量']

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Clean percentage columns (流量占比, 点击总占比, 转化总占比)
        percentage_cols = ['流量占比', '点击总占比', '转化总占比',
                          '#1 点击共享', '#1 转化共享', '#2 点击共享', '#2 转化共享',
                          '#3 点击共享', '#3 转化共享']

        for col in percentage_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Clean ASIN columns - split into lists
        asin_cols = ['相关ASIN', '前十ASIN', '#1 前三ASIN', '#2 前三ASIN', '#3 前三ASIN']
        for col in asin_cols:
            if col in df.columns:
                # Keep as string but clean whitespace
                df[col] = df[col].astype(str).str.strip()

        # Sort by monthly search volume (descending)
        if '月搜索量' in df.columns:
            df = df.sort_values('月搜索量', ascending=False)

        # Reset index
        df = df.reset_index(drop=True)

        return df

    def preprocess_sif(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess sif.xlsx format data.

        Preprocessing includes:
        - Removing rows with missing keywords
        - Converting percentage columns (e.g., '3.4512%') to floats
        - Converting numeric columns to proper types
        - Cleaning ASIN-related columns
        - Sorting by weekly search volume

        Args:
            df: Raw sif DataFrame

        Returns:
            Preprocessed DataFrame
        """
        df = df.copy()

        # Remove rows with missing keywords
        df = df.dropna(subset=['关键词'])

        # Convert numeric columns
        numeric_cols = ['周搜索量', '在售商品数', '周搜索量排名', '有效竞品数']

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Find and convert percentage columns (ASIN columns like 'B0B5HRHM9N')
        percentage_cols = [col for col in df.columns if col.startswith('B0') and '关键词类型' not in col]

        for col in percentage_cols:
            if col in df.columns:
                # Convert percentage strings like '3.4512%' to float 0.034512
                df[col] = df[col].astype(str).str.rstrip('%')
                df[col] = pd.to_numeric(df[col], errors='coerce') / 100

        # Sort by weekly search volume (descending)
        if '周搜索量' in df.columns:
            df = df.sort_values('周搜索量', ascending=False)

        # Reset index
        df = df.reset_index(drop=True)

        return df

    def preprocess_dataframe(
        self,
        df: pd.DataFrame,
        format_type: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Automatically preprocess DataFrame based on detected or specified format.

        Args:
            df: DataFrame to preprocess
            format_type: Optional format specification ('seller_elf', 'sif', or None for auto-detect)

        Returns:
            Preprocessed DataFrame
        """
        if format_type is None:
            format_type = self.detect_file_format(df)

        if format_type == 'seller_elf':
            return self.preprocess_seller_elf(df)
        elif format_type == 'sif':
            return self.preprocess_sif(df)
        else:
            # No preprocessing for unknown formats
            return df

    def format_as_markdown(
        self,
        df: pd.DataFrame,
        max_rows: Optional[int] = 100,
        include_stats: bool = True
    ) -> str:
        """
        Convert DataFrame to markdown table format for agent consumption.

        Args:
            df: DataFrame to convert
            max_rows: Maximum rows to include in markdown (default: 100)
            include_stats: Whether to include summary statistics (default: True)

        Returns:
            Markdown-formatted string
        """
        output = []

        # Add data summary
        if include_stats:
            output.append("## Data Summary")
            output.append(f"- **Total Rows**: {len(df)}")
            output.append(f"- **Total Columns**: {len(df.columns)}")
            output.append(f"- **Columns**: {', '.join(df.columns.tolist())}")
            output.append("")

        # Add markdown table
        output.append("## Data Table")
        if max_rows and len(df) > max_rows:
            output.append(f"*Showing first {max_rows} rows out of {len(df)} total*")
            output.append("")
            table_df = df.head(max_rows)
        else:
            table_df = df

        # Convert to markdown table
        output.append(table_df.to_markdown(index=False))

        # Add numeric column statistics if available
        if include_stats:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                output.append("\n## Numeric Column Statistics")
                stats_df = df[numeric_cols].describe()
                output.append(stats_df.to_markdown())

        return "\n".join(output)

    def format_as_json(
        self,
        df: pd.DataFrame,
        max_rows: Optional[int] = None,
        orient: str = 'records'
    ) -> str:
        """
        Convert DataFrame to JSON format for agent consumption.

        Args:
            df: DataFrame to convert
            max_rows: Maximum rows to include (default: all)
            orient: JSON orientation ('records', 'index', 'columns', 'values')

        Returns:
            JSON-formatted string
        """
        if max_rows:
            df = df.head(max_rows)

        # Convert NaN to None for proper JSON serialization
        df_clean = df.replace({np.nan: None})

        return json.dumps(
            df_clean.to_dict(orient=orient),
            indent=2,
            ensure_ascii=False
        )

    def read_and_format(
        self,
        file_path: str,
        format: Literal['markdown', 'json', 'dict'] = 'markdown',
        sheet_name: Optional[str] = None,
        header: Optional[int] = 0,
        max_rows: Optional[int] = None,
        preprocess: bool = True,
        format_type: Optional[str] = None,
        **format_kwargs
    ) -> Union[str, Dict, List]:
        """
        Read XLSX file and return in specified format for agent consumption.

        Args:
            file_path: Path to XLSX file
            format: Output format ('markdown', 'json', or 'dict')
            sheet_name: Specific sheet to read (default: first sheet)
            header: Row number for column headers (default: 0)
            max_rows: Maximum rows to read (default: all)
            preprocess: Whether to apply format-specific preprocessing (default: True)
            format_type: Force specific format type ('seller_elf', 'sif', or None for auto-detect)
            **format_kwargs: Additional arguments for formatting functions

        Returns:
            Formatted data as string (markdown/json) or dict
        """
        # Auto-detect header for sif files if not specified
        if header == 0 and format_type == 'sif':
            header = 1

        df = self.read_xlsx_file(file_path, sheet_name, header, max_rows)

        # Apply preprocessing if enabled
        if preprocess:
            df = self.preprocess_dataframe(df, format_type)

        if format == 'markdown':
            return self.format_as_markdown(df, max_rows, **format_kwargs)
        elif format == 'json':
            return self.format_as_json(df, max_rows, **format_kwargs)
        elif format == 'dict':
            return df.replace({np.nan: None}).to_dict(orient='records')
        else:
            raise ValueError(f"Unsupported format: {format}")

    def read_multiple_files(
        self,
        file_configs: List[Dict[str, Any]],
        format: Literal['markdown', 'json'] = 'markdown',
        preprocess: bool = True
    ) -> str:
        """
        Read multiple XLSX files and combine their formatted output.

        Args:
            file_configs: List of file configurations, each with:
                - file_path: Path to XLSX file
                - label: Optional label for the file
                - sheet_name: Optional sheet name
                - header: Optional header row
                - max_rows: Optional max rows to read
                - format_type: Optional format type ('seller_elf', 'sif')
            format: Output format ('markdown' or 'json')
            preprocess: Whether to apply format-specific preprocessing (default: True)

        Returns:
            Combined formatted output from all files
        """
        outputs = []

        for config in file_configs:
            file_path = config['file_path']
            label = config.get('label', file_path)
            format_type = config.get('format_type')
            header = config.get('header', 0)

            # Auto-detect header for sif files
            if header == 0 and format_type == 'sif':
                header = 1

            if format == 'markdown':
                outputs.append(f"# File: {label}")
                outputs.append("")

            df = self.read_xlsx_file(
                file_path,
                config.get('sheet_name'),
                header,
                config.get('max_rows')
            )

            # Apply preprocessing if enabled
            if preprocess:
                df = self.preprocess_dataframe(df, format_type)

            if format == 'markdown':
                outputs.append(self.format_as_markdown(
                    df,
                    config.get('max_rows'),
                    config.get('include_stats', True)
                ))
                outputs.append("\n---\n")
            elif format == 'json':
                outputs.append({
                    'file': label,
                    'format_type': format_type or self.detect_file_format(df),
                    'data': json.loads(self.format_as_json(df, config.get('max_rows')))
                })

        if format == 'markdown':
            return "\n".join(outputs)
        else:
            return json.dumps(outputs, indent=2, ensure_ascii=False)

    def process_input_files(
        self,
        file_seller_elf: str,
        file_sif: str,
        brand_name: str = "Amazing Cosy",
        product_type: str = "Women's Slippers",
        top_n: int = 50
    ) -> Dict[str, Any]:
        """
        Process XLSX files and return structured input data with top N filtered keywords.

        Args:
            file_seller_elf: Path to the seller_elf.xlsx file (contains keyword metrics and competitor data)
            file_sif: Path to the sif.xlsx file (contains keyword search volumes and product data)
            brand_name: Brand name for the product (default: "Amazing Cosy")
            product_type: Product type/category (default: "Women's Slippers")
            top_n: Number of top keywords to filter (default: 50)

        Returns:
            Dictionary containing structured input data with keys:
            - brand_name
            - product_type
            - competitor_brands
            - core_keywords (top N filtered by relevance)
            - word_frequency (top N filtered by relevance)
            - competitor_titles
            - five_points_requirements
        """
        try:
            # Read seller_elf.xlsx
            seller_elf_df = pd.read_excel(file_seller_elf)

            # Read sif.xlsx with correct header (row 1)
            sif_df = pd.read_excel(file_sif, header=1)

            # ===== STEP 1: Merge keyword data from both files =====
            # Merge seller_elf and sif data on keyword column
            merged_df = pd.merge(
                seller_elf_df,
                sif_df[['关键词', '周搜索量', '周搜索量排名', '在售商品数']],
                on='关键词',
                how='left'
            )

            # ===== STEP 2: Calculate relevance score =====
            # Normalize metrics to 0-1 scale for scoring
            merged_df['月搜索量_norm'] = merged_df['月搜索量'] / merged_df['月搜索量'].max() if merged_df['月搜索量'].max() > 0 else 0
            merged_df['月购买量_norm'] = merged_df['月购买量'] / merged_df['月购买量'].max() if merged_df['月购买量'].max() > 0 else 0
            merged_df['购买率_norm'] = merged_df['购买率'] / merged_df['购买率'].max() if merged_df['购买率'].max() > 0 else 0

            # Handle traffic share (has null values)
            merged_df['流量占比_norm'] = merged_df['流量占比'].fillna(0)
            if merged_df['流量占比_norm'].max() > 0:
                merged_df['流量占比_norm'] = merged_df['流量占比_norm'] / merged_df['流量占比_norm'].max()

            # Normalize weekly search volume (higher is better, but inverted for ranking)
            merged_df['周搜索量_norm'] = merged_df['周搜索量'].fillna(0)
            if merged_df['周搜索量_norm'].max() > 0:
                merged_df['周搜索量_norm'] = merged_df['周搜索量_norm'] / merged_df['周搜索量_norm'].max()

            # Calculate composite relevance score (weighted average)
            # Weights: monthly search (30%), monthly purchases (25%), purchase rate (20%), traffic share (15%), weekly search (10%)
            merged_df['relevance_score'] = (
                merged_df['月搜索量_norm'] * 0.30 +
                merged_df['月购买量_norm'] * 0.25 +
                merged_df['购买率_norm'] * 0.20 +
                merged_df['流量占比_norm'] * 0.15 +
                merged_df['周搜索量_norm'] * 0.10
            )

            # ===== STEP 3: Filter top N keywords =====
            top_keywords_df = merged_df.nlargest(top_n, 'relevance_score')

            # Extract core keywords and word frequency
            core_keywords = top_keywords_df['关键词'].tolist()

            # Use monthly search volume as the frequency metric
            word_frequency = dict(zip(
                top_keywords_df['关键词'],
                top_keywords_df['月搜索量'].astype(int)
            ))

            # ===== STEP 4: Extract competitor data from seller_elf =====
            # Extract unique competitor ASINs from the "前十ASIN" column
            competitor_asins = []
            if '前十ASIN' in top_keywords_df.columns:
                for asin_list in top_keywords_df['前十ASIN'].dropna():
                    if isinstance(asin_list, str):
                        asins = [a.strip() for a in asin_list.split(',')]
                        competitor_asins.extend(asins)

            # Get unique competitor ASINs (limit to top 10)
            competitor_asins = list(dict.fromkeys(competitor_asins))[:10]

            # For competitor brands and titles, we'll use placeholder data
            # In a real scenario, you'd fetch this from Amazon API or another source
            competitor_brands = ["UGG", "Bearpaw", "Dearfoams", "Skechers", "Crocs"]

            # Extract sample competitor titles from top keywords
            competitor_titles = [
                f"{core_keywords[i]} - Premium Quality"
                for i in range(min(5, len(core_keywords)))
            ]

            # ===== STEP 5: Create five-point requirements =====
            # Based on the product type and top keywords, generate requirements
            five_points_requirements = [
                f"Optimized for top keyword: {core_keywords[0] if core_keywords else 'slippers'}",
                f"Target high-conversion terms like '{core_keywords[1] if len(core_keywords) > 1 else 'comfortable'}'",
                "Plush, cozy comfort (faux fur/fleece lining)",
                "Durable, non-slip rubber outsole",
                "True-to-size fit with wide-width options"
            ]

            # ===== STEP 6: Construct the structured input data =====
            input_data = {
                "brand_name": brand_name,
                "product_type": product_type,
                "competitor_brands": competitor_brands,
                "core_keywords": core_keywords,
                "word_frequency": word_frequency,
                "competitor_titles": competitor_titles,
                "five_points_requirements": five_points_requirements,
                "metadata": {
                    "total_keywords_analyzed": len(merged_df),
                    "top_keywords_selected": top_n,
                    "average_monthly_search": int(top_keywords_df['月搜索量'].mean()),
                    "average_purchase_rate": float(top_keywords_df['购买率'].mean()),
                    "competitor_asins": competitor_asins
                }
            }

            return input_data

        except Exception as e:
            raise Exception(f"Error processing input files: {str(e)}")

    def __call__(
        self,
        file_path: str = None,
        format: str = 'markdown',
        sheet_name: Optional[str] = None,
        header: int = 0,
        max_rows: Optional[int] = 100,
        preprocess: bool = True,
        format_type: Optional[str] = None,
        # Legacy parameters for backward compatibility
        file_seller_elf: str = None,
        file_sif: str = None,
        brand_name: str = "Amazing Cosy",
        product_type: str = "Women's Slippers",
        top_n: int = 50
    ) -> str:
        """
        Make the tool callable. Can be used in two modes:

        1. **New mode (flexible)**: Read and format XLSX files for agent consumption
           - file_path: Path to XLSX file to read
           - format: Output format ('markdown', 'json', 'dict')
           - preprocess: Apply format-specific preprocessing
           - format_type: Force format type ('seller_elf', 'sif')

        2. **Legacy mode**: Process seller_elf and sif files (backward compatible)
           - file_seller_elf, file_sif: Paths to specific XLSX files
           - brand_name, product_type, top_n: Processing parameters

        Args:
            file_path: Path to XLSX file (new mode)
            format: Output format - 'markdown', 'json', or 'dict' (default: 'markdown')
            sheet_name: Sheet name to read (default: first sheet)
            header: Header row number (default: 0, auto-adjusted for sif)
            max_rows: Max rows to return (default: 100)
            preprocess: Apply format-specific preprocessing (default: True)
            format_type: Force format type - 'seller_elf', 'sif', or None for auto-detect
            file_seller_elf: Legacy - seller_elf.xlsx path
            file_sif: Legacy - sif.xlsx path
            brand_name: Legacy - brand name
            product_type: Legacy - product type
            top_n: Legacy - number of top keywords

        Returns:
            Formatted data as string (markdown/json) or JSON string (dict/legacy mode)
        """
        # Legacy mode: if both seller_elf and sif files are provided
        if file_seller_elf and file_sif:
            result = self.process_input_files(
                file_seller_elf,
                file_sif,
                brand_name,
                product_type,
                top_n
            )
            return json.dumps(result, indent=2, ensure_ascii=False)

        # New mode: flexible XLSX reading
        if file_path:
            return self.read_and_format(
                file_path=file_path,
                format=format,
                sheet_name=sheet_name,
                header=header,
                max_rows=max_rows,
                preprocess=preprocess,
                format_type=format_type
            )

        raise ValueError(
            "Must provide either 'file_path' (new mode) or both "
            "'file_seller_elf' and 'file_sif' (legacy mode)"
        )


# Create a singleton instance
xlsx_processor_tool = XlsxProcessorTool()
