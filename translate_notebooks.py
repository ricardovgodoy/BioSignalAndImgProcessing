#!/usr/bin/env python3
"""
Script to translate Portuguese Jupyter notebooks to English.
Creates new files with '_en' suffix.
"""

import json
import os
import re
from pathlib import Path

# Translation dictionary for common terms
TRANSLATIONS = {
    # Common words that appear frequently
    "comparar a performance de diferentes filtros": "compare the performance of different filters",
    "tanto no domínio do tempo quanto da frequência": "both in the time domain and frequency domain",
    "tanto": "both",
    "quanto": "and",
    "contém": "contains",
    "contaminado por artefatos de 60 Hz": "contaminated by 60 Hz artifacts",
    "artefatos de": "artifacts of",
    "provenientes da rede elétrica": "from the electrical network",
    "foi adquirido a": "was acquired at",
    "adquiridos a": "acquired at",
    "e contém ruídos de alta frequência": "and contains high-frequency noise",
    "e frequência de amostragem de": "and sampling frequency of",
    "diversas técnicas de": "various techniques of",
    "filtragem de sinais": "signal filtering",
    "Como vocês se lembram": "As you remember",
    "ou deveriam se lembrar": "or should remember",
    "podem ser empregadas para": "can be used for",
    "o mesmo tipo de problema": "the same type of problem",
    "com filtros passa-baixa": "with low-pass filters",
    "média sincrona": "synchronous averaging",
    "e até mesmo": "and even",
    "média móvel": "moving average",
    "com filtros derivativos e filtros passa-alta": "with derivative filters and high-pass filters",
    "com filtros derivativos": "with derivative filters",
    "filtros passa-alta": "high-pass filters",
    "filtros passa-baixa": "low-pass filters",
    "ou ruído de linha": "or line noise",
    "com Notch filters": "with Notch filters",
    "Os filtros no domínio do tempo": "Filters in the time domain",
    "podem ser empregados sem que": "can be used without",
    "a caracterização espectral do sinal e do ruído seja necessária": "the spectral characterization of the signal and noise being necessary",
    "do sinal e do ruído": "of the signal and noise",
    "seja necessária": "being necessary",
    "estes filtros não são projetados para": "these filters are not designed to",
    "processar frequências específicas": "process specific frequencies",
    "podemos usar filtros no domínio da frequência": "we can use filters in the frequency domain",
    "aplicar filtros para cada um dos sinais de ECG": "apply filters for each of the ECG signals",
    "para cada um dos sinais": "for each of the signals",
    "de ECG": "of ECG",
    "disponíveis": "available",
    "quaisquer um dos filtros e quantos forem necessários": "any of the filters and as many as needed",
    "e quantos forem necessários": "and as many as needed",
    "Para algum dos sinais": "For some signals",
    "serão necessários empregar mais de um tipo de filtro": "it will be necessary to use more than one type of filter",
    "para mais de um tipo de ruído": "for more than one type of noise",
    "A ordem com que você emprega os filtros": "The order in which you use the filters",
    "pode influenciar no resultado final": "can influence the final result",
    "Para descobrir quais filtros usar": "To find out which filters to use",
    "Use eles descomentando": "Use them by uncommenting",
    "e substituindo": "and replacing",
    "por emojis": "by emojis",
    "onde você vai colocar": "where you will place",
    "e deverá ser submetida no Canvas": "and must be submitted on Canvas",
    "neste notebook não ficarão salvas": "to this notebook will not be saved",
    "recomendo que você vá em": "I recommend you go to",
    "Salvar uma cópia no Drive": "Save a copy to Drive",
    "a vontade que elas ficarão salvas": "freely and they will be saved",
    "O arquivo salvo no Drive de vocês": "The saved file in your Drive",
    "provavelmente tem o nome de": "probably has the name",
    "ou algo similar": "or something similar",
    "e talvez esteja dentro de uma pasta chamada": "and may be inside a folder called",
    "A nota é em grupo": "The grade is for the group",
    "mas todos do grupo devem submeter a tarefa": "but everyone in the group must submit the task",
    "Por ser uma atividade em grupo": "As it is a group activity",
    "obviamente o arquivo submetido por integrantes do mesmo grupo será o mesmo": "obviously the file submitted by members of the same group will be the same",
    "por integrantes do mesmo grupo": "by members of the same group",
    "será o mesmo": "will be the same",
    "Contudo": "However",
    "arquivos exatamente iguais para integrantes de grupos diferentes": "exactly identical files for members of different groups",
    "será resultado em nota 0": "will result in a grade of 0",
    "Esta tarefa vale nota de": "This task is worth a grade for",
    "atividade complementar": "complementary activity",
    "Boa sorte": "Good luck",
    
    # More common words
    "de": "of",
    "da": "of the",
    "do": "of the",
    "dos": "of the",
    "das": "of the",
    "para": "for",
    "com": "with",
    "sem": "without",
    "que": "that",
    "ou": "or",
    "e": "and",
    "no": "in the",
    "na": "in the",
    "nos": "in the",
    "nas": "in the",
    "em": "in",
    "por": "by",
    "a": "at",
    
    # Common phrases
    "Clonando": "Cloning",
    "Carrega os dados": "Load the data",
    "Carrega os dados do ECG": "Load ECG data",
    "Carrega os dados ECG": "Load ECG data",
    "Taxa de amostragem": "Sampling rate",
    "Determina o comprimento do sinal": "Determine signal length",
    "Cria o vetor de tempo": "Create time vector",
    "Plota o sinal": "Plot the signal",
    "Plota o sinal ECG": "Plot ECG signal",
    "Frequência de amostragem": "Sampling frequency",
    "Tempo em segundos": "Time in seconds",
    "Tempo (s)": "Time (s)",
    "Sinal ECG Original": "Original ECG Signal",
    "Sinal Original": "Original Signal",
    "Sinal Filtrado": "Filtered Signal",
    "ECG Filtrado": "Filtered ECG",
    "Frequência de Nyquist": "Nyquist frequency",
    "Ordem do filtro": "Filter order",
    "Frequência de corte": "Cutoff frequency",
    "Frequência de corte em Hz": "Cutoff frequency in Hz",
    "Tamanho da janela": "Window size",
    "ajustar conforme necessário": "adjust as needed",
    "Após": "After",
    "Resposta em frequência": "Frequency response",
    "Magnitude (dB)": "Magnitude (dB)",
    "Frequência (Hz)": "Frequency (Hz)",
    "Certifique-se de que": "Make sure that",
    "esteja no diretório de trabalho": "is in the working directory",
    "Frequência que se deseja remover": "Frequency to remove",
    "Fator de qualidade do filtro": "Filter quality factor",
    "determina a largura da faixa rejeitada": "determines the width of the rejected band",
    "Gera os coeficientes do filtro": "Generate filter coefficients",
    "Visualiza a resposta em frequência": "Visualize frequency response",
    "Aplica o filtro": "Apply the filter",
    "Plota o sinal original e o sinal filtrado": "Plot original and filtered signal",
    "para comparação": "for comparison",
    "Prática em python": "Python practice",
    "extração de features": "feature extraction",
    "classificação": "classification",
    "Vamos começar importando": "Let's start by importing",
    "as bibliotecas necessárias": "the necessary libraries",
    "carregando/criando": "loading/creating",
    "algumas imagens de exemplo": "some example images",
    "que usaremos ao longo desta prática": "that we will use throughout this practice",
    "Importações Necessárias": "Necessary Imports",
    "Função Auxiliar": "Helper Function",
    "Plotagem": "Plotting",
    "Criar/Carregar Imagens de Exemplo": "Create/Load Example Images",
    "Imagem para": "Image for",
    "contornos": "contours",
    "descritores": "descriptors",
    "textura": "texture",
    "momentos regionais": "regional moments",
    "usaremos": "we will use",
    "Retângulo": "Rectangle",
    "Adiciona uma parte": "Add a part",
    "Pega o contorno": "Get the contour",
    "Encontrar o maior objeto": "Find the largest object",
    "caso haja múltiplos": "in case there are multiple",
    "descomentando": "uncommenting",
    "Descomente": "Uncomment",
    "substituindo": "replacing",
    "Empregue": "Use",
    "pertinente": "relevant",
    "necessário": "necessary",
    "compare a performance": "compare the performance",
    "Estude a eficacia": "Study the effectiveness",
    "Determine o melhor": "Determine the best",
    "foram suficientes": "were sufficient",
    "Tente empregar": "Try using",
    "eles podem ou não": "they may or may not",
    "vocês irão ter que testar": "you will have to test",
    "seu código final aqui": "your final code here",
    "Fique a vontade": "Feel free",
    "inverter a ordem": "reverse the order",
    "quaisquer outras alterações": "any other changes",
    
    # Headers and titles
    "Projeto de Filtros": "Filter Design",
    "Nesta prática": "In this practice",
    "iremos": "we will",
    "Começamos clonando": "We start by cloning",
    "os arquivos que iremos utilizar": "the files we will use",
    "nessa prática": "in this practice",
    "contém um": "contains a",
    "contém sinais": "contains signals",
    "contém artefatos": "contains artifacts",
    "contaminado por": "contaminated by",
    "provenientes da rede elétrica": "from the electrical network",
    "Este sinal foi adquirido": "This signal was acquired",
    "adquiridos a": "acquired at",
    "Nas últimas aulas": "In the last classes",
    "vocês aprenderam": "you learned",
    "diversas técnicas": "various techniques",
    "filtragem de sinais": "signal filtering",
    "ou deveriam se lembrar": "or should remember",
    "podem ser empregadas": "can be used",
    "para o mesmo tipo de problema": "for the same type of problem",
    "Por exemplo": "For example",
    "Ruídos de alta frequência": "High-frequency noise",
    "podem ser atenuados": "can be attenuated",
    "Ruídos de baixa frequência": "Low-frequency noise",
    "Ruídos estruturados": "Structured noise",
    "ruído de linha": "line noise",
    "filtros de Notch": "Notch filters",
    "no domínio do tempo": "in the time domain",
    "podem ser empregados sem": "can be used without",
    "a caracterização espectral": "spectral characterization",
    "seja necessária": "is necessary",
    "Contudo": "However",
    "estes filtros não são projetados": "these filters are not designed",
    "para processar": "to process",
    "frequências específicas": "specific frequencies",
    "Para estes fins": "For these purposes",
    "podemos usar filtros": "we can use filters",
    "no domínio da frequência": "in the frequency domain",
    "voces irão aplicar": "you will apply",
    "para cada um dos sinais": "for each of the signals",
    "disponíveis": "available",
    "Vocês poderão empregar": "You can use",
    "quaisquer um dos filtros": "any of the filters",
    "quantos forem necessários": "as many as needed",
    "Para algum dos sinais": "For some signals",
    "serão necessários empregar": "it will be necessary to use",
    "mais de um tipo de filtro": "more than one type of filter",
    "A ordem com que você emprega": "The order in which you use",
    "os filtros pode influenciar": "the filters can influence",
    "no resultado final": "the final result",
    "Para descobrir quais filtros usar": "To find out which filters to use",
    "vocês terão que testar": "you will have to test",
    "eu vou deixar implementado": "I will leave implemented",
    "todos os filtros": "all filters",
    "a linha pertinente": "the relevant line",
    "os parâmetros necessários": "the necessary parameters",
    "que estarão indicados": "which will be indicated",
    "A primeira célula contém": "The first cell contains",
    "tudo que vocês precisam": "everything you need",
    "Podem usar ela como rascunho": "You can use it as a draft",
    "para testar implementações": "to test implementations",
    "Na segunda célula": "In the second cell",
    "é sua resposta final": "is your final answer",
    "ontem você vai colocar": "where you will place",
    "o código final": "the final code",
    "limpo e organizado": "clean and organized",
    "Lembrando que": "Remember that",
    "esta prática vale nota": "this practice is graded",
    "deverá ser submetida": "must be submitted",
    "Quaisquer alterações que você fizer": "Any changes you make",
    "neste notebook": "to this notebook",
    "não ficarão salvas": "will not be saved",
    "Portanto": "Therefore",
    "recomendo que você vá": "I recommend you go",
    "Arquivo": "File",
    "Salvar uma cópia": "Save a copy",
    "Agora sim você pode fazer alterações": "Now you can make changes",
    "a vontade": "freely",
    "que elas ficarão salvas": "and they will be saved",
    "O arquivo salvo": "The saved file",
    "provavelmente tem o nome": "probably has the name",
    "ou algo similar": "or something similar",
    "talvez esteja dentro de uma pasta": "may be inside a folder",
    "chamada": "called",
    "A nota é em grupo": "The grade is for the group",
    "mas todos do grupo devem submeter": "but everyone in the group must submit",
    "a tarefa": "the task",
    "Por ser uma atividade em grupo": "As it is a group activity",
    "obviamente o arquivo submetido": "obviously the file submitted",
    "por integrantes do mesmo grupo": "by members of the same group",
    "será o mesmo": "will be the same",
    "arquivos exatamente iguais": "exactly identical files",
    "para integrantes de grupos diferentes": "for members of different groups",
    "será resultado em nota": "will result in a grade of",
    "Esta tarefa vale nota": "This task is worth a grade",
    "atividade complementar": "complementary activity",
    "Boa sorte": "Good luck",
    
    # Specific instructions
    "Lidando com artefato": "Dealing with artifact",
    "artefato de baixa frequência": "low-frequency artifact",
    "artefato de alta frequência": "high-frequency artifact",
    "ruídos estruturados de rede": "structured network noise",
    "no sinal do arquivo": "in the signal from file",
    "técnicas de filtragem de dados": "data filtering techniques",
    "para remover os ruídos": "to remove the noise",
    "Lembrande que": "Remember that",
    "Diversas opções de filtros": "Various filter options",
    "estão disponíveis": "are available",
    "comentadas no código": "commented in the code",
    "a que voce achar": "the one you find",
    "mais de uma se necessário": "more than one if necessary",
    "Dica": "Tip",
    "implemente filtros de ordem": "implement filters of order",
    "com frequências de corte de": "with cutoff frequencies of",
    "em remover o ruído": "in removing the noise",
    "o seu efeito": "its effect",
    "nas ondas de ECG": "on ECG waves",
    "apenas filtros para remover ruído": "only filters to remove noise",
    "também ruídos": "also noise",
    "ruídos aleatórios": "random noise",
    "melhora o sinal": "improve the signal",
    "Plot do sinal original": "Original signal plot",
    "Plot do sinal final": "Final signal plot",
    "após filtragens": "after filtering",
    "Escolher entre os seguintes filtros": "Choose from the following filters",
    "Esse filtro": "This filter",
    "realça as variações rápidas": "emphasizes rapid variations",
    "podendo atenuar tendências": "which can attenuate trends",
    "o uso de": "the use of",
    "reduz o tamanho do sinal": "reduces signal size",
    "Uma alternativa é usar": "An alternative is to use",
    "para manter o tamanho": "to keep the size",
    "remove componentes": "removes components",
    "de forma mais controlada": "in a more controlled way",
    "Uma abordagem simples": "A simple approach",
    "suavização do sinal": "signal smoothing",
    "preservando as características": "preserving the characteristics",
    "Remove tendências": "Remove trends",
    "variações lentas no sinal": "slow variations in the signal",
    "descomente o código abaixo": "uncomment the code below",
    "para plotar": "to plot",
    "Abaixo": "Below",
    "copie e cole": "copy and paste",
    "do seu filtro": "of your filter",
    "propor": "propose",
    "de uso dos filtros": "of filter usage",
    "Devem escolher": "You must choose",
    "entre as opções abaixo": "from the options below",
    "descomente a desejada": "uncomment the desired one",
    "Opção": "Option",
    "Remove componentes de alta frequência": "Removes high-frequency components",
    "Suaviza o sinal": "Smooths the signal",
    "atenua ruídos": "attenuates noise",
    "após a filtragem": "after filtering",
    "após a remoção": "after removal",
    "pode ser interessante": "may be interesting",
    "Novamente": "Again",
    "escolher entre": "choose between",
    "as opções": "the options",
    "acharem melhor": "find better",
    "pode ser necessário": "may be necessary",
    "devem escolher": "must choose",
    "Remove componentes de baixa frequência": "Removes low-frequency components",
    "de forma controlada": "in a controlled way",
    "Projeto do filtro": "Filter design",
    "para remover o ruído": "to remove the noise",
    "largura da faixa rejeitada": "width of rejected band",
    "coeficientes do filtro": "filter coefficients",
    "ao sinal": "to the signal",
    "Só existe uma frequência possível": "There is only one possible frequency",
    "para o parâmetro da frequência": "for the frequency parameter",
    
    # Use or not use warnings
    "USE OU": "USE EITHER",
    "NÃO USE OS DOIS DE UMA VEZ": "DO NOT USE BOTH AT ONCE",
    "FILTROS PASSA-ALTA": "HIGH-PASS FILTERS",
    "FILTROS DERIVATIVOS": "DERIVATIVE FILTERS",
    "FILTROS PASSA-BAIXA": "LOW-PASS FILTERS",
    "FILTROS MÉDIA MÓVEL": "MOVING AVERAGE FILTERS",
}

