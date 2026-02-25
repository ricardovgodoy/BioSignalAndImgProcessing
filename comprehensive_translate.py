#!/usr/bin/env python3
"""
Comprehensive Portuguese to English translation for Jupyter notebooks.
Translates markdown cells, code comments, and string literals while preserving variable names.
"""

import json
import re
from pathlib import Path

def get_comprehensive_translations():
    """
    Returns a comprehensive translation dictionary.
    Organized by priority: longest/most specific phrases first.
    """
    return {
        # === COMPLETE SENTENCES AND LONG PHRASES ===
        "Nesta prática, iremos comparar a performance de diferentes filtros, tanto no domínio do tempo quanto da frequência":
            "In this practice, we will compare the performance of different filters, both in the time domain and frequency domain",
        "Ruídos de alta frequência podem ser atenuados com filtros passa-baixa, média sincrona, e até mesmo média móvel":
            "High-frequency noise can be attenuated with low-pass filters, synchronous averaging, and even moving average",
        "Ruídos de baixa frequência podem ser atenuados com filtros derivativos e filtros passa-alta":
            "Low-frequency noise can be attenuated with derivative filters and high-pass filters",
        "Ruídos estruturados ou ruído de linha podem ser atenuados com filtros de Notch":
            "Structured noise or line noise can be attenuated with Notch filters",
        "Os filtros no domínio do tempo podem ser empregados sem que a caracterização espectral":
            "Filters in the time domain can be used without spectral characterization",
        "Vocês poderão empregar qualquer filtro no domínio do tempo ou da frequência":
            "You can use any filter in the time or frequency domain",
        "Como vocês se lembram, ou deveriam se lembrar, diversas técnicas podem ser empregadas para o mesmo tipo de problema":
            "As you remember, or should remember, various techniques can be used for the same type of problem",
        "Para descobrir quais filtros usar, vocês terão que testar":
            "To find out which filters to use, you will have to test",
        "Construir um sistema simplificado que possa extrair características de imagens de células sanguíneas":
            "Build a simplified system that can extract features from blood cell images",
        "Abaixo, copie e cole o código final do seu filtro":
            "Below, copy and paste the final code for your filter",
        
        # === TITLES AND SECTION HEADERS ===
        "Prática em Python: Sistema para Classificação de Células Sanguíneas": 
            "Python Practice: System for Blood Cell Classification",
        "Explicação do Código para Tipos de Sinais Discreto": "Code Explanation for Discrete Signal Types",
        "Explicação do Código de Sistema Atraso e Avanço Ideal": "Code Explanation for Ideal Delay and Advance System",
        "Explicação do Código para Exemplificar Amostragem Periódica": "Code Explanation to Exemplify Periodic Sampling",
        "Geração do Eixo Temporal": "Generation of Time Axis",
        "Geração do Sinal Contínuo": "Continuous Signal Generation",
        "Criação dos Sinais Discretos": "Creation of Discrete Signals",
        "Impulso Unitário": "Unit Impulse",
        "Degrau Unitário": "Unit Step",
        "O que será mostrado nos gráficos": "What will be shown in the graphs",
        "O primeiro plot mostra o EMG, o segundo seu envelope": 
            "The first plot shows the EMG, the second its envelope",
        "e o terceiro mostra o": "and the third shows the",
        "irá baixar os dados e preparar as": "will download the data and prepare the",
        "Projeto de Filtros": "Filter Design",
        "Processamento de Imagens": "Image Processing",
        "Exercícios de programação": "Programming Exercises",
        "Exercício Final e Discussão": "Final Exercise and Discussion",
        "Prática de Python": "Python Practice",
        "Demonstração": "Demonstration",
        "Prática Final": "Final Practice",
        "Parte 0: Configuração e Carregamento de Dados": "Part 0: Setup and Data Loading",
        "Instruções Gerai": "General Instructions",
        "Explicação Breve": "Brief Explanation",
        "Como o Código Funciona": "How the Code Works",
        "Interpretando os Resultados": "Interpreting the Results",
        "Matriz de Confusão": "Confusion Matrix",
        "Discussão": "Discussion",
        "Conclusão": "Conclusion",
        "Carregamento e taxa de amostragem": "Loading and sampling rate",
        "Definição das janelas": "Window definition",
        "Cálculo do RMS": "RMS Calculation",
        
        # === COMMON TECHNICAL PHRASES ===
        "divide em conjuntos de treino e teste": "splits into training and test sets",
        "contém um ECG contaminado por artefatos de 60 Hz provenientes da rede elétrica":
            "contains an ECG contaminated by 60 Hz artifacts from the electrical grid",
        "Este sinal foi adquirido a": "This signal was acquired at",
        "representa dois ciclos respiratórios de um cachorro adquiridos empregando eletrodos posicionados próximos ao diafragma do animal":
            "represents two respiratory cycles of a dog acquired using electrodes positioned near the animal's diaphragm",
        "O primeiro plot mostra o EMG, o segundo seu envelope (atividade), e o terceiro mostra o fluxo de ar":
            "The first plot shows the EMG, the second its envelope (activity), and the third shows the air flow",
        "tanto no domínio do tempo quanto da frequência": "both in the time domain and frequency domain",
        "no domínio do tempo": "in the time domain",
        "no domínio da frequência": "in the frequency domain",
        "domínio do tempo": "time domain",
        "domínio da frequência": "frequency domain",
        "ruído de linha": "line noise",
        "ruídos de alta frequência": "high-frequency noise",
        "ruídos de baixa frequência": "low-frequency noise",
        "ruídos estruturados": "structured noise",
        "frequência de amostragem": "sampling frequency",
        "taxa de amostragem": "sampling rate",
        "sinal discreto": "discrete signal",
        "sinais discretos": "discrete signals",
        "sinal senoidal": "sinusoidal signal",
        "sinal contínuo": "continuous signal",
        "eixo do tempo": "time axis",
        "eixo temporal": "temporal axis",
        "valores inteiros": "integer values",
        "linha base": "baseline",
        "células sanguíneas": "blood cells",
        "aprendizado de máquina": "machine learning",
        "extração de características": "feature extraction",
        "processamento de imagens": "image processing",
        "detecção de bordas": "edge detection",
        "suavização prévia": "prior smoothing",
        "equalização de histograma": "histogram equalization",
        "resolução espacial": "spatial resolution",
        
        # === FILTER AND SIGNAL PROCESSING TERMS ===
        "filtros passa-baixa": "low-pass filters",
        "filtros passa-alta": "high-pass filters",
        "filtro passa-baixa": "low-pass filter",
        "filtro passa-alta": "high-pass filter",
        "filtros derivativos": "derivative filters",
        "filtros de Notch": "Notch filters",
        "filtro de Notch": "Notch filter",
        "filtro Gaussiano": "Gaussian filter",
        "média sincrona": "synchronous averaging",
        "média móvel": "moving average",
        "caracterização espectral": "spectral characterization",
        "transformada de Fourier": "Fourier transform",
        "Baseline Wander": "Baseline Wander",
        "técnica de convolução": "convolution technique",
        "função Gaussiana": "Gaussian function",
        "kernel Laplaciano": "Laplacian kernel",
        "Vizinho Mais Próximo": "Nearest Neighbor",
        "filtragem de ruído periódico": "periodic noise filtering",
        
        # === COMMON VERBS AND VERB PHRASES ===
        "Construir um sistema simplificado que possa extrair": "Build a simplified system that can extract",
        "Vamos começar instalando e importando as bibliotecas necessárias": "Let's start by installing and importing the necessary libraries",
        "Usaremos o dataset": "We will use the dataset",
        "O código abaixo irá baixar os dados e preparar as imagens e rótulos para uso":
            "The code below will download the data and prepare the images and labels for use",
        "A célula deve baixar o dataset e imprimir o mapeamento de classes":
            "The cell should download the dataset and print the class mapping",
        "Uma grade de imagens será exibida, mostrando um exemplo de cada tipo":
            "A grid of images will be displayed, showing an example of each type",
        "Observe as diferenças visuais entre elas": "Observe the visual differences between them",
        "Criamos um array": "We create an array",
        "Criamos um sinal": "We create a signal",
        "Utiliza": "Uses",
        "utiliza a técnica de convolução para calcular": "uses the convolution technique to calculate",
        "que define": "which defines",
        "será mostrado": "will be shown",
        "serão mostrados": "will be shown",
        "pode ser": "can be",
        "podem ser": "can be",
        "podem ser empregados": "can be used",
        "podem ser empregadas": "can be used",
        "podem ser atenuados": "can be attenuated",
        "poderão empregar": "can use",
        "terão que testar": "will have to test",
        "deve aparecer como": "should appear as",
        "iremos": "we will",
        "comparar a performance": "compare the performance",
        "é deslocado para a direita": "is shifted to the right",
        "é deslocado para a esquerda": "is shifted to the left",
        "é definido como": "is defined as",
        "é definida como": "is defined as",
        "são definidos": "are defined",
        "são coletadas": "are collected",
        "começa mais tarde": "starts later",
        "começa mais cedo": "starts earlier",
        "só existem em": "only exist at",
        "define os instantes": "defines the instants",
        "em que as amostras são avaliadas": "at which the samples are evaluated",
        "é usado para representar": "is used to represent",
        "é carregado com": "is loaded with",
        "é gerado para comparar": "is generated to compare",
        "Fique a vontade para propor": "Feel free to propose",
        "copie e cole": "copy and paste",
        "recomendo que você vá em": "I recommend you go to",
        
        # === COMMON PHRASES ===
        "de -10 a 10 usando": "from -10 to 10 using",
        "a cada 1/20 de segundo": "every 1/20 of a second",
        "com 1000 pontos": "with 1000 points",
        "com 5 Hz de frequência": "with 5 Hz frequency",
        "de forma contínua": "continuously",
        "de forma mais uniforme": "more uniformly",
        "garantindo que a soma dos coeficientes seja zero": "ensuring that the sum of coefficients is zero",
        "em 𝑛=0 e 0 em todos os outros pontos": "at n=0 and 0 at all other points",
        "em todos os outros pontos": "at all other points",
        "para remover": "to remove",
        "para os três": "for the three",
        "para exibir": "to display",
        "para visualizar": "to visualize",
        "para funções de": "for functions of",
        "Como sinais discretos": "As discrete signals",
        "Como": "As",
        "esse vetor": "this vector",
        "esse sinal": "this signal",
        "este sinal": "this signal",
        "este vetor": "this vector",
        "este notebook": "this notebook",
        "Por exemplo": "For example",
        "Por outro lado": "On the other hand",
        "Além disso": "Furthermore",
        "No entanto": "However",
        "Ou seja": "That is",
        "ou seja": "that is",
        "até mesmo": "even",
        "algo similar": "something similar",
        "Boa sorte": "Good luck",
        "Abra este notebook no Google Colab": "Open this notebook in Google Colab",
        "Execute as": "Execute the",
        "Uma tabela visual que mostra o desempenho do classificador em detalhe":
            "A visual table that shows the classifier's performance in detail",
        "Uma função": "A function",
        "é definida para": "is defined to",
        "Um vetor de tempo": "A time vector",
        "Um conjunto de gráficos": "A set of graphs",
        "usando, por exemplo,": "using, for example,",
        "ex: com diagonais incluídas": "e.g., with diagonals included",
        "ex: para 1/4 do tamanho original": "e.g., to 1/4 of the original size",
        
        # === COMMON WORDS (More specific combinations first) ===
        "Intervalo de": "Interval from",
        "Intervalo": "Interval",
        "Definição do": "Definition of",
        "Definição da": "Definition of",
        "Definição": "Definition",
        "Instalação": "Installation",
        "Aplicar a equalização": "Apply equalization",
        "Amplie a imagem": "Enlarge the image",
        "Reduza a resolução": "Reduce the resolution",
        "Defina manualmente": "Define manually",
        "Compare as imagens": "Compare the images",
        "Teste a função": "Test the function",
        "Função para": "Function to",
        "Função": "Function",
        "Criar figuras": "Create figures",
        "Visualização": "Visualization",
        "Transformação Logarítmica": "Logarithmic Transformation",
        "Transformadas": "Transforms",
        "Técnica automática": "Automatic technique",
        "Máscara Final": "Final Mask",
        "Objetivo": "Objective",
        "Instruções": "Instructions",
        "original é azul": "original is blue",
        "atrasado é verde": "delayed is green",
        "avançado é vermelho": "advanced is red",
        "Portanto": "Therefore",
        "Dica": "Tip",
        "Arquivo": "File",
        "Salvar uma cópia no Drive": "Save a copy to Drive",
        
        # === COMMON TECHNICAL NOUNS ===
        "atraso no tempo": "time delay",
        "avanço no tempo": "time advance",
        "ciclos respiratórios": "respiratory cycles",
        "rede elétrica": "electrical grid",
        "artefatos de": "artifacts from",
        "próximos ao diafragma": "near the diaphragm",
        "fluxo de ar": "air flow",
        "fluxo respiratório": "respiratory flow",
        "quadrado do sinal": "signal squared",
        "raiz quadrada": "square root",
        "tamanho de janela": "window size",
        "número de amostras": "number of samples",
        "conjunto de gráficos": "set of graphs",
        "mapeamento de classes": "class mapping",
        "conjuntos de treino e teste": "training and test sets",
        "níveis e visualize o efeito do falso contorno": "levels and visualize the false contour effect",
        "imagem reduzida de volta ao tamanho original": "reduced image back to original size",
        "métodos de interpolação": "interpolation methods",
        "imagens de magnitude do gradiente": "gradient magnitude images",
        "imagens médicas ruidosas": "noisy medical images",
        "mancha branca sólida": "solid white spot",
        "grande faixa dinâmica": "large dynamic range",
        "série de propriedades": "series of properties",
        "região rotulada": "labeled region",
        "Atraso": "Delay",
        "Avanço": "Advance",
        "Sistema": "System",
        "Ideal": "Ideal",
        "Amostragem": "Sampling",
        "Periódica": "Periodic",
        "gráficos": "graphs",
        "gráfico": "graph",
        "figuras": "figures",
        "figura": "figure",
        "plot": "plot",
        "plots": "plots",
        "sinais": "signals",
        "sinal": "signal",
        "ruídos": "noise",
        "ruído": "noise",
        "tempo": "time",
        "frequência": "frequency",
        "frequências": "frequencies",
        "amplitude": "amplitude",
        "fase": "phase",
        "período": "period",
        "amostra": "sample",
        "amostras": "samples",
        "filtro": "filter",
        "filtros": "filters",
        "imagem": "image",
        "imagens": "images",
        "células": "cells",
        "características": "features",
        "classificador": "classifier",
        "bibliotecas": "libraries",
        "dataset": "dataset",
        "rótulos": "labels",
        "kernel": "kernel",
        "coeficientes": "coefficients",
        "diagonais": "diagonals",
        "bordas": "edges",
        "suavização": "smoothing",
        "contorno": "contour",
        "interpolação": "interpolation",
        "textura": "texture",
        "compressão": "compression",
        "envelope": "envelope",
        "atividade": "activity",
        "threshold": "threshold",
        "janela": "window",
        "instante": "instant",
        "instantes": "instants",
        
        # === ADJECTIVES ===
        "necessárias": "necessary",
        "diferentes tipos de": "different types of",
        "discreto": "discrete",
        "discretos": "discrete",
        "contínuo": "continuous",
        "contínuos": "continuous",
        "diferentes": "different",
        "estruturados": "structured",
        "suficientes": "sufficient",
        "unitário": "unit",
        "atrasado": "delayed",
        "avançado": "advanced",
        "original": "original",
        "senoidal": "sinusoidal",
        "inteiros": "integer",
        "próximos": "near",
        "visual": "visual",
        "visuais": "visual",
        "sólida": "solid",
        "pronta para": "ready for",
        "útil para": "useful for",
        "útil em": "useful in",
        "ruidosas": "noisy",
        "prévia": "prior",
        "resultantes": "resulting",
        "global": "global",
        "automática": "automatic",
        "maior": "greater",
        "mais uniforme": "more uniform",
        "natural": "natural",
        "final": "final",
        
        # === COLORS ===
        "azul": "blue",
        "verde": "green",
        "vermelho": "red",
        "amarelo": "yellow",
        "preto": "black",
        "branco": "white",
        "branca": "white",
        
        # === COMMON SMALL WORDS AND PREPOSITIONS ===
        "deslocado para": "shifted to",
        "deslocado": "shifted",
        "usando": "using",
        "empregando": "using",
        "através de": "through",
        "resultando em": "resulting in",
        "garantindo que": "ensuring that",
        "caso houvesse": "if there were",
        "então calcula": "then calculates",
        "pronto para": "ready for",
        "capaz de distinguir": "capable of distinguishing",
        "capaz de": "capable of",
        "será": "will be",
        "são": "are",
        "é": "is",
        "um": "a",
        "uma": "a",
        "dois": "two",
        "três": "three",
        "não": "not",
        "usar": "use",
        "essas": "these",
        "esses": "these",
        "treinar": "train",
        "tipos": "types",
        "tipo": "type",
        "contém": "contains",
        "função": "function",
        "convertidos": "converted",
        "convertido": "converted",
        "após": "after",
        "código": "code",
        "célula": "cell",
        "núcleo": "nucleus",
        "área": "area",
        "número": "number",
        "números": "numbers",
        "média": "average",
        "móvel": "moving",
        "será": "will be",
        "serão": "will be",
        "aparecerá": "will appear",
        "apresentará": "will present",
        "mostrará": "will show",
        "mostrarão": "will show",
        "gerará": "will generate",
        "sofrerá": "will undergo",
        "vocês": "you",
        "vê": "see",
        "parâmetro": "parameter",
        "parâmetros": "parameters",
        "suíte": "suite",
        "técnicas": "techniques",
        "prática": "practice",
        "práticas": "practices",
        "exercício": "exercise",
        "exercícios": "exercises",
        "explicação": "explanation",
        "criação": "creation",
        "geração": "generation",
        "análise": "analysis",
        "adição": "addition",
        "redução": "reduction",
        "conversão": "conversion",
        "transformação": "transformation",
        "visualização": "visualization",
        "classificação": "classification",
        "classificações": "classifications",
        "identificação": "identification",
        "detecção": "detection",
        "segmentação": "segmentation",
        "extração": "extraction",
        "avaliação": "evaluation",
        "convolução": "convolution",
        "resolução": "resolution",
        "dimensões": "dimensions",
        "seção": "section",
        "capítulo": "chapter",
        "capítulos": "chapters",
        "título": "title",
        "critério": "criterion",
        "sequência": "sequence",
        "diferença": "difference",
        "diferenças": "differences",
        "variações": "variations",
        "considerações": "considerations",
        "implicações": "implications",
        "previsões": "predictions",
        "saída": "output",
        "versão": "version",
        "padrão": "standard",
        "específico": "specific",
        "único": "unique",
        "básicas": "basic",
        "úteis": "useful",
        "difíceis": "difficult",
        "crítico": "critical",
        "clínico": "clinical",
        "sintético": "synthetic",
        "periódica": "periodic",
        "contínuas": "continuous",
        "espaçados": "spaced",
        "extraídas": "extracted",
        "extraímos": "we extract",
        "construímos": "we build",
        "removê": "remove",
        "limpá": "clean",
        "descrevê": "describe",
        "pré": "pre",
        "aproximação": "approximation",
        "distorção": "distortion",
        "interferência": "interference",
        "restauração": "restoration",
        "rotação": "rotation",
        "translação": "translation",
        "limiarização": "thresholding",
        "decimação": "decimation",
        "cálculo": "calculation",
        "dicionário": "dictionary",
        "dicionários": "dictionaries",
        "importância": "importance",
        "importações": "imports",
        "binária": "binary",
        "matemática": "mathematical",
        "rápida": "fast",
        "máxima": "maximum",
        "ótimo": "optimal",
        "combinação": "combination",
        "representação": "representation",
        "máscara": "mask",
        "rótulo": "label",
        "confusão": "confusion",
        "começa": "starts",
        "quão": "how",
        "quê": "what",
        "diagnóstico": "diagnostic",
        "sensível": "sensitive",
        "acurácia": "accuracy",
        "numéricos": "numerical",
        "éticas": "ethical",
        "respiratório": "respiratory",
        "cardíacos": "cardiac",
        "sanguínea": "blood",
        "basófilo": "basophil",
        "basófilos": "basophils",
        "eosinófilo": "eosinophil",
        "eosinófilos": "eosinophils",
        "linfócito": "lymphocyte",
        "neutrófilo": "neutrophil",
        "espúrios": "spurious",
        "primeiro": "first",
        "segunda": "second",
        "segundo": "second",
        "terceiro": "third",
        "quarto": "fourth",
        "quinto": "fifth",
        "sexto": "sixth",
        "dados": "data",
        "tamanhos": "sizes",
        "tamanho": "size",
        "baixar": "download",
        "preparar": "prepare",
        "uso": "use",
        "mostra": "shows",
        "mostram": "show",
        "seguida": "then",
        "obter": "obtain",
        "seu": "its",
        "sua": "its",
        "seus": "their",
        "suas": "their",
        "onde": "where",
        "qual": "which",
        "instala": "installs",
        "instalá": "install",
        "biblioteca": "library",
        "bibliotecas": "libraries",
        "irá": "will",
        "importar": "import",
        "ordem": "order",
        "projeto": "project",
        "sequencia": "sequence",
        "método": "method",
        "métodos": "methods",
        "operação": "operation",
        "operações": "operations",
        "divisão": "division",
        "multiplicação": "multiplication",
        "aritmética": "arithmetic",
        "lógica": "logic",
        "lógicas": "logical",
        "execução": "execution",
        "implementação": "implementation",
        "implementações": "implementations",
        "informações": "information",
        "orientação": "orientation",
        "região": "region",
        "regiões": "regions",
        "níveis": "levels",
        "nível": "level",
        "mínimo": "minimum",
        "máximo": "maximum",
        "médica": "medical",
        "médicas": "medical",
        "médicos": "medical",
        "aparência": "appearance",
        "iluminação": "illumination",
        "mudanças": "changes",
        "fórmula": "formula",
        "fórmulas": "formulas",
        "dimensão": "dimension",
        "distorções": "distortions",
        "geométricas": "geometric",
        "específicas": "specific",
        "idênticos": "identical",
        "bicúbica": "bicubic",
        "numéricas": "numerical",
        "quantização": "quantization",
        "realçar": "enhance",
        "precisará": "will need",
        "facilita": "facilitates",
        "importa": "imports",
        "usaremos": "we will use",
        "useemos": "we use",
        "usamos": "we use",
        "todas": "all",
        "cada": "each",
        "exemplo": "example",
        "exemplos": "examples",
        "apenas": "only",
        "sempre": "always",
        "depois": "after",
        "antes": "before",
        "ainda": "still",
        "bem": "well",
        "muito": "very",
        "pouco": "little",
        "alguns": "some",
        "algumas": "some",
        "várias": "several",
        "próxima": "next",
        "última": "last",
        "último": "last",
        "está": "is",
        "estão": "are",
        "há": "there is",
        "clássica": "classical",
        "mecânica": "mechanical",
        "cérebro": "brain",
        "botão": "button",
        "domínio": "domain",
        "potência": "power",
        "referência": "reference",
        "situação": "situation",
        "situações": "situations",
        "convenção": "convention",
        "distribuição": "distribution",
        "formação": "formation",
        "correlação": "correlation",
        "especificação": "specification",
        "específica": "specific",
        "modificações": "modifications",
        "mudança": "change",
        "transformações": "transformations",
        "introdução": "introduction",
        "percepção": "perception",
        "correção": "correction",
        "contribuição": "contribution",
        "remoção": "removal",
        "tentará": "will try",
        "realça": "enhances",
        "realçam": "enhance",
        "rápido": "fast",
        "subtraída": "subtracted",
        "responsável": "responsible",
        "necessários": "necessary",
        "teóricos": "theoretical",
        "diagnóstica": "diagnostic",
        "preferível": "preferable",
        "aceitável": "acceptable",
        "eficácia": "efficacy",
        "distâncias": "distances",
        "funções": "functions",
        "técnica": "technique",
        "aguçamento": "sharpening",
        "magnética": "magnetic",
        "ressonância": "resonance",
        "informação": "information",
        "configureção": "configuration",
        
        # Common Portuguese grammar patterns to fix
        "types different": "different types",
        "times different": "different times",
        "methods different": "different methods",
        "sizes different": "different sizes",
        "values different": "different values",
        "a library that facilita o download": "a library that facilitates downloading",
        "Importa all as libraries that": "Import all the libraries that",
        "libraries that useemos": "libraries that we use",
        "signal discrete": "discrete signal",
        "signal original": "original signal",
        "signal delayed": "delayed signal",
        "signal advanced": "advanced signal",
        "Are defined two": "Two are defined",
        "arquivo esteja": "file is",
        "mesmo diretório": "same directory",
        "certifique-se": "make sure",
        "diretório": "directory",
        "nesta": "in this",
        "desta": "of this",
        "deste": "of this",
        "agora": "now",
        "aqui": "here",
        "ali": "there",
        "discutir": "discuss",
        "discutiremos": "we will discuss",
        "conhecimento": "knowledge",
        "arquivos": "files",
        "arquivo": "file",
        "coloridas": "color",
        "demonstração": "demonstration",
        "morfológico": "morphological",
        "morfológica": "morphological",
        "aula": "class",
        "acurácia": "accuracy",
        "agradável": "pleasant",
        "aplicação": "application",
        "aplicações": "applications",
        "atenuação": "attenuation",
        "ativação": "activation",
        "ativações": "activations",
        "através": "through",
        "atribuição": "attribution",
        "atribuída": "attributed",
        "atribuídas": "attributed",
        "até": "until",
        "aumentá": "increase",
        "avançada": "advanced",
        "avanço": "advance",
        "ação": "action",
        "ações": "actions",
        "balanço": "balance",
        "binárias": "binary",
        "binário": "binary",
        "binários": "binary",
        "biológicos": "biological",
        "biológico": "biological",
        "básico": "basic",
        "básicos": "basic",
        "bíceps": "biceps",
        "característica": "feature",
        "características": "features",
        "característico": "characteristic",
        "centralização": "centralization",
        "codificação": "encoding",
        "comentários": "comments",
        "comparação": "comparison",
        "compressão": "compression",
        "concluído": "completed",
        "condições": "conditions",
        "condição": "condition",
        "conexão": "connection",
        "disponível": "available",
        "disponíveis": "available",
        "descrição": "description",
        "extensão": "extension",
        "implementar": "implement",
        "incluída": "included",
        "incluído": "included",
        "incluídas": "included",
        "incluídos": "included",
        "normalizaç": "normaliz",  # Partial word match
        "otimização": "optimization",
        "parágrafo": "paragraph",
        "próximo": "next",
        "próximos": "next",
        "redução": "reduction",
        "versão": "version",
        "versões": "versions",
        "processamento": "processing",
        "discutidos": "discussed",
        "discutido": "discussed",
        "os": "the",
        "as": "the",
        "uma": "a",
        "uns": "some",
        "umas": "some",
        "com": "with",
        "sem": "without",
        "sem que": "without",
        "para": "to",
        "para a": "to the",
        "de": "of",
        "em": "at",
        "e": "and",
        "ou": "or",
        "que": "that",
        "mais": "more",
        "menos": "less",
        "sobre": "about",
        "entre": "between",
        "abaixo": "below",
        "acima": "above",
        "direita": "right",
        "esquerda": "left",
        "cada": "each",
        "todas": "all",
        "todos": "all",
        "algumas": "some",
        "alguns": "some",
        "pelo": "by the",
        "pela": "by the",
        "pelos": "by the",
        "pelas": "by the",
        "nos": "in the",
        "nas": "in the",
        "aos": "to the",
        "às": "to the",
        "dos": "of the",
        "das": "of the",
        "do": "of the",
        "da": "of the",
        "no": "in the",
        "na": "in the",
        "ao": "to the",
        "à": "to the",
    }

