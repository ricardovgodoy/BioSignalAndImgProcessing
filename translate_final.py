#!/usr/bin/env python3
"""
Final comprehensive translation script for Portuguese to English Jupyter notebooks.
"""

import json
import re
from pathlib import Path

def get_all_translations():
    """Get comprehensive translation dictionary sorted by length (longest first)."""
    trans = {
        # === COMPLETE PHRASES (Highest Priority) ===
        "Nesta prática, iremos": "In this practice, we will",
        "comparar a performance de diferentes filtros, tanto no domínio do tempo quanto da frequência":
            "compare the performance of different filters, both in the time domain and frequency domain",
        "tanto no domínio do tempo quanto da frequência": "both in the time domain and frequency domain",
        "comparar a performance de diferentes filtros": "compare the performance of different filters",
        "Ruídos de alta frequência podem ser atenuados com filtros passa-baixa, média sincrona, e até mesmo média móvel":
            "High-frequency noise can be attenuated with low-pass filters, synchronous averaging, and even moving average",
        "Ruídos de baixa frequência podem ser atenuados com filtros derivativos e filtros passa-alta":
            "Low-frequency noise can be attenuated with derivative filters and high-pass filters",
        "Ruídos estruturados ou ruído de linha podem ser atenuados com filtros de Notch":
            "Structured noise or line noise can be attenuated with Notch filters",
        "Os filtros no domínio do tempo podem ser empregados sem que a caracterização espectral":
            "Filters in the time domain can be used without the spectral characterization",
        
        # === TITLES AND HEADERS ===
        "Projeto de Filtros": "Filter Design",
        "Ruídos de alta frequência": "High-frequency noise",
        "Ruídos de baixa frequência": "Low-frequency noise",
        "Ruídos estruturados": "Structured noise",
        "Exercícios de programação": "Programming exercises",
        
        # === COMMON MULTI-WORD PHRASES ===
        "ruído de linha": "line noise",
        "no domínio do tempo": "in the time domain",
        "no domínio da frequência": "in the frequency domain",
        "domínio do tempo": "time domain",
        "domínio da frequência": "frequency domain",
        "podem ser empregados": "can be used",
        "podem ser atenuados": "can be attenuated",
        "Vocês poderão empregar": "You can use",
        "Para algum dos sinais": "For some signals",
        "diferentes filtros": "different filters",
        "alta frequência": "high frequency",
        "baixa frequência": "low frequency",
        "frequência de amostragem": "sampling frequency",
        "foram suficientes": "were sufficient",
        "podem ou não": "may or may not",
        "algo similar": "something similar",
        "Por exemplo": "For example",
       
        # === FILTER TYPES ===
        "filtros passa-baixa": "low-pass filters",
        "filtros passa-alta": "high-pass filters",
        "filtros derivativos": "derivative filters",
        "filtros de Notch": "Notch filters",
        "média sincrona": "synchronous averaging",
        "média móvel": "moving average",
        
        # === NOUNS (Two-word combinations first) ===
        "até mesmo": "even",
        
        # === SINGLE NOUNS ===
        "Projeto": "Project",
        "Filtros": "Filters",
        "prática": "practice",
        "práticas": "practices",
        "programação": "programming",
        "Exercícios": "Exercises",
        "Arquivo": "File",
        "sinais": "signals",
        "sinal": "signal",
        "ruídos": "noises",
        "ruído": "noise",
        "tempo": "time",
        "frequência": "frequency",
        "estruturados": "structured",
        "diferentes": "different",
        
        # === VERBS ===
        "iremos": "we will",
        "irão": "will",
        "utilizar": "use",
        "empregar": "use",
        "comparar": "compare",
        "atenuados": "attenuated",
        "poderão": "can",
        "podem": "can",
        "foram": "were",
        "terão": "will have",
        "terá": "will have",
        
        # === ADJECTIVES & ADVERBS ===
        "tanto": "both",
        "quanto": "as",
        "algo": "something",
        "similar": "similar",
        "suficientes": "sufficient",
        
        # === MISC WORDS ===
        "Contudo": "However",
        "Boa sorte": "Good luck",
    }
    
    # Sort by length (longest first)
    return sorted(trans.items(), key=lambda x: len(x[0]), reverse=True)

def translate_text(text):
    """Translate text using all translation pairs."""
    if not isinstance(text, str):
        return text
    
    result = text
    for pt, en in get_all_translations():
        if pt in result:
            result = result.replace(pt, en)
    
    return result

def process_notebook(input_path):
    """Process a single notebook."""
    with open(input_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Translate all cells
    for cell in notebook.get('cells', []):
        if 'source' in cell:
            if isinstance(cell['source'], list):
                cell['source'] = [translate_text(line) for line in cell['source']]
            else:
                cell['source'] = translate_text(cell['source'])
    
    # Create output with _en suffix
    output_name = input_path.name.replace('.ipynb', '_en.ipynb')
    output_path = input_path.parent / output_name
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)
    
    return output_path

def main():
    assignments_dir = Path('/home/runner/work/BioSignalAndImgProcessing/BioSignalAndImgProcessing/assignments')
    
    notebooks = [
        "Aula_10.ipynb",
        "Aula_12_e_13.ipynb",
        "Aula_17.ipynb",
        "Aula_18.ipynb",
        "Aula_19.ipynb",
        "Aula_20.ipynb",
        "Aula_21.ipynb",
        "Aula_22.ipynb",
        "Aula_23.ipynb",
        "Aula_3.ipynb",
        "Aula_5_e_6.ipynb",
        "Aula_7.ipynb",
        "Aula_8.ipynb",
        "Demonstração_EMG (1).ipynb",
        "Demonstração_EMG.ipynb",
        "Exercícios_de_programação_1.ipynb",
        "Extra_Aula_12_e_13.ipynb",
        "Extra_Processamento_de_Imagens.ipynb",
        "Pratica_3.ipynb",
        "Pratica_de_python_2.ipynb",
        "Pratica_final.ipynb"
    ]
    
    print(f"Final translation pass for {len(notebooks)} notebooks...\n")
    
    for nb_name in notebooks:
        try:
            input_path = assignments_dir / nb_name
            output_path = process_notebook(input_path)
            print(f"  ✓ {nb_name} -> {output_path.name}")
        except Exception as e:
            print(f"  ✗ Error with {nb_name}: {e}")
    
    print("\nFinal translation complete!")

if __name__ == '__main__':
    main()
