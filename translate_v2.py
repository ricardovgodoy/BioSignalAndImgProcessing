#!/usr/bin/env python3
"""
Enhanced script to translate Portuguese Jupyter notebooks to English.
Creates new files with '_en' suffix.
"""

import json
import os
import re
from pathlib import Path

# Comprehensive translation dictionary - order matters (longest first)
TRANSLATIONS = [
    # Long phrases first to avoid partial matches
    ("comparar a performance de diferentes filtros, tanto no domínio do tempo quanto da frequência", 
     "compare the performance of different filters, both in the time domain and frequency domain"),
    ("a caracterização espectral do sinal e do ruído seja necessária", 
     "the spectral characterization of the signal and noise is necessary"),
    ("quaisquer um dos filtros e quantos forem necessários", 
     "any of the filters and as many as needed"),
    ("serão necessários empregar mais de um tipo de filtro para mais de um tipo de ruído", 
     "it will be necessary to use more than one type of filter for more than one type of noise"),
    ("obviamente o arquivo submetido por integrantes do mesmo grupo será o mesmo", 
     "obviously the file submitted by members of the same group will be the same"),
    ("arquivos exatamente iguais para integrantes de grupos diferentes será resultado em nota 0", 
     "exactly identical files for members of different groups will result in a grade of 0"),
    ("A ordem com que você emprega os filtros pode influenciar no resultado final", 
     "The order in which you use the filters can influence the final result"),
    ("O arquivo salvo no Drive de vocês provavelmente tem o nome de", 
     "The saved file in your Drive probably has the name"),
    ("e talvez esteja dentro de uma pasta chamada", 
     "and may be inside a folder called"),
    ("mas todos do grupo devem submeter a tarefa", 
     "but everyone in the group must submit the task"),
    ("Por ser uma atividade em grupo", 
     "As it is a group activity"),
    ("Quaisquer alterações que você fizer neste notebook não ficarão salvas", 
     "Any changes you make to this notebook will not be saved"),
    ("Agora sim você pode fazer alterações a vontade que elas ficarão salvas", 
     "Now you can make changes freely and they will be saved"),
    ("Como vocês se lembram, ou deveriam se lembrar", 
     "As you remember, or should remember"),
    
    # Specific technical phrases
    ("contaminado por artefatos de 60 Hz provenientes da rede elétrica", 
     "contaminated by 60 Hz artifacts from the electrical network"),
    ("contém sinais de ECG adquiridos a 1000 Hz e contém ruídos de alta frequência", 
     "contains ECG signals acquired at 1000 Hz and contains high-frequency noise"),
    ("contém artefatos de baixa frequência e frequência de amostragem de 1000 Hz", 
     "contains low-frequency artifacts and sampling frequency of 1000 Hz"),
    ("Este sinal foi adquirido a 200 Hz", 
     "This signal was acquired at 200 Hz"),
    ("adquiridos a 1000 Hz", 
     "acquired at 1000 Hz"),
    
    # Instruction phrases
    ("Começamos clonando os arquivos que iremos utilizar nessa prática", 
     "We start by cloning the files we will use in this practice"),
    ("Nas últimas aulas, vocês aprenderam diversas técnicas de filtragem de sinais", 
     "In the last classes, you learned various techniques for signal filtering"),
    ("podem ser empregadas para o mesmo tipo de problema", 
     "can be used for the same type of problem"),
    ("Os filtros no domínio do tempo podem ser empregados sem que a caracterização espectral do sinal e do ruído seja necessária", 
     "Filters in the time domain can be used without the spectral characterization of the signal and noise being necessary"),
    ("Contudo, estes filtros não são projetados para processar frequências específicas", 
     "However, these filters are not designed to process specific frequencies"),
    ("Para estes fins, podemos usar filtros no domínio da frequência", 
     "For these purposes, we can use filters in the frequency domain"),
    ("Nesta prática, voces irão aplicar filtros para cada um dos sinais de ECG disponíveis", 
     "In this practice, you will apply filters for each of the available ECG signals"),
    ("Vocês poderão empregar quaisquer um dos filtros e quantos forem necessários", 
     "You can use any of the filters and as many as needed"),
    ("Para descobrir quais filtros usar, vocês terão que testar", 
     "To find out which filters to use, you will have to test"),
    ("Nesta prática, eu vou deixar implementado todos os filtros", 
     "In this practice, I will leave all filters implemented"),
    ("Empregue eles descomentando a linha pertinente e substituindo os parâmetros necessários, que estarão indicados por emojis", 
     "Use them by uncommenting the relevant line and replacing the necessary parameters, which will be indicated by emojis"),
    ("A primeira célula contém tudo que vocês precisam", 
     "The first cell contains everything you need"),
    ("Podem usar ela como rascunho para testar implementações", 
     "You can use it as a draft to test implementations"),
    ("Na segunda célula é sua resposta final, ontem você vai colocar o código final, limpo e organizado", 
     "In the second cell is your final answer, where you will place the final code, clean and organized"),
    ("Lembrando que esta prática vale nota, e deverá ser submetida no Canvas", 
     "Remember that this practice is graded and must be submitted on Canvas"),
    ("Portanto, recomendo que você vá em", 
     "Therefore, I recommend you go to"),
    ("A nota é em grupo", 
     "The grade is for the group"),
    ("Esta tarefa vale nota de atividade complementar", 
     "This task is worth a grade for complementary activity"),
    
    # Filter-related phrases
    ("Ruídos de alta frequência podem ser atenuados com filtros passa-baixa, média sincrona, e até mesmo média móvel", 
     "High-frequency noise can be attenuated with low-pass filters, synchronous averaging, and even moving average"),
    ("Ruídos de baixa frequência podem ser atenuados com filtros derivativos e filtros passa-alta", 
     "Low-frequency noise can be attenuated with derivative filters and high-pass filters"),
    ("Ruídos estruturados ou ruído de linha podem ser atenuados com filtros de Notch", 
     "Structured noise or line noise can be attenuated with Notch filters"),
    
    # Section headers
    ("Lidando com artefato de baixa frequência no sinal do arquivo", 
     "Dealing with low-frequency artifact in the signal from file"),
    ("Lidando com artefato de alta frequência no sinal do arquivo", 
     "Dealing with high-frequency artifact in the signal from file"),
    ("Lidando com ruídos estruturados de rede (60 Hz) do arquivo", 
     "Dealing with structured network noise (60 Hz) from file"),
    
    # Instructions
    ("Empregue técnicas de filtragem de dados para remover os ruídos de baixa frequência do sinal", 
     "Use data filtering techniques to remove low-frequency noise from the signal"),
    ("Empregue técnicas de filtragem de dados para remover os ruídos de alta frequência do sinal", 
     "Use data filtering techniques to remove high-frequency noise from the signal"),
    ("Empregue técnicas de filtragem de dados para remover os ruídos de ruído de rede (60 Hz)", 
     "Use data filtering techniques to remove network noise (60 Hz)"),
    ("Diversas opções de filtros estão disponíveis e comentadas no código", 
     "Various filter options are available and commented in the code"),
    ("Descomente a que voce achar pertinente substituindo os parâmetros que estão indicados por emojis", 
     "Uncomment the one you find relevant replacing the parameters indicated by emojis"),
    ("Empregue mais de uma se necessário", 
     "Use more than one if necessary"),
    ("compare a performance a performance de filtros derivativos com filtros passa-alta", 
     "compare the performance of derivative filters with high-pass filters"),
    ("compare a performance a performance de filtros filtros passa-baixa com filtros de média móvel", 
     "compare the performance of low-pass filters with moving average filters"),
    ("implemente filtros de ordem 2 a 8, com frequências de corte de 0.5 a 5 Hz", 
     "implement filters of order 2 to 8, with cutoff frequencies from 0.5 to 5 Hz"),
    ("Estude a eficacia dos filtros em remover o ruído de base e o seu efeito nas ondas de ECG", 
     "Study the effectiveness of filters in removing baseline noise and its effect on ECG waves"),
    ("Estude a eficacia dos filtros em remover o ruído de alta frequência e o seu efeito nas ondas de ECG", 
     "Study the effectiveness of filters in removing high-frequency noise and its effect on ECG waves"),
    ("Determine o melhor", 
     "Determine the best"),
    ("apenas filtros para remover ruído de baixa frequência foram suficientes", 
     "only filters to remove low-frequency noise were sufficient"),
    ("apenas filtros para remover ruído de alta frequência foram suficientes", 
     "only filters to remove high-frequency noise were sufficient"),
    ("Tente empregar mais filtros para remover também ruídos aleatórios de alta frequência", 
     "Try using more filters to also remove random high-frequency noise"),
    ("Tente empregar mais filtros para remover também ruídos de baixa frequência", 
     "Try using more filters to also remove low-frequency noise"),
    ("eles podem ou não melhora o sinal, vocês irão ter que testar", 
     "they may or may not improve the signal, you will have to test"),
    ("Abaixo, copie e cole o código final do seu filtro", 
     "Below, copy and paste the final code of your filter"),
    ("Fique a vontade para propor inverter a ordem de uso dos filtros ou quaisquer outras alterações", 
     "Feel free to propose reversing the order of filter usage or any other changes"),
    
    # Common instructions
    ("Lembrande que", "Remember that"),
    ("Dica", "Tip"),
    ("seu código final aqui", "your final code here"),
    ("Só existe uma frequência possível para o parâmetro da frequência", 
     "There is only one possible frequency for the frequency parameter"),
    
    # Code comments - filtering
    ("Carrega os dados do ECG a partir do arquivo", 
     "Load ECG data from the file"),
    ("Carrega os dados ECG a partir do arquivo", 
     "Load ECG data from the file"),
    ("Taxa de amostragem (Hz)", 
     "Sampling rate (Hz)"),
    ("Taxa de amostragem em Hz", 
     "Sampling rate in Hz"),
    ("Taxa de amostragem = 1000 Hz", 
     "Sampling rate = 1000 Hz"),
    ("Taxa de amostragem = 200 Hz", 
     "Sampling rate = 200 Hz"),
    ("Determina o comprimento do sinal", 
     "Determine signal length"),
    ("Determina o comprimento do sinal e cria o vetor de tempo", 
     "Determine signal length and create time vector"),
    ("Cria o vetor de tempo similar ao MATLAB", 
     "Create time vector similar to MATLAB"),
    ("Cria o vetor de tempo", 
     "Create time vector"),
    ("Vetor de tempo", 
     "Time vector"),
    ("Plota o sinal ECG", 
     "Plot ECG signal"),
    ("Plota o sinal", 
     "Plot the signal"),
    ("Plot do sinal original", 
     "Original signal plot"),
    ("Plot do sinal final após filtragens de baixa frequência", 
     "Final signal plot after low-frequency filtering"),
    ("Plot do sinal após a filtragem de alta frequência", 
     "Signal plot after high-frequency filtering"),
    ("Plot do sinal após a filtragem", 
     "Signal plot after filtering"),
    ("descomente o código abaixo para plotar", 
     "uncomment the code below to plot"),
    
    # Filter descriptions
    ("FILTRAGEM DE RUÍDOS DE BAIXA FREQUÊNCIA", 
     "LOW-FREQUENCY NOISE FILTERING"),
    ("FILTRAGEM DE RUÍDOS DE ALTA FREQUÊNCIA", 
     "HIGH-FREQUENCY NOISE FILTERING"),
    ("Escolher entre os seguintes filtros, descomentando a opção desejada", 
     "Choose from the following filters, uncommenting the desired option"),
    ("Filtro derivativo", 
     "Derivative filter"),
    ("Esse filtro realça as variações rápidas, podendo atenuar tendências de baixa frequência", 
     "This filter emphasizes rapid variations, which can attenuate low-frequency trends"),
    ("o uso de np.diff reduz o tamanho do sinal", 
     "the use of np.diff reduces the signal size"),
    ("Uma alternativa é usar 'prepend' para manter o tamanho", 
     "An alternative is to use 'prepend' to keep the size"),
    ("Descomente aqui se você quiser usar filtros derivativos", 
     "Uncomment here if you want to use derivative filters"),
    ("Descomente aqui se você quiser usar filtros passa-alta", 
     "Uncomment here if you want to use high-pass filters"),
    ("Descomente aqui se você quiser usar filtros passa-baixa", 
     "Uncomment here if you want to use low-pass filters"),
    ("Descomente aqui se quiser usar filtros Butterworth passa-baixa", 
     "Uncomment here if you want to use Butterworth low-pass filters"),
    ("Descomente aqui se você quiser usar filtros média móvel", 
     "Uncomment here if you want to use moving average filters"),
    ("Filtro Butterworth passa-alta", 
     "Butterworth high-pass filter"),
    ("Filtro Butterworth passa-baixa", 
     "Butterworth low-pass filter"),
    ("Esse filtro remove componentes de baixa frequência de forma mais controlada", 
     "This filter removes low-frequency components in a more controlled way"),
    ("Ordem do filtro", 
     "Filter order"),
    ("Ordem do filtro passa-baixa", 
     "Low-pass filter order"),
    ("Frequência de corte em Hz", 
     "Cutoff frequency in Hz"),
    ("ajustar conforme necessário", 
     "adjust as needed"),
    ("Frequência de Nyquist", 
     "Nyquist frequency"),
    ("Média móvel", 
     "Moving average"),
    ("Uma abordagem simples para suavização do sinal", 
     "A simple approach for signal smoothing"),
    ("Tamanho da janela; ajustar conforme necessário", 
     "Window size; adjust as needed"),
    ("Tamanho da janela", 
     "Window size"),
    ("Após a remoção dos ruídos de baixa frequência, pode ser interessante filtrar ruídos de alta frequência", 
     "After removing low-frequency noise, it may be interesting to filter high-frequency noise"),
    ("Após a filtragem de alta frequência, pode ser necessário remover ruídos de baixa frequência", 
     "After high-frequency filtering, it may be necessary to remove low-frequency noise"),
    ("Novamente, escolher entre as opções descomentando a que acharem melhor", 
     "Again, choose from the options uncommenting the one you find better"),
    ("devem escolher entre as opções abaixo (descomente a desejada)", 
     "must choose from the options below (uncomment the desired one)"),
    ("Devem escolher entre as opções abaixo (descomente a desejada)", 
     "Must choose from the options below (uncomment the desired one)"),
    ("Remove ruídos de alta frequência preservando as características do sinal", 
     "Removes high-frequency noise preserving signal characteristics"),
    ("Remove componentes de alta frequência do sinal", 
     "Removes high-frequency components from the signal"),
    ("Remove componentes de baixa frequência de forma controlada", 
     "Removes low-frequency components in a controlled way"),
    ("Filtro derivativo simples", 
     "Simple derivative filter"),
    ("Remove tendências e variações lentas no sinal", 
     "Remove trends and slow variations in the signal"),
    ("Suaviza o sinal e atenua ruídos de alta frequência", 
     "Smooths the signal and attenuates high-frequency noise"),
    ("Opção", 
     "Option"),
    
    # Notch filter specific
    ("Projeto do filtro notch para remover o ruído de 60 Hz", 
     "Notch filter design to remove 60 Hz noise"),
    ("Frequência que se deseja remover (Hz)", 
     "Frequency to remove (Hz)"),
    ("Fator de qualidade do filtro (determina a largura da faixa rejeitada)", 
     "Filter quality factor (determines the width of the rejected band)"),
    ("Gera os coeficientes do filtro notch", 
     "Generate notch filter coefficients"),
    ("Visualiza a resposta em frequência do filtro", 
     "Visualize filter frequency response"),
    ("Resposta em frequência do filtro notch", 
     "Notch filter frequency response"),
    ("Aplica o filtro ao sinal de ECG", 
     "Apply the filter to the ECG signal"),
    ("Plota o sinal original e o sinal filtrado para comparação", 
     "Plot original and filtered signal for comparison"),
    ("Certifique-se de que 'ecg2x60.dat' esteja no diretório de trabalho", 
     "Make sure 'ecg2x60.dat' is in the working directory"),
    
    # Plot labels
    ("Tempo em segundos", "Time in seconds"),
    ("Tempo (s)", "Time (s)"),
    ("Sinal ECG Original", "Original ECG Signal"),
    ("Sinal ECG Após Filtragem (Baixa Frequência)", 
     "ECG Signal After Filtering (Low Frequency)"),
    ("Sinal ECG Após Filtragem (Alta Frequência)", 
     "ECG Signal After Filtering (High Frequency)"),
    ("Sinal ECG Após Filtragem (Baixa e Alta Frequência)", 
     "ECG Signal After Filtering (Low and High Frequency)"),
    ("Sinal ECG Após Filtragem (Alta e Baixa Frequência)", 
     "ECG Signal After Filtering (High and Low Frequency)"),
    ("Sinal Original", "Original Signal"),
    ("Sinal Filtrado", "Filtered Signal"),
    ("ECG Filtrado", "Filtered ECG"),
    ("Frequência (Hz)", "Frequency (Hz)"),
    ("Magnitude (dB)", "Magnitude (dB)"),
    
    # Warnings with emojis
    ("USE OU FILTROS PASSA-ALTA OU FILTROS DERIVATIVOS, NÃO USE OS DOIS DE UMA VEZ", 
     "USE EITHER HIGH-PASS FILTERS OR DERIVATIVE FILTERS, DO NOT USE BOTH AT ONCE"),
    ("USE OU FILTROS PASSA-BAIXA OU FILTROS MÉDIA MÓVEL, NÃO USE OS DOIS DE UMA VEZ", 
     "USE EITHER LOW-PASS FILTERS OR MOVING AVERAGE FILTERS, DO NOT USE BOTH AT ONCE"),
    
    # General imports and setup
    ("Importações Necessárias", "Necessary Imports"),
    ("Função Auxiliar de Plotagem", "Helper Plotting Function"),
    ("Criar/Carregar Imagens de Exemplo", "Create/Load Example Images"),
    ("Imagem para contornos e descritores", "Image for contours and descriptors"),
    ("Imagem para textura e momentos regionais (usaremos a do cérebro)", 
     "Image for texture and regional moments (we will use the brain)"),
    ("Retângulo", "Rectangle"),
    ("Adiciona uma parte para forma em L", "Add a part for L shape"),
    ("Pega o contorno do maior objeto", "Get the contour of the largest object"),
    ("Encontrar o maior objeto (caso haja múltiplos desconectados)", 
     "Find the largest object (in case there are multiple disconnected)"),
    
    # Practice titles
    ("Prática em python 3: extração de features e classificação", 
     "Python practice 3: feature extraction and classification"),
    ("Vamos começar importando as bibliotecas necessárias e carregando/criando algumas imagens de exemplo que usaremos ao longo desta prática", 
     "Let's start by importing the necessary libraries and loading/creating some example images that we will use throughout this practice"),
    
    # Short common words (last to avoid over-matching)
    ("contém um ecg", "contains an ECG"),
    ("contém sinais", "contains signals"),
    ("contém artefatos", "contains artifacts"),
    (" e ", " and "),
    (" ou ", " or "),
    (" de ", " of "),
    (" da ", " of the "),
    (" do ", " of the "),
    (" dos ", " of the "),
    (" das ", " of the "),
    (" para ", " for "),
    (" com ", " with "),
    (" sem ", " without "),
    (" que ", " that "),
    (" no ", " in the "),
    (" na ", " in the "),
    (" nos ", " in the "),
    (" nas ", " in the "),
    (" em ", " in "),
    (" por ", " by "),
    (" a ", " at "),
]

