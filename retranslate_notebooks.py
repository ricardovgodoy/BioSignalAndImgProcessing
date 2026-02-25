#!/usr/bin/env python3
"""
Professional retranslation of Jupyter notebooks from Portuguese to English.
Uses Google Translate API via deep-translator for natural, context-aware translations.
"""

import json
import re
from pathlib import Path
from deep_translator import GoogleTranslator
import time

def translate_text(text, source='pt', target='en', max_retries=3):
    """
    Translate text from Portuguese to English using Google Translate.
    Handles errors and retries automatically.
    """
    if not text or not text.strip():
        return text
    
    # Skip if text is already in English (basic heuristic)
    # Check for common Portuguese words that shouldn't appear in English
    portuguese_indicators = ['você', 'vocês', 'para', 'com', 'seu', 'sua', 'seus', 'suas', 
                             'este', 'esta', 'estes', 'estas', 'aquele', 'aquela',
                             'fazer', 'terá', 'será', 'pode', 'podem', 'deve', 'devem']
    
    text_lower = text.lower()
    has_portuguese = any(word in text_lower.split() for word in portuguese_indicators)
    
    # Also check if text has mostly English words (simple heuristic)
    english_words = ['the', 'and', 'for', 'with', 'this', 'that', 'from', 'will', 'can', 'should']
    has_english = any(word in text_lower.split() for word in english_words)
    
    # If it looks like English already, don't translate
    if has_english and not has_portuguese and len(text.split()) > 3:
        return text
    
    for attempt in range(max_retries):
        try:
            # Split long text into chunks (Google Translate has a 5000 char limit)
            if len(text) > 4500:
                # Split by sentences or paragraphs
                chunks = []
                current_chunk = ""
                sentences = re.split(r'([.!?]\s+)', text)
                
                for i in range(0, len(sentences), 2):
                    sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else '')
                    if len(current_chunk) + len(sentence) < 4500:
                        current_chunk += sentence
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = sentence
                
                if current_chunk:
                    chunks.append(current_chunk)
                
                # Translate each chunk
                translated_chunks = []
                for chunk in chunks:
                    translator = GoogleTranslator(source=source, target=target)
                    translated = translator.translate(chunk)
                    translated_chunks.append(translated)
                    time.sleep(0.5)  # Be nice to the API
                
                return ' '.join(translated_chunks)
            else:
                translator = GoogleTranslator(source=source, target=target)
                translated = translator.translate(text)
                return translated
                
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Translation error (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(2)  # Wait before retry
            else:
                print(f"Failed to translate after {max_retries} attempts: {text[:100]}...")
                return text  # Return original on failure
    
    return text

def translate_markdown_cell(source_lines):
    """
    Translate markdown cell content while preserving formatting.
    """
    if not source_lines:
        return source_lines
    
    # Join lines into full text
    full_text = ''.join(source_lines)
    
    # Preserve code blocks and inline code
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"<<<CODE_BLOCK_{len(code_blocks)-1}>>>"
    
    # Save code blocks (triple backticks)
    full_text = re.sub(r'```[\s\S]*?```', save_code_block, full_text)
    
    # Save inline code (single backticks)
    inline_codes = []
    def save_inline_code(match):
        inline_codes.append(match.group(0))
        return f"<<<INLINE_CODE_{len(inline_codes)-1}>>>"
    
    full_text = re.sub(r'`[^`\n]+`', save_inline_code, full_text)
    
    # Translate the text
    translated = translate_text(full_text)
    
    # Restore inline codes
    for i, code in enumerate(inline_codes):
        translated = translated.replace(f"<<<INLINE_CODE_{i}>>>", code)
    
    # Restore code blocks
    for i, block in enumerate(code_blocks):
        translated = translated.replace(f"<<<CODE_BLOCK_{i}>>>", block)
    
    # Convert back to lines
    return [translated]

def translate_code_cell(source_lines):
    """
    Translate comments in code cells while preserving code.
    """
    if not source_lines:
        return source_lines
    
    translated_lines = []
    for line in source_lines:
        # Check if line contains a comment
        if '#' in line:
            # Split by # to separate code from comment
            parts = line.split('#', 1)
            code_part = parts[0]
            
            if len(parts) > 1:
                comment_part = parts[1]
                # Translate the comment
                translated_comment = translate_text(comment_part.strip())
                # Reconstruct the line
                translated_line = f"{code_part}# {translated_comment}\n"
                translated_lines.append(translated_line)
            else:
                translated_lines.append(line)
        else:
            # No comment, keep as is
            translated_lines.append(line)
    
    return translated_lines

def retranslate_notebook(input_path, output_path=None):
    """
    Retranslate a Jupyter notebook from Portuguese to English.
    """
    if output_path is None:
        output_path = input_path
    
    print(f"Processing: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Process each cell
    for i, cell in enumerate(notebook.get('cells', [])):
        print(f"  Cell {i+1}/{len(notebook['cells'])} ({cell.get('cell_type', 'unknown')})")
        
        if cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            if source:
                translated = translate_markdown_cell(source)
                cell['source'] = translated
                time.sleep(0.3)  # Rate limiting
        
        elif cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            if source:
                translated = translate_code_cell(source)
                cell['source'] = translated
                time.sleep(0.2)  # Rate limiting
    
    # Save the retranslated notebook
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)
    
    print(f"✓ Saved: {output_path}\n")

def main():
    """
    Retranslate all _en.ipynb files in the assignments directory.
    """
    assignments_dir = Path('/home/runner/work/BioSignalAndImgProcessing/BioSignalAndImgProcessing/assignments')
    
    # Find all _en.ipynb files
    en_files = sorted(assignments_dir.glob('*_en.ipynb'))
    
    print(f"Found {len(en_files)} files to retranslate\n")
    print("=" * 60)
    
    for i, file_path in enumerate(en_files):
        print(f"\n[{i+1}/{len(en_files)}] {file_path.name}")
        print("-" * 60)
        retranslate_notebook(file_path)
    
    print("\n" + "=" * 60)
    print(f"✓ Retranslation complete! Processed {len(en_files)} files")

if __name__ == '__main__':
    main()
