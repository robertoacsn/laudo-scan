# 🏥 LaudoScan: Extrator de Metadados de Laudos Médicos

> **Ferramenta de auditoria e automação para validação de dados clínicos.**

## 📄 Sobre o Projeto

Este projeto foi desenvolvido para resolver um gargalo crítico durante um processo de **migração de sistemas (ERP)** na área da saúde. A necessidade era validar a integridade de milhares de arquivos legados e garantir que os dados contidos nos PDFs (conteúdo) correspondiam aos metadados do sistema.

O **LaudoScan** atua como um "auditor digital", varrendo diretórios recursivamente, aplicando leitura de texto e estruturando dados não estruturados em uma planilha para conferência massiva.

## 📋 Funcionalidades Principais

- **Varredura Recursiva:** Localiza arquivos `.pdf` em todas as subpastas do diretório alvo, independente da profundidade.
- **Extração Inteligente (Regex):**
  - Identifica **Nome do Paciente** e **Código do Atendimento** baseando-se em padrões textuais específicos.
  - Padroniza datas automaticamente para o formato `dd/mm/aaaa`.
- **Lógica de Títulos Complexos:** Algoritmo customizado capaz de identificar títulos de exames que sofrem quebra de linha, tratando conectores específicos (ex: _"USG ABDOME TOTAL \n POR MÉDICO X"_ é lido corretamente como um único título).
- **Tratamento de Erros (Fault Tolerance):** O script possui robustez para não parar caso encontre um arquivo corrompido; ele registra o erro no relatório final e continua o processamento dos demais.
- **Exportação Compatível:** Gera um relatório em CSV com encoding `utf-8-sig`, pronto para ser aberto no **Excel** ou **Google Sheets** sem erros de acentuação.

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **pdfplumber:** Para extração precisa de layout e texto dos PDFs.
- **RegEx (re):** Para mineração e identificação