def translate_text(text):
    """Translate Portuguese text to English using pattern matching."""
    if not isinstance(text, str):
        return text
    
    result = text
    
    # Apply all translations in order (longest first already)
    for pt, en in TRANSLATIONS:
        result = result.replace(pt, en)
    
    return result

def translate_code_line(line):
    """Translate comments in a code line, preserving code."""
    if '#' not in line:
        return line
    
    # Find all # positions
    parts = []
    current_pos = 0
    
    while True:
        hash_pos = line.find('#', current_pos)
        if hash_pos == -1:
            parts.append(('code', line[current_pos:]))
            break
        
        # Add code part
        if hash_pos > current_pos:
            parts.append(('code', line[current_pos:hash_pos]))
        
        # Find end of line or next hash
        next_hash = line.find('#', hash_pos + 1)
        if next_hash == -1:
            # Rest is comment
            parts.append(('comment', line[hash_pos:]))
            break
        else:
            # Comment until newline (if multi-line)
            newline = line.find('\n', hash_pos)
            if newline != -1 and newline < next_hash:
                parts.append(('comment', line[hash_pos:newline+1]))
                current_pos = newline + 1
            else:
                parts.append(('comment', line[hash_pos:next_hash]))
                current_pos = next_hash
    
    # Reconstruct line
    result = ''
    for part_type, part_text in parts:
        if part_type == 'comment':
            result += translate_text(part_text)
        else:
            result += part_text
    
    return result

def translate_notebook(input_path, output_path):
    """Translate a Jupyter notebook from Portuguese to English."""
    print(f"Translating {input_path.name}...")
    
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
                if isinstance(cell['source'], list):
                    cell['source'] = [translate_code_line(line) for line in cell['source']]
                else:
                    cell['source'] = translate_code_line(cell['source'])
    
    # Save translated notebook
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ Completed")

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
            import traceback
            traceback.print_exc()
    
    print(f"\nTranslation complete! Created {len(notebooks)} English versions.")

if __name__ == '__main__':
    main()
