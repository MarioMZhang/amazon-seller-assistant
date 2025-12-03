"""
Unit tests for XlsxProcessorTool - testing XLSX file reading and formatting for agent consumption.
"""

import pytest
import pandas as pd
import numpy as np
import json
import tempfile
import os
from src.tools.xlsx_processor_tool import XlsxProcessorTool, xlsx_processor_tool


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        '关键词': ['slippers women', 'winter boots', 'cozy shoes', 'warm footwear'],
        '月搜索量': [10000, 8000, 5000, 3000],
        '月购买量': [500, 400, 250, 150],
        '购买率': [0.05, 0.05, 0.05, 0.05],
        '流量占比': [0.15, 0.12, 0.08, 0.05]
    })


@pytest.fixture
def temp_xlsx_file(sample_dataframe):
    """Create a temporary XLSX file for testing."""
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as f:
        temp_path = f.name
        sample_dataframe.to_excel(temp_path, index=False)

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def temp_xlsx_file_with_header(sample_dataframe):
    """Create a temporary XLSX file with header on row 1."""
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as f:
        temp_path = f.name
        # Write empty first row, then data
        with pd.ExcelWriter(temp_path, engine='openpyxl') as writer:
            pd.DataFrame([['Header Row']]).to_excel(writer, index=False, header=False)
            sample_dataframe.to_excel(writer, index=False, startrow=1)

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