def translate_markdown(text):
    """Translate markdown text while preserving formatting."""
    if not text or not isinstance(text, str):
        return text
    
    result = text
    translations = get_comprehensive_translations()
    
    # Sort by length (longest first) to handle phrases before individual words
    sorted_translations = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    # Special handling for Portuguese articles and common patterns
    # Handle "O que" -> "What" (not "The that")
    result = re.sub(r'\bO\s+que\b', 'What', result)
    result = re.sub(r'\bo\s+que\b', 'what', result)
    
    # Handle other "O" patterns (Portuguese "the")
    result = re.sub(r'\bO\s+(signal|sinal)', r'The \1', result)
    result = re.sub(r'\bo\s+(signal|sinal)', r'the \1', result)
    
    for pt, en in sorted_translations:
        # Use word boundary matching for short words (<=3 chars) to avoid partial replacements
        if len(pt) <= 3 and pt.lower() not in ['ecg', 'emg', 'rms', 'dft', 'fft', 'pré', 'roc']:
            # For very short words, use word boundaries
            pattern = r'\b' + re.escape(pt) + r'\b'
            result = re.sub(pattern, en, result, flags=re.IGNORECASE)
            # Handle capitalized version
            pt_cap = pt[0].upper() + pt[1:] if len(pt) > 0 else pt
            en_cap = en[0].upper() + en[1:] if len(en) > 0 else en
            if pt_cap != pt:
                pattern_cap = r'\b' + re.escape(pt_cap) + r'\b'
                result = re.sub(pattern_cap, en_cap, result)
        else:
            # For longer phrases, use simple replacement
            if pt in result:
                result = result.replace(pt, en)
            # Also try with first letter capitalized
            pt_cap = pt[0].upper() + pt[1:] if len(pt) > 0 else pt
            en_cap = en[0].upper() + en[1:] if len(en) > 0 else en
            if pt_cap in result and pt_cap != pt:
                result = result.replace(pt_cap, en_cap)
    
    return result

