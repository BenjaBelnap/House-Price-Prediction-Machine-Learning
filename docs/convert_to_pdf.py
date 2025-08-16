#!/usr/bin/env python3
"""
PDF Conversion Helper Script for Documentation

This script converts all markdown files in the docs directory to PDF format
for easy submission. It uses markdown2 and weasyprint libraries.

Usage:
    python convert_to_pdf.py

Requirements:
    pip install markdown2 weasyprint

Note: On Windows, you may need to install GTK3 runtime for weasyprint:
    https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
"""

import os
import sys
from pathlib import Path
import subprocess

def install_requirements():
    """Install required packages if not already installed"""
    required_packages = ['markdown2', 'weasyprint']
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def convert_md_to_pdf(md_file_path, output_dir):
    """Convert a single markdown file to PDF"""
    try:
        import markdown2
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError as e:
        print(f"Error importing required libraries: {e}")
        print("Please install required packages: pip install markdown2 weasyprint")
        return False
    
    # Read markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])
    
    # Add CSS styling for better PDF appearance
    css_style = """
    <style>
    body {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.4;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    h1 {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    h2 {
        color: #34495e;
        border-bottom: 2px solid #bdc3c7;
        padding-bottom: 5px;
        margin-top: 25px;
    }
    h3 {
        color: #34495e;
        margin-top: 20px;
    }
    code {
        background-color: #f8f9fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 10pt;
    }
    pre {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #3498db;
        overflow-x: auto;
        font-size: 9pt;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
    }
    th, td {
        border: 1px solid #bdc3c7;
        padding: 8px 12px;
        text-align: left;
    }
    th {
        background-color: #ecf0f1;
        font-weight: bold;
    }
    blockquote {
        border-left: 4px solid #3498db;
        padding-left: 15px;
        margin-left: 0;
        font-style: italic;
        color: #555;
    }
    .page-break {
        page-break-before: always;
    }
    @page {
        margin: 1in;
        @bottom-right {
            content: counter(page);
        }
    }
    </style>
    """
    
    # Create complete HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{md_file_path.stem}</title>
        {css_style}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Generate PDF
    output_file = output_dir / f"{md_file_path.stem}.pdf"
    
    try:
        font_config = FontConfiguration()
        HTML(string=full_html).write_pdf(
            output_file,
            font_config=font_config
        )
        return True
    except Exception as e:
        print(f"Error converting {md_file_path.name}: {e}")
        return False

def main():
    """Main function to convert all markdown files to PDF"""
    print("Documentation PDF Converter")
    print("=" * 40)
    
    # Install requirements if needed
    try:
        install_requirements()
    except Exception as e:
        print(f"Error installing requirements: {e}")
        return
    
    # Get the docs directory
    docs_dir = Path(__file__).parent
    output_dir = docs_dir / "pdfs"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Find all markdown files
    md_files = list(docs_dir.glob("*.md"))
    
    if not md_files:
        print("No markdown files found in the docs directory.")
        return
    
    print(f"Found {len(md_files)} markdown files:")
    for md_file in md_files:
        print(f"  - {md_file.name}")
    
    print(f"\nConverting to PDFs in: {output_dir}")
    print("-" * 40)
    
    successful_conversions = 0
    failed_conversions = 0
    
    # Convert each file
    for md_file in md_files:
        print(f"Converting {md_file.name}...", end=" ")
        if convert_md_to_pdf(md_file, output_dir):
            print("✓ Success")
            successful_conversions += 1
        else:
            print("✗ Failed")
            failed_conversions += 1
    
    # Summary
    print("-" * 40)
    print(f"Conversion Summary:")
    print(f"  Successful: {successful_conversions}")
    print(f"  Failed: {failed_conversions}")
    print(f"  Total: {len(md_files)}")
    
    if successful_conversions > 0:
        print(f"\nPDFs saved to: {output_dir.absolute()}")
    
    if failed_conversions > 0:
        print("\nNote: If conversions failed, you may need to install GTK3 runtime on Windows:")
        print("https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer")

if __name__ == "__main__":
    main()