class TestXlsxProcessorTool:
    """Test suite for XlsxProcessorTool."""

    def test_initialization(self):
        """Test tool initialization."""
        tool = XlsxProcessorTool()
        assert tool.name == "xlsx_processor_tool"
        assert "LLM agent consumption" in tool.description

    def test_read_xlsx_file(self, temp_xlsx_file, sample_dataframe):
        """Test reading a basic XLSX file."""
        tool = XlsxProcessorTool()
        df = tool.read_xlsx_file(temp_xlsx_file)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == len(sample_dataframe)
        assert list(df.columns) == list(sample_dataframe.columns)
        assert df['关键词'].tolist() == sample_dataframe['关键词'].tolist()

    def test_read_xlsx_file_with_max_rows(self, temp_xlsx_file):
        """Test reading XLSX file with max_rows limit."""
        tool = XlsxProcessorTool()
        df = tool.read_xlsx_file(temp_xlsx_file, max_rows=2)

        assert len(df) == 2

    def test_read_xlsx_file_with_custom_header(self, temp_xlsx_file_with_header):
        """Test reading XLSX file with custom header row."""
        tool = XlsxProcessorTool()
        df = tool.read_xlsx_file(temp_xlsx_file_with_header, header=1)

        assert isinstance(df, pd.DataFrame)
        assert '关键词' in df.columns

    def test_read_xlsx_file_not_found(self):
        """Test error handling when file doesn't exist."""
        tool = XlsxProcessorTool()

        with pytest.raises(Exception) as exc_info:
            tool.read_xlsx_file('/nonexistent/file.xlsx')

        assert "Error reading XLSX file" in str(exc_info.value)

    def test_format_as_markdown(self, sample_dataframe):
        """Test formatting DataFrame as markdown."""
        tool = XlsxProcessorTool()
        markdown = tool.format_as_markdown(sample_dataframe, max_rows=10)

        assert isinstance(markdown, str)
        assert "## Data Summary" in markdown
        assert "## Data Table" in markdown
        assert "Total Rows" in markdown
        assert "Total Columns" in markdown
        assert "关键词" in markdown
        assert "slippers women" in markdown

    def test_format_as_markdown_with_stats(self, sample_dataframe):
        """Test markdown formatting includes statistics."""
        tool = XlsxProcessorTool()
        markdown = tool.format_as_markdown(sample_dataframe, include_stats=True)

        assert "## Numeric Column Statistics" in markdown
        assert "月搜索量" in markdown

    def test_format_as_markdown_without_stats(self, sample_dataframe):
        """Test markdown formatting without statistics."""
        tool = XlsxProcessorTool()
        markdown = tool.format_as_markdown(sample_dataframe, include_stats=False)

        assert "## Numeric Column Statistics" not in markdown
        assert "## Data Table" in markdown

    def test_format_as_markdown_max_rows(self, sample_dataframe):
        """Test markdown formatting respects max_rows."""
        tool = XlsxProcessorTool()
        markdown = tool.format_as_markdown(sample_dataframe, max_rows=2)

        assert "Showing first 2 rows out of 4 total" in markdown

    def test_format_as_json(self, sample_dataframe):
        """Test formatting DataFrame as JSON."""
        tool = XlsxProcessorTool()
        json_str = tool.format_as_json(sample_dataframe)

        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert isinstance(data, list)
        assert len(data) == 4
        assert data[0]['关键词'] == 'slippers women'
        assert data[0]['月搜索量'] == 10000

    def test_format_as_json_max_rows(self, sample_dataframe):
        """Test JSON formatting respects max_rows."""
        tool = XlsxProcessorTool()
        json_str = tool.format_as_json(sample_dataframe, max_rows=2)

        data = json.loads(json_str)
        assert len(data) == 2

    def test_format_as_json_orient(self, sample_dataframe):
        """Test JSON formatting with different orientations."""
        tool = XlsxProcessorTool()

        # Test 'records' orientation (default)
        json_records = tool.format_as_json(sample_dataframe, orient='records')
        data_records = json.loads(json_records)
        assert isinstance(data_records, list)

        # Test 'index' orientation
        json_index = tool.format_as_json(sample_dataframe, orient='index')
        data_index = json.loads(json_index)
        assert isinstance(data_index, dict)
        assert '0' in data_index  # First row index

    def test_read_and_format_markdown(self, temp_xlsx_file):
        """Test read_and_format with markdown output."""
        tool = XlsxProcessorTool()
        result = tool.read_and_format(temp_xlsx_file, format='markdown', max_rows=5)

        assert isinstance(result, str)
        assert "## Data Summary" in result
        assert "关键词" in result

    def test_read_and_format_json(self, temp_xlsx_file):
        """Test read_and_format with JSON output."""
        tool = XlsxProcessorTool()
        result = tool.read_and_format(temp_xlsx_file, format='json', max_rows=5)

        assert isinstance(result, str)
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) <= 5

    def test_read_and_format_dict(self, temp_xlsx_file):
        """Test read_and_format with dict output."""
        tool = XlsxProcessorTool()
        result = tool.read_and_format(temp_xlsx_file, format='dict', max_rows=5)

        assert isinstance(result, list)
        assert len(result) <= 5
        assert isinstance(result[0], dict)

    def test_read_and_format_invalid_format(self, temp_xlsx_file):
        """Test read_and_format with invalid format."""
        tool = XlsxProcessorTool()

        with pytest.raises(ValueError) as exc_info:
            tool.read_and_format(temp_xlsx_file, format='invalid')

        assert "Unsupported format" in str(exc_info.value)

    def test_read_multiple_files_markdown(self, temp_xlsx_file, sample_dataframe):
        """Test reading multiple files with markdown output."""
        # Create second temp file
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as f:
            temp_path2 = f.name
            sample_dataframe.to_excel(temp_path2, index=False)

        try:
            tool = XlsxProcessorTool()
            file_configs = [
                {'file_path': temp_xlsx_file, 'label': 'File 1', 'max_rows': 3},
                {'file_path': temp_path2, 'label': 'File 2', 'max_rows': 2}
            ]

            result = tool.read_multiple_files(file_configs, format='markdown')

            assert isinstance(result, str)
            assert "# File: File 1" in result
            assert "# File: File 2" in result
            assert "---" in result
        finally:
            if os.path.exists(temp_path2):
                os.unlink(temp_path2)

    def test_read_multiple_files_json(self, temp_xlsx_file, sample_dataframe):
        """Test reading multiple files with JSON output."""
        # Create second temp file
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as f:
            temp_path2 = f.name
            sample_dataframe.to_excel(temp_path2, index=False)

        try:
            tool = XlsxProcessorTool()
            file_configs = [
                {'file_path': temp_xlsx_file, 'label': 'File 1', 'max_rows': 2},
                {'file_path': temp_path2, 'label': 'File 2', 'max_rows': 2}
            ]

            result = tool.read_multiple_files(file_configs, format='json')

            assert isinstance(result, str)
            data = json.loads(result)
            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]['file'] == 'File 1'
            assert data[1]['file'] == 'File 2'
        finally:
            if os.path.exists(temp_path2):
                os.unlink(temp_path2)

    def test_call_new_mode_markdown(self, temp_xlsx_file):
        """Test __call__ method in new mode with markdown format."""
        tool = XlsxProcessorTool()
        result = tool(file_path=temp_xlsx_file, format='markdown', max_rows=3)

        assert isinstance(result, str)
        assert "## Data Summary" in result

    def test_call_new_mode_json(self, temp_xlsx_file):
        """Test __call__ method in new mode with JSON format."""
        tool = XlsxProcessorTool()
        result = tool(file_path=temp_xlsx_file, format='json', max_rows=3)

        assert isinstance(result, str)
        data = json.loads(result)
        assert isinstance(data, list)

    def test_call_no_arguments(self):
        """Test __call__ method with no arguments raises error."""
        tool = XlsxProcessorTool()

        with pytest.raises(ValueError) as exc_info:
            tool()

        assert "Must provide either 'file_path'" in str(exc_info.value)

    def test_singleton_instance(self):
        """Test that xlsx_processor_tool is a valid singleton instance."""
        assert isinstance(xlsx_processor_tool, XlsxProcessorTool)
        assert xlsx_processor_tool.name == "xlsx_processor_tool"