def translate_code_comment(comment):
    """Translate a Python comment."""
    if comment.strip().startswith('#'):
        # Extract the # and any spaces
        match = re.match(r'^(\s*#\s*)', comment)
        if match:
            prefix = match.group(1)
            text = comment[len(prefix):]
            
            # Additional translations for code comments
            text = text.replace('Definir o', 'Define the')
            text = text.replace('Carrega the', 'Load the')
            text = text.replace('Carrega o', 'Load the')
            text = text.replace('certifique-se of that o', 'make sure the')
            text = text.replace('arquivo esteja in the mesmo', 'file is in the same')
            text = text.replace('Installsr a library', 'Install the library')
            text = text.replace('esteja in', 'is in')
            text = text.replace('mesmo diretório', 'same directory')
            
            translated = translate_markdown(text)
            return prefix + translated
    return translate_markdown(comment)

def translate_code_cell(source_lines):
    """Translate comments in code while preserving code logic."""
    if not source_lines:
        return source_lines
    
    result = []
    for line in source_lines:
        # Check if line contains a comment
        if '#' in line:
            # Split on first # that's not in a string
            in_string = False
            quote_char = None
            comment_pos = -1
            
            for i, char in enumerate(line):
                if char in ['"', "'"] and (i == 0 or line[i-1] != '\\'):
                    if not in_string:
                        in_string = True
                        quote_char = char
                    elif char == quote_char:
                        in_string = False
                        quote_char = None
                elif char == '#' and not in_string:
                    comment_pos = i
                    break
            
            if comment_pos >= 0:
                code_part = line[:comment_pos]
                comment_part = line[comment_pos:]
                translated_comment = translate_code_comment(comment_part)
                result.append(code_part + translated_comment)
            else:
                result.append(line)
        else:
            result.append(line)
    
    return result

