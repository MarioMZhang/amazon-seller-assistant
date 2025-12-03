# Real Data Integration Tests

## Overview

Comprehensive integration tests using actual `seller_elf.xlsx` and `sif.xlsx` files from the `data/` directory. These tests verify that preprocessing works correctly with real-world data.

## Test Suite: TestXlsxProcessorToolIntegration

**Total Tests: 10** (all passing ✅)

### 1. test_read_real_seller_elf_file
- Verifies basic reading of seller_elf.xlsx file
- Confirms DataFrame structure and column presence
- Tests basic data loading functionality

### 2. test_read_real_sif_file
- Verifies basic reading of sif.xlsx file with header=1
- Confirms DataFrame structure and column presence
- Tests header row detection

### 3. test_legacy_process_input_files
- Tests backward compatibility with original process_input_files method
- Verifies INPUT_DATA structure generation
- Confirms top-50 keyword filtering works

### 4. test_call_legacy_mode
- Tests __call__ method in legacy mode
- Verifies JSON output structure
- Confirms brand name and product type are preserved

### 5. test_real_seller_elf_preprocessing ⭐ NEW
**Comprehensive preprocessing validation for seller_elf data:**
- ✅ Verifies all rows have non-null keywords
- ✅ Confirms numeric columns are properly typed (int/float)
- ✅ Validates data is sorted by monthly search volume (descending)
- ✅ Ensures no negative values in key metrics
- ✅ Tests filtering of up to 20 rows

**Sample Test Output:**
```python
# Top keywords sorted by search volume
[
    {'关键词': 'uggs', '月搜索量': 1902043, '月购买量': 1902, ...},
    {'关键词': 'slippers for women', '月搜索量': 1051640, '月购买量': 9149, ...},
    {'关键词': 'slippers', '月搜索量': 700329, '月购买量': 4412, ...},
    ...
]
```

### 6. test_real_sif_preprocessing ⭐ NEW
**Comprehensive preprocessing validation for sif data:**
- ✅ Verifies all rows have non-null keywords
- ✅ Confirms numeric columns are properly typed
- ✅ Validates percentage conversion ('3.4512%' → 0.034512)
- ✅ Ensures ASIN columns are floats between 0 and 1
- ✅ Validates data is sorted by weekly search volume (descending)

**Sample Test Output:**
```python
# Percentage columns properly converted
{
    'B0B5HRHM9N': 0.034512,  # Was '3.4512%'
    'B0D9QNGMZ8': 0.023686,  # Was '2.3686%'
    'B0FCBBK3L8': 0.006546,  # Was '0.6546%'
}
```

### 7. test_real_data_multiple_files_preprocessing ⭐ NEW
**Tests reading and preprocessing both files together:**
- ✅ Markdown output contains both file labels
- ✅ JSON output structure is correct (list of 2 files)
- ✅ Each file is correctly identified by format_type
- ✅ Both files are limited to max_rows
- ✅ Data Summary and Data Table sections present

**Sample JSON Output:**
```json
[
    {
        "file": "Seller Elf Keywords",
        "format_type": "seller_elf",
        "data": [/* 10 rows */]
    },
    {
        "file": "SIF Data",
        "format_type": "sif",
        "data": [/* 10 rows */]
    }
]
```

### 8. test_real_seller_elf_markdown_formatting ⭐ NEW
**Tests markdown output for LLM consumption:**
- ✅ Verifies markdown structure (headers, tables, statistics)
- ✅ Confirms presence of Data Summary section
- ✅ Validates Data Table with pipe separators
- ✅ Checks Numeric Column Statistics are included
- ✅ Ensures Chinese column names render correctly

**Sample Markdown Output:**
```markdown
## Data Summary
- **Total Rows**: 5
- **Total Columns**: 33
- **Columns**: 关键词, 月搜索量, 月购买量, ...

## Data Table
| 关键词 | 月搜索量 | 月购买量 | 购买率 | ...
|--------|----------|----------|--------|----
| uggs   | 1902043  | 1902     | 0.001  | ...
...

## Numeric Column Statistics
...
```

### 9. test_real_sif_json_formatting ⭐ NEW
**Tests JSON output for programmatic use:**
- ✅ Verifies valid JSON parsing
- ✅ Confirms list structure with proper data types
- ✅ Validates required fields present in all items
- ✅ Tests max_rows limiting (15 rows)

