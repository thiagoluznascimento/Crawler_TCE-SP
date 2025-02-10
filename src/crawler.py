import requests
from bs4 import BeautifulSoup

import re
import json

class BuscadorTceSp:

    URL_BASE = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar"

    def __init__(self, busca):
        self.nome_busca = busca
        print(f'Buscando por {self.nome_busca}...')

    def baixa_docs(self):
        url_busca = f'{self.URL_BASE}?txtTdPalvs={self.nome_busca.replace(' ', '+')}&txtExp=&txtQqUma=&txtNenhPalvs=&txtNumIni=&txtNumFim=&tipoBuscaTxt=Documento&_tipoBuscaTxt=on&quantTrechos=1&processo=&exercicio=&dataAutuacaoInicio=&dataAutuacaoFim=&dataPubInicio=&dataPubFim=&_relator=1&_auditor=1&_materia=1&_tipoDocumento=1&acao=Executa'
        pagina_jurisprudencia = self._obtem_pag_jurisprudencia(url_busca)
        documentos = self._exatrai_dados_tabela(pagina_jurisprudencia)
        self._obtem_total_pag(pagina_jurisprudencia)
        self._salva_em_json(documentos, 'dados_jurisprudencia.json')


    def _obtem_pag_jurisprudencia( self, url_busca):
        """Faz requisição ao TCE-SP e retorna resultado HTML"""
        try:
            response = requests.get(url_busca)
            response.raise_for_status()
        except Exception as e:
            print(f'Erro ao requisitar Jurisprudencia - Erro: {str(e)}')
        return response.text
    
    def _exatrai_dados_tabela(self, pagina_jurisprudencia):
        """Extrai dados da tabela contendo as informações"""
        soup = BeautifulSoup(pagina_jurisprudencia, 'html.parser')
        rows = soup.select("table.table-docs tbody tr")
        documentos = []
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 8:
                doc = {
                    "Doc" : cols[0].get_text(strip=True),
                    # "N_processo" : cols[1].get_text(strip=True).split()[0], (Estava pegando informações a mais)
                    # "N_processo": re.match(r'^\d{4,}/\d{3}/\d{2}', cols[1].get_text(strip=True)).group(0)
                    # if re.match(r'^\d{4,}/\d{3}/\d+', cols[1].get_text(strip=True))
                    # else cols[1].get_text(strip=True),
                    "N° processo" : self._extrair_numero_processo(cols[1].get_text(strip=True)),
                    "Data_Atuação" : cols[2].get_text(strip=True),
                    "Partes" : [cols[3].get_text(strip=True) + "; " + cols[4].get_text(strip=True)],
                    "Materia" : cols[5].get_text(strip=True),
                    "URL" : cols[0].find('a')['href'] if cols[0].find('a') else ""
                }
                documentos.append(doc)
        return documentos
    
    def _extrair_numero_processo(self, texto):
        """Extrai número do processo do campo correspondente"""
        match = re.match(r'^\d{1,}/\d{3,}/\d{2}', texto)
        return match.group(0) if match else texto
    
    def _obtem_total_pag(self, pagina_jurisprudencia):
        """Retorna o total de páginas da paginação"""
        soup = BeautifulSoup(pagina_jurisprudencia, 'html.parser')
        paginas = soup.find_all('a', class_='page-link')
        total_paginas = max([int(pagina.get_text()) for pagina in paginas if pagina.get_text(strip=True).isdigit()], default=1)
        return total_paginas

    def _salva_em_json(self, dados, nome_arquivo):
        """Salva os dados extraídos em um arquivo JSON"""
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        print(f"Dados salvos em {nome_arquivo}")