def process_notebook(input_path, output_path):
    """Process a single Jupyter notebook file."""
    print(f"  Processing: {input_path.name}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Process each cell
    for cell in notebook.get('cells', []):
        if 'source' not in cell:
            continue
        
        cell_type = cell.get('cell_type', '')
        source = cell['source']
        
        # Ensure source is a list
        if isinstance(source, str):
            source = [source]
        
        if cell_type == 'markdown':
            # Translate all markdown content
            cell['source'] = [translate_markdown(line) for line in source]
        elif cell_type == 'code':
            # Translate only comments in code cells
            cell['source'] = translate_code_cell(source)
    
    # Write the translated notebook
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)
    
    print(f"    → Created: {output_path.name}")

def main():
    """Main function to process all notebooks."""
    base_dir = Path('/home/runner/work/BioSignalAndImgProcessing/BioSignalAndImgProcessing')
    assignments_dir = base_dir / 'assignments'
    
    # List of all notebooks to translate
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
    
    print(f"\n{'='*60}")
    print(f"Comprehensive Portuguese to English Translation")
    print(f"{'='*60}")
    print(f"Processing {len(notebooks)} notebooks...\n")
    
    success_count = 0
    error_count = 0
    
    for notebook_name in notebooks:
        try:
            input_path = assignments_dir / notebook_name
            output_name = notebook_name.replace('.ipynb', '_en.ipynb')
            output_path = assignments_dir / output_name
            
            if not input_path.exists():
                print(f"  ✗ Not found: {notebook_name}")
                error_count += 1
                continue
            
            process_notebook(input_path, output_path)
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ Error processing {notebook_name}: {str(e)}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"Translation Complete!")
    print(f"  ✓ Success: {success_count}")
    if error_count > 0:
        print(f"  ✗ Errors: {error_count}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