### 10. test_real_data_preprocessing_comparison ⭐ NEW
**Compares preprocessing ON vs OFF:**
- ✅ Raw data may contain more rows (filtered rows included)
- ✅ Processed data is sorted, raw data maintains original order
- ✅ Processed data has proper types, validated structure
- ✅ Demonstrates preprocessing impact on data quality

**Comparison Example:**
```python
# RAW DATA (preprocess=False)
# - May include rows with null keywords
# - Original order (unsorted)
# - 30 rows as-is

# PROCESSED DATA (preprocess=True)
# - Null keywords filtered out
# - Sorted by search volume
# - ≤30 rows (some filtered)
# - All numeric columns properly typed
```

## Test Coverage Summary

| Category | Tests | Status |
|----------|-------|--------|
| Basic Reading | 2 | ✅ All Pass |
| Legacy Compatibility | 2 | ✅ All Pass |
| seller_elf Preprocessing | 2 | ✅ All Pass |
| sif Preprocessing | 2 | ✅ All Pass |
| Multi-file Processing | 1 | ✅ All Pass |
| Comparison Tests | 1 | ✅ All Pass |
| **TOTAL** | **10** | **✅ 100%** |

## New Tests Added (7)

1. ✅ `test_real_seller_elf_preprocessing` - Validates seller_elf data cleaning and sorting
2. ✅ `test_real_sif_preprocessing` - Validates sif percentage conversion and sorting
3. ✅ `test_real_data_multiple_files_preprocessing` - Tests combined file processing
4. ✅ `test_real_seller_elf_markdown_formatting` - Tests LLM-friendly markdown output
5. ✅ `test_real_sif_json_formatting` - Tests programmatic JSON output
6. ✅ `test_real_data_preprocessing_comparison` - Compares raw vs processed data
7. ✅ All tests use actual data files from `data/` directory

## Running the Tests

### Run all integration tests:
```bash
python3 -m pytest tests/test_xlsx_processor_tool.py::TestXlsxProcessorToolIntegration -v
```

### Run specific real data test:
```bash
python3 -m pytest tests/test_xlsx_processor_tool.py::TestXlsxProcessorToolIntegration::test_real_seller_elf_preprocessing -v
```

### Run all tests with coverage:
```bash
python3 -m pytest tests/test_xlsx_processor_tool.py -v --cov=src/tools/xlsx_processor_tool
```

## What These Tests Verify

### Data Quality
- ✅ No null/missing keywords after preprocessing
- ✅ All numeric columns properly typed (not strings)
- ✅ Percentage strings converted to floats (0-1 range)
- ✅ Data sorted by relevance (search volume)

### Format Detection
- ✅ Auto-detects seller_elf format
- ✅ Auto-detects sif format
- ✅ Handles both formats correctly

### Output Formats
- ✅ Markdown format for LLM agents
- ✅ JSON format for programmatic use
- ✅ Dict format for Python manipulation
- ✅ Multi-file combined outputs

### Edge Cases
- ✅ Empty rows filtered correctly
- ✅ Max rows limiting works
- ✅ Unicode content preserved
- ✅ Percentage conversion accurate

## Integration with Real Data

These tests use the actual files:
- `data/seller_elf.xlsx` - 100+ rows of keyword data
- `data/sif.xlsx` - 1000+ rows of search intelligence data

All tests automatically skip if data files are not present, making the test suite portable.

## Example Test Results

```bash
tests/test_xlsx_processor_tool.py::TestXlsxProcessorToolIntegration::test_real_seller_elf_preprocessing PASSED
tests/test_xlsx_processor_tool.py::TestXlsxProcessorToolIntegration::test_real_sif_preprocessing PASSED
tests/test_xlsx_processor_tool.py::TestXlsxProcessorToolIntegration::test_real_data_multiple_files_preprocessing PASSED
tests/test_xlsx_processor_tool.py::TestXlsxProcessorToolIntegration::test_real_seller_elf_markdown_formatting PASSED
tests/test_xlsx_processor_tool.py::TestXlsxProcessorToolIntegration::test_real_sif_json_formatting PASSED
tests/test_xlsx_processor_tool.py::TestXlsxProcessorToolIntegration::test_real_data_preprocessing_comparison PASSED

10 passed in 2.49s ✅
```

## Conclusion

The real data integration tests provide comprehensive validation that:
1. Preprocessing works correctly with actual production data
2. Both seller_elf and sif formats are handled properly
3. Output formats are suitable for both LLM and programmatic consumption
4. Data quality is maintained throughout the pipeline
5. The tool is production-ready for agent integration
