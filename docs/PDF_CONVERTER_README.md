# Documentation PDF Converter

This directory contains tools to convert all markdown documentation files to PDF format for easy submission.

## Quick Start

### Option 1: Using the Batch File (Windows)
Simply double-click `convert_docs_to_pdf.bat` or run it from command prompt:
```cmd
convert_docs_to_pdf.bat
```

### Option 2: Using Python Script Directly
```bash
python convert_to_pdf.py
```

## Requirements

The script will automatically install the required Python packages:
- `markdown2` - For converting markdown to HTML
- `weasyprint` - For converting HTML to PDF

**Windows Users**: If you encounter issues with weasyprint, you may need to install the GTK3 runtime:
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

## Output

- PDFs will be generated in the `docs/pdfs/` directory
- Each markdown file will create a corresponding PDF with the same name
- Files are styled with professional formatting suitable for submission

## What Gets Converted

All `.md` files in the docs directory:
- `README.md`
- `accuracy_assessment.md`
- `analysis_overview.md`
- `api.md`
- `business_vision.md`
- `dashboard.md`
- `data.md`
- `hypothesis_assessment.md`
- `monitoring.md`
- `quick_start.md`
- `security.md`
- `storytelling.md`
- `testing_and_optimization.md`
- `testing.md`

## Styling Features

The generated PDFs include:
- Professional typography with clean fonts
- Syntax highlighting for code blocks
- Proper table formatting
- Styled headers and sections
- Page numbers
- Consistent margins and spacing

## Troubleshooting

1. **Import errors**: The script will attempt to install missing packages automatically
2. **Permission errors**: Make sure you have write access to the docs directory
3. **GTK3 issues on Windows**: Install the GTK3 runtime from the link above
4. **Virtual environment**: The batch file will automatically activate your project's virtual environment if it exists

## Manual Installation

If automatic installation fails, install packages manually:
```bash
pip install markdown2 weasyprint
```