class TestXlsxProcessorToolIntegration:
    """Integration tests using real data files if available."""

    @pytest.mark.skipif(
        not os.path.exists('data/seller_elf.xlsx'),
        reason="seller_elf.xlsx not found in data directory"
    )
    def test_read_real_seller_elf_file(self):
        """Test reading the actual seller_elf.xlsx file."""
        tool = XlsxProcessorTool()
        df = tool.read_xlsx_file('data/seller_elf.xlsx')

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert '关键词' in df.columns

    @pytest.mark.skipif(
        not os.path.exists('data/sif.xlsx'),
        reason="sif.xlsx not found in data directory"
    )
    def test_read_real_sif_file(self):
        """Test reading the actual sif.xlsx file."""
        tool = XlsxProcessorTool()
        df = tool.read_xlsx_file('data/sif.xlsx', header=1)

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    @pytest.mark.skipif(
        not (os.path.exists('data/seller_elf.xlsx') and os.path.exists('data/sif.xlsx')),
        reason="Data files not found"
    )
    def test_legacy_process_input_files(self):
        """Test the legacy process_input_files method with real data."""
        tool = XlsxProcessorTool()

        result = tool.process_input_files(
            file_seller_elf='data/seller_elf.xlsx',
            file_sif='data/sif.xlsx',
            brand_name='Amazing Cosy',
            product_type='Women\'s Slippers',
            top_n=50
        )

        assert isinstance(result, dict)
        assert 'brand_name' in result
        assert 'product_type' in result
        assert 'core_keywords' in result
        assert 'word_frequency' in result
        assert 'competitor_brands' in result
        assert 'competitor_titles' in result
        assert 'five_points_requirements' in result
        assert result['brand_name'] == 'Amazing Cosy'
        assert len(result['core_keywords']) <= 50

    @pytest.mark.skipif(
        not (os.path.exists('data/seller_elf.xlsx') and os.path.exists('data/sif.xlsx')),
        reason="Data files not found"
    )
    def test_call_legacy_mode(self):
        """Test __call__ method in legacy mode with real data."""
        tool = XlsxProcessorTool()

        result = tool(
            file_seller_elf='data/seller_elf.xlsx',
            file_sif='data/sif.xlsx',
            brand_name='Amazing Cosy',
            product_type='Women\'s Slippers',
            top_n=50
        )

        assert isinstance(result, str)
        data = json.loads(result)
        assert isinstance(data, dict)
        assert 'brand_name' in data
        assert data['brand_name'] == 'Amazing Cosy'

    @pytest.mark.skipif(
        not os.path.exists('data/seller_elf.xlsx'),
        reason="seller_elf.xlsx not found"
    )
    def test_real_seller_elf_preprocessing(self):
        """Test comprehensive preprocessing on real seller_elf.xlsx data."""
        tool = XlsxProcessorTool()

        # Read with preprocessing enabled
        result = tool(
            file_path='data/seller_elf.xlsx',
            format='dict',
            format_type='seller_elf',
            max_rows=20,
            preprocess=True
        )

        assert isinstance(result, list)
        assert len(result) > 0
        assert len(result) <= 20

        # Verify all rows have keywords (no null values)
        for row in result:
            assert row['关键词'] is not None
            assert isinstance(row['关键词'], str)
            assert len(row['关键词']) > 0

        # Verify numeric columns are properly typed
        first_row = result[0]
        assert isinstance(first_row['月搜索量'], (int, float))
        assert isinstance(first_row['月购买量'], (int, float))
        assert isinstance(first_row['购买率'], (int, float))

        # Verify data is sorted by monthly search volume (descending)
        search_volumes = [row['月搜索量'] for row in result]
        assert search_volumes == sorted(search_volumes, reverse=True), \
            "Data should be sorted by monthly search volume in descending order"

        # Verify no negative values in key metrics
        for row in result:
            assert row['月搜索量'] >= 0
            assert row['月购买量'] >= 0
            assert row['购买率'] >= 0

    @pytest.mark.skipif(
        not os.path.exists('data/sif.xlsx'),
        reason="sif.xlsx not found"
    )
    def test_real_sif_preprocessing(self):
        """Test comprehensive preprocessing on real sif.xlsx data."""
        tool = XlsxProcessorTool()

        # Read with preprocessing enabled
        result = tool(
            file_path='data/sif.xlsx',
            format='dict',
            format_type='sif',
            max_rows=20,
            preprocess=True
        )

        assert isinstance(result, list)
        assert len(result) > 0
        assert len(result) <= 20

        # Verify all rows have keywords
        for row in result:
            assert row['关键词'] is not None
            assert isinstance(row['关键词'], str)

        # Verify numeric columns are properly typed
        first_row = result[0]
        assert isinstance(first_row['周搜索量'], (int, float))
        assert isinstance(first_row['在售商品数'], (int, float))
        assert isinstance(first_row['周搜索量排名'], (int, float))

        # Verify percentage columns are converted from strings to floats
        # ASIN columns should be floats between 0 and 1, not strings with '%'
        asin_cols = [col for col in first_row.keys() if col.startswith('B0') and '关键词类型' not in col]
        for col in asin_cols:
            if first_row[col] is not None:
                assert isinstance(first_row[col], (int, float)), \
                    f"Column {col} should be numeric, not string with '%'"
                # Should be a reasonable percentage value (0 to 1)
                if first_row[col] > 0:
                    assert 0 <= first_row[col] <= 1, \
                        f"Column {col} should be between 0 and 1, got {first_row[col]}"

        # Verify data is sorted by weekly search volume (descending)
        search_volumes = [row['周搜索量'] for row in result]
        assert search_volumes == sorted(search_volumes, reverse=True), \
            "Data should be sorted by weekly search volume in descending order"

    @pytest.mark.skipif(
        not (os.path.exists('data/seller_elf.xlsx') and os.path.exists('data/sif.xlsx')),
        reason="Data files not found"
    )
    def test_real_data_multiple_files_preprocessing(self):
        """Test reading and preprocessing multiple real data files together."""
        tool = XlsxProcessorTool()

        file_configs = [
            {
                'file_path': 'data/seller_elf.xlsx',
                'label': 'Seller Elf Keywords',
                'format_type': 'seller_elf',
                'max_rows': 10
            },
            {
                'file_path': 'data/sif.xlsx',
                'label': 'SIF Data',
                'format_type': 'sif',
                'max_rows': 10
            }
        ]

        # Test markdown output
        markdown_result = tool.read_multiple_files(
            file_configs,
            format='markdown',
            preprocess=True
        )

        assert isinstance(markdown_result, str)
        assert 'Seller Elf Keywords' in markdown_result
        assert 'SIF Data' in markdown_result
        assert '## Data Summary' in markdown_result
        assert '## Data Table' in markdown_result

        # Test JSON output
        json_result = tool.read_multiple_files(
            file_configs,
            format='json',
            preprocess=True
        )

        assert isinstance(json_result, str)
        data = json.loads(json_result)
        assert isinstance(data, list)
        assert len(data) == 2

        # Verify first file (seller_elf)
        assert data[0]['file'] == 'Seller Elf Keywords'
        assert data[0]['format_type'] == 'seller_elf'
        assert isinstance(data[0]['data'], list)
        assert len(data[0]['data']) <= 10

        # Verify second file (sif)
        assert data[1]['file'] == 'SIF Data'
        assert data[1]['format_type'] == 'sif'
        assert isinstance(data[1]['data'], list)
        assert len(data[1]['data']) <= 10

    @pytest.mark.skipif(
        not os.path.exists('data/seller_elf.xlsx'),
        reason="seller_elf.xlsx not found"
    )
    def test_real_seller_elf_markdown_formatting(self):
        """Test markdown formatting with real seller_elf data for LLM consumption."""
        tool = XlsxProcessorTool()

        result = tool(
            file_path='data/seller_elf.xlsx',
            format='markdown',
            format_type='seller_elf',
            max_rows=5,
            preprocess=True
        )

        assert isinstance(result, str)

        # Verify markdown structure
        assert '## Data Summary' in result
        assert 'Total Rows' in result
        assert 'Total Columns' in result
        assert '## Data Table' in result
        assert '关键词' in result
        assert '月搜索量' in result

        # Verify statistics are included
        assert '## Numeric Column Statistics' in result

        # Verify markdown table format (should have pipes)
        assert '|' in result

    @pytest.mark.skipif(
        not os.path.exists('data/sif.xlsx'),
        reason="sif.xlsx not found"
    )
    def test_real_sif_json_formatting(self):
        """Test JSON formatting with real sif data for programmatic use."""
        tool = XlsxProcessorTool()

        result = tool(
            file_path='data/sif.xlsx',
            format='json',
            format_type='sif',
            max_rows=15,
            preprocess=True
        )

        assert isinstance(result, str)

        # Parse JSON
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0
        assert len(data) <= 15

        # Verify JSON structure
        first_item = data[0]
        assert '关键词' in first_item
        assert '周搜索量' in first_item
        assert '在售商品数' in first_item

        # Verify all items have required fields
        for item in data:
            assert '关键词' in item
            assert '周搜索量' in item

    @pytest.mark.skipif(
        not os.path.exists('data/seller_elf.xlsx'),
        reason="seller_elf.xlsx not found"
    )
    def test_real_data_preprocessing_comparison(self):
        """Compare preprocessing ON vs OFF with real data to verify behavior."""
        tool = XlsxProcessorTool()

        # Read without preprocessing
        raw_data = tool(
            file_path='data/seller_elf.xlsx',
            format='dict',
            max_rows=30,
            preprocess=False
        )

        # Read with preprocessing
        processed_data = tool(
            file_path='data/seller_elf.xlsx',
            format='dict',
            format_type='seller_elf',
            max_rows=30,
            preprocess=True
        )

        # Preprocessed data should have same or fewer rows (due to filtering)
        assert len(processed_data) <= len(raw_data)

        # Preprocessed data should be sorted (descending by search volume)
        search_volumes = [row['月搜索量'] for row in processed_data]
        assert search_volumes == sorted(search_volumes, reverse=True)

        # Raw data might not be sorted
        raw_search_volumes = [row['月搜索量'] for row in raw_data if row.get('月搜索量')]
        # Don't assert on raw data sorting, just verify it exists
        assert len(raw_search_volumes) > 0


