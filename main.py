import pdfplumber
from pathlib import Path
import csv
import re
import tkinter as tk
from tkinter import filedialog 

def extrair_nome(linha):
    """Extrai nome do paciente da primeira linha""" 
    if 'PACIENTE:' in linha:
        return linha.split('PACIENTE:')[1].strip()
    return linha.strip()

def extrair_codigo(linha):
    """Extrai código da segunda linha"""
    numeros = re.findall(r'\d+', linha)
    if numeros:
        return numeros[0]
    return linha.replace('CÓDIGO:', '').replace('CODIGO:', '').strip()

def extrair_data(linha):
    """Extrai data da terceira linha"""
    padrao_data = r'(\d{2}/\d{2}/\d{4})'
    match = re.search(padrao_data, linha)
    return match.group(1) if match else ""

def extrair_titulo_com_por(linhas, indice_inicial=3):
    """
    Extrai título com lógica especial para 'POR':
    1. Pula linhas com ':'
    2. Se linha sem ':' termina com 'POR', inclui próxima linha
    """
    limite_busca = min(15, len(linhas))
    
    for i in range(indice_inicial, limite_busca):
        linha_atual = linhas[i]
        
        if ':' not in linha_atual:
            titulo = linha_atual
            linha_titulo = i + 1
            
            # verifica se termina com POR
            linha_limpa = linha_atual.strip().upper()
            while linha_limpa and not linha_limpa[-1].isalnum():
                linha_limpa = linha_limpa[:-1]
            
            if linha_limpa.endswith('POR') and i + 1 < len(linhas):
                proxima_linha = linhas[i + 1].strip()
                if ':' not in proxima_linha:
                    titulo = f"{linha_atual} {proxima_linha}"
            
            return titulo, linha_titulo
    
    if len(linhas) > indice_inicial:
        return linhas[indice_inicial], indice_inicial + 1
    
    return "NÃO ENCONTRADO", 0

def processar_pdfs_completo(diretorio):
    """Processa PDFs extraindo todas as informações"""
    resultados = []
    diretorio_path = Path(diretorio)
    arquivos_pdf = list(diretorio_path.rglob("*.pdf"))
    
    if not arquivos_pdf:
        print("Nenhum arquivo PDF encontrado.")
        return resultados
    
    print(f"Processando {len(arquivos_pdf)} arquivos (com lógica POR)...\n")
    
    for idx, arquivo in enumerate(arquivos_pdf, 1):
        print(f"[{idx}/{len(arquivos_pdf)}] {arquivo.name}")
        
        try:
            with pdfplumber.open(arquivo) as pdf:
                texto = pdf.pages[0].extract_text()
                linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
                
                if len(linhas) >= 4:
                    nome = extrair_nome(linhas[0]) if len(linhas) > 0 else ""
                    codigo = extrair_codigo(linhas[1]) if len(linhas) > 1 else ""
                    data = extrair_data(linhas[2]) if len(linhas) > 2 else ""
                    titulo, linha_titulo = extrair_titulo_com_por(linhas)
                    
                    # verifica se título incluiu linha extra
                    incluiu_extra = 'POR' in titulo.upper() and len(titulo.split()) > 3
                    
                    resultados.append({
                        'caminho_arquivo': str(arquivo.absolute()),
                        'paciente': nome,
                        'codigo': codigo,
                        'data': data,
                        'titulo_exame': titulo,
                    })
                    
                    print(f"  ✓ {nome[:20]}... | Cód: {codigo} | Data: {data}")
                    if incluiu_extra:
                        print(f"    Título (com POR): {titulo[:60]}...")
                    elif linha_titulo > 4:
                        print(f"    Título na linha {linha_titulo}")
                        
                else:
                    resultados.append({
                        'caminho_arquivo': str(arquivo.absolute()),
                        'paciente': '',
                        'codigo': '',
                        'data': '',
                        'titulo_exame': f'ERRO: Apenas {len(linhas)} linhas',
                    })
                    
        except Exception as e:
            resultados.append({
                'caminho_arquivo': str(arquivo.absolute()),
                'paciente': '',
                'codigo': '',
                'data': '',
                'titulo_exame': f'ERRO: {str(e)[:50]}',
            })
    
    return resultados

def exportar_completo(resultados, arquivo_saida='info_laudos.csv'):
    """Exporta resultados completos para CSV"""
    with open(arquivo_saida, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)
    
    print(f"\nExportado para: {arquivo_saida}")

# Executar com Interface Gráfica
if __name__ == "__main__":
    # Configuração da janela oculta (root)
    root = tk.Tk()
    root.withdraw() # Esconde a janela principal do Tkinter, queremos só o popup
    
    print("Por favor, selecione a pasta contendo os PDFs na janela que se abriu...")
    
    # Abre o seletor de pastas
    pasta_selecionada = filedialog.askdirectory(title="Selecione a pasta raiz dos Laudos")
    
    if pasta_selecionada:
        print(f"\nPasta selecionada: {pasta_selecionada}")
        resultados = processar_pdfs_completo(pasta_selecionada)
        if resultados:
            exportar_completo(resultados)
    else:
        print("\nNenhuma pasta selecionada... Operação cancelada.")