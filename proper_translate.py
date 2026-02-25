#!/usr/bin/env python3
"""
Proper translation script for Jupyter notebooks from Portuguese to English.
Reads both Portuguese original and current bad English version to create proper translations.
"""

import json
import sys
from typing import Dict, List, Any
import anthropic
import os

def read_notebook(filepath: str) -> Dict[str, Any]:
    """Read a Jupyter notebook file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_notebook(filepath: str, notebook: Dict[str, Any]):
    """Write a Jupyter notebook file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)

def translate_notebook(pt_notebook: Dict[str, Any], bad_en_notebook: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a proper English translation by analyzing both Portuguese original and bad English version.
    Uses Claude API for high-quality translation.
    """
    # Start with the Portuguese structure
    result = json.loads(json.dumps(pt_notebook))
    
    # Get API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Process each cell
    for i, (pt_cell, bad_en_cell) in enumerate(zip(pt_notebook['cells'], bad_en_notebook['cells'])):
        if pt_cell['cell_type'] == 'markdown':
            # Translate markdown cells
            pt_content = ''.join(pt_cell['source'])
            bad_en_content = ''.join(bad_en_cell['source'])
            
            if pt_content.strip():
                prompt = f"""You are a professional translator specializing in academic/technical materials. 

PORTUGUESE ORIGINAL:
{pt_content}

CURRENT BAD AUTO-TRANSLATION:
{bad_en_content}

Create a proper, natural English translation that:
- Sounds like it was originally written in English by a native speaker
- Uses professional, academic tone appropriate for course materials
- Maintains all formatting (markdown, LaTeX, etc.)
- Translates technical terms correctly
- Has proper grammar and sentence structure
- Contains NO Portuguese words (except in intentional examples)

Provide ONLY the translated text, no explanations or comments."""

                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                translated = message.content[0].text.strip()
                result['cells'][i]['source'] = [translated + '\n' if not translated.endswith('\n') else translated]
                
        elif pt_cell['cell_type'] == 'code':
            # For code cells, translate only comments
            pt_source = pt_cell['source']
            bad_en_source = bad_en_cell['source']
            
            # Check if there are comments to translate
            has_comments = any('#' in line for line in pt_source)
            
            if has_comments:
                pt_code = ''.join(pt_source)
                bad_en_code = ''.join(bad_en_source)
                
                prompt = f"""You are a professional translator for technical code.

PORTUGUESE CODE WITH COMMENTS:
{pt_code}

CURRENT BAD AUTO-TRANSLATION:
{bad_en_code}

Translate ONLY the comments to natural English. Keep ALL code exactly the same.
- Preserve all code structure, indentation, and formatting
- Translate comments to sound natural and professional
- Keep variable names, function calls, outputs unchanged
- NO Portuguese in comments

Provide ONLY the code with translated comments, no explanations."""

                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                translated_code = message.content[0].text.strip()
                # Ensure proper line endings
                if not translated_code.endswith('\n'):
                    translated_code += '\n'
                result['cells'][i]['source'] = [translated_code]
            else:
                # No comments, use bad_en_cell source (should be same as pt)
                result['cells'][i]['source'] = bad_en_cell['source']
            
            # Always preserve outputs exactly
            if 'outputs' in bad_en_cell:
                result['cells'][i]['outputs'] = bad_en_cell['outputs']
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python proper_translate.py <notebook_base_name>")
        print("Example: python proper_translate.py Aula_10")
        sys.exit(1)
    
    base_name = sys.argv[1]
    assignments_dir = "assignments"
    
    pt_file = f"{assignments_dir}/{base_name}.ipynb"
    bad_en_file = f"{assignments_dir}/{base_name}_en.ipynb"
    output_file = bad_en_file
    
    print(f"Processing {base_name}...")
    print(f"  Reading Portuguese: {pt_file}")
    print(f"  Reading bad English: {bad_en_file}")
    
    pt_notebook = read_notebook(pt_file)
    bad_en_notebook = read_notebook(bad_en_file)
    
    print(f"  Translating...")
    translated_notebook = translate_notebook(pt_notebook, bad_en_notebook)
    
    print(f"  Writing to: {output_file}")
    write_notebook(output_file, translated_notebook)
    
    print(f"✓ Completed {base_name}")

if __name__ == "__main__":
    main()