class TestXlsxProcessorToolPreprocessing:
    """Test preprocessing functionality for seller_elf and sif formats."""

    def test_detect_seller_elf_format(self):
        """Test detection of seller_elf format."""
        tool = XlsxProcessorTool()
        df = pd.DataFrame({
            '关键词': ['test'],
            '月搜索量': [1000],
            '月购买量': [100],
            '购买率': [0.1],
            '前十ASIN': ['B123']
        })

        format_type = tool.detect_file_format(df)
        assert format_type == 'seller_elf'

    def test_detect_sif_format(self):
        """Test detection of sif format."""
        tool = XlsxProcessorTool()
        df = pd.DataFrame({
            '关键词': ['test'],
            '周搜索量': [5000],
            '在售商品数': [100],
            '周搜索量排名': [50]
        })

        format_type = tool.detect_file_format(df)
        assert format_type == 'sif'

    def test_detect_unknown_format(self):
        """Test detection returns None for unknown format."""
        tool = XlsxProcessorTool()
        df = pd.DataFrame({
            'unknown_col': ['test'],
            'another_col': [123]
        })

        format_type = tool.detect_file_format(df)
        assert format_type is None

    def test_preprocess_seller_elf(self):
        """Test seller_elf preprocessing."""
        tool = XlsxProcessorTool()
        df = pd.DataFrame({
            '关键词': ['keyword1', 'keyword2', None, 'keyword4'],
            '月搜索量': ['1000', '2000', '1500', '500'],
            '月购买量': [100, 200, 150, 50],
            '购买率': [0.1, 0.1, 0.1, 0.1],
            '流量占比': [0.15, 0.20, None, 0.05],
            '前十ASIN': ['B123,B456', 'B789', 'B012', 'B345']
        })

        processed = tool.preprocess_seller_elf(df)

        # Should remove rows with missing keywords
        assert len(processed) == 3

        # Should convert numeric columns
        assert processed['月搜索量'].dtype in [np.int64, np.float64]

        # Should be sorted by monthly search volume (descending)
        assert processed.iloc[0]['月搜索量'] == 2000
        assert processed.iloc[1]['月搜索量'] == 1000
        assert processed.iloc[2]['月搜索量'] == 500

    def test_preprocess_sif(self):
        """Test sif preprocessing."""
        tool = XlsxProcessorTool()
        df = pd.DataFrame({
            '关键词': ['keyword1', None, 'keyword3'],
            '周搜索量': ['5000', '3000', '8000'],
            '在售商品数': [100, 200, 50],
            '周搜索量排名': [10, 20, 5],
            'B0B5HRHM9N': ['3.4512%', '1.7531%', '0.0564%']
        })

        processed = tool.preprocess_sif(df)

        # Should remove rows with missing keywords
        assert len(processed) == 2

        # Should be sorted by weekly search volume (descending)
        assert processed.iloc[0]['周搜索量'] == 8000
        assert processed.iloc[1]['周搜索量'] == 5000

        # Should convert percentage columns (check the row with keyword3 which has 8000 search volume)
        assert processed.iloc[0]['B0B5HRHM9N'] == pytest.approx(0.000564, rel=1e-5)

    def test_preprocess_dataframe_auto_detect(self):
        """Test automatic format detection in preprocessing."""
        tool = XlsxProcessorTool()

        # Test seller_elf auto-detect
        seller_elf_df = pd.DataFrame({
            '关键词': ['test'],
            '月搜索量': ['1000'],
            '月购买量': [100],
            '购买率': [0.1],
            '前十ASIN': ['B123']
        })

        processed = tool.preprocess_dataframe(seller_elf_df)
        assert processed['月搜索量'].dtype in [np.int64, np.float64]

        # Test sif auto-detect
        sif_df = pd.DataFrame({
            '关键词': ['test'],
            '周搜索量': ['5000'],
            '在售商品数': [100],
            '周搜索量排名': [50],
            'B0B5HRHM9N': ['3.4512%']
        })

        processed = tool.preprocess_dataframe(sif_df)
        assert processed.iloc[0]['B0B5HRHM9N'] == pytest.approx(0.034512, rel=1e-5)

    @pytest.mark.skipif(
        not os.path.exists('data/seller_elf.xlsx'),
        reason="seller_elf.xlsx not found"
    )
    def test_read_and_format_with_preprocessing_seller_elf(self):
        """Test read_and_format with preprocessing on real seller_elf file."""
        tool = XlsxProcessorTool()

        result = tool.read_and_format(
            'data/seller_elf.xlsx',
            format='json',
            max_rows=10,
            preprocess=True,
            format_type='seller_elf'
        )

        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) <= 10

        # Check that numeric columns are properly typed
        if len(data) > 0:
            assert isinstance(data[0]['月搜索量'], (int, float))

    @pytest.mark.skipif(
        not os.path.exists('data/sif.xlsx'),
        reason="sif.xlsx not found"
    )
    def test_read_and_format_with_preprocessing_sif(self):
        """Test read_and_format with preprocessing on real sif file."""
        tool = XlsxProcessorTool()

        result = tool.read_and_format(
            'data/sif.xlsx',
            format='json',
            max_rows=10,
            preprocess=True,
            format_type='sif'
        )

        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) <= 10

        # Check that percentage columns are converted to floats
        if len(data) > 0 and 'B0B5HRHM9N' in data[0]:
            # Should be a float between 0 and 1, not a string with '%'
            assert isinstance(data[0]['B0B5HRHM9N'], (int, float, type(None)))

    def test_read_and_format_without_preprocessing(self):
        """Test that preprocessing can be disabled."""
        tool = XlsxProcessorTool()

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as f:
            temp_path = f.name
            df = pd.DataFrame({
                '关键词': ['test1', 'test2', None],  # Include None to test filtering
                '月搜索量': [500, 1000, 750],
                '月购买量': [100, 50, 200],
                '购买率': [0.1, 0.2, 0.15],
                '前十ASIN': ['B123', 'B456', 'B789']
            })
            df.to_excel(temp_path, index=False)

        try:
            # With preprocessing disabled, None row should remain and data should not be sorted
            result = tool.read_and_format(
                temp_path,
                format='dict',
                preprocess=False
            )

            assert isinstance(result, list)
            assert len(result) == 3  # Should include the None row
            # Data should not be sorted (first row should have 500, not 1000)
            assert result[0]['月搜索量'] == 500

            # With preprocessing enabled, None row should be removed and sorted
            result_preprocessed = tool.read_and_format(
                temp_path,
                format='dict',
                preprocess=True,
                format_type='seller_elf'
            )

            assert len(result_preprocessed) == 2  # None row removed
            # Should be sorted by search volume (descending)
            assert result_preprocessed[0]['月搜索量'] == 1000
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestXlsxProcessorToolEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_dataframe_markdown(self):
        """Test formatting an empty DataFrame as markdown."""
        tool = XlsxProcessorTool()
        empty_df = pd.DataFrame()

        markdown = tool.format_as_markdown(empty_df)
        assert isinstance(markdown, str)
        assert "**Total Rows**: 0" in markdown

    def test_empty_dataframe_json(self):
        """Test formatting an empty DataFrame as JSON."""
        tool = XlsxProcessorTool()
        empty_df = pd.DataFrame()

        json_str = tool.format_as_json(empty_df)
        data = json.loads(json_str)
        assert data == []

    def test_dataframe_with_nan_values(self):
        """Test handling DataFrames with NaN values."""
        tool = XlsxProcessorTool()
        df_with_nan = pd.DataFrame({
            'col1': [1, 2, None, 4],
            'col2': ['a', None, 'c', 'd']
        })

        json_str = tool.format_as_json(df_with_nan)
        data = json.loads(json_str)

        # NaN should be converted to None (null in JSON)
        assert data[2]['col1'] is None
        assert data[1]['col2'] is None

    def test_unicode_content(self):
        """Test handling Unicode content in DataFrames."""
        tool = XlsxProcessorTool()
        unicode_df = pd.DataFrame({
            '中文': ['测试', '数据', '内容'],
            'emoji': ['😀', '🎉', '✨'],
            'mixed': ['hello 世界', 'test 测试', 'data 数据']
        })

        # Test markdown format
        markdown = tool.format_as_markdown(unicode_df)
        assert '测试' in markdown
        assert '😀' in markdown

        # Test JSON format
        json_str = tool.format_as_json(unicode_df)
        data = json.loads(json_str)
        assert data[0]['中文'] == '测试'
        assert data[0]['emoji'] == '😀'