def translate_text(text):
    """Translate Portuguese text to English."""
    if not isinstance(text, str):
        return text
    
    result = text
    
    # Sort by length (longest first) to avoid partial matches
    for pt, en in sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(pt, en)
    
    return result

def translate_notebook(input_path, output_path):
    """Translate a Jupyter notebook from Portuguese to English."""
    print(f"Translating {input_path} -> {output_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Translate cells
    for cell in notebook.get('cells', []):
        if cell['cell_type'] == 'markdown':
            # Translate markdown content
            if 'source' in cell:
                if isinstance(cell['source'], list):
                    cell['source'] = [translate_text(line) for line in cell['source']]
                else:
                    cell['source'] = translate_text(cell['source'])
        
        elif cell['cell_type'] == 'code':
            # Translate comments in code
            if 'source' in cell:
                translated_source = []
                if isinstance(cell['source'], list):
                    for line in cell['source']:
                        translated_source.append(translate_code_line(line))
                    cell['source'] = translated_source
                else:
                    cell['source'] = translate_code_line(cell['source'])
    
    # Save translated notebook
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ Completed")

def translate_code_line(line):
    """Translate comments in a code line, preserving code."""
    if '#' not in line:
        return line
    
    # Split on first # to separate code from comment
    parts = line.split('#', 1)
    if len(parts) == 2:
        code_part = parts[0]
        comment_part = parts[1]
        return code_part + '#' + translate_text(comment_part)
    return line

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
    
    print(f"Starting translation of {len(notebooks)} notebooks...\n")
    
    for notebook_name in notebooks:
        input_path = assignments_dir / notebook_name
        # Create output filename with _en suffix
        output_name = notebook_name.replace('.ipynb', '_en.ipynb')
        output_path = assignments_dir / output_name
        
        try:
            translate_notebook(input_path, output_path)
        except Exception as e:
            print(f"  ✗ Error translating {notebook_name}: {e}")
    
    print(f"\nTranslation complete!")

if __name__ == '__main__':
    main()
