import requests
from bs4 import BeautifulSoup

import re

class BuscadorTceSp:

    URL_BASE = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar"

    def __init__(self, busca):
        self.nome_busca = busca
        print(f'Buscando por {self.nome_busca}...')
        # import pdb; pdb.set_trace()

    def baixa_docs(self):
        url_busca = f'{self.URL_BASE}?txtTdPalvs={self.nome_busca.replace(' ', '+')}&txtExp=&txtQqUma=&txtNenhPalvs=&txtNumIni=&txtNumFim=&tipoBuscaTxt=Documento&_tipoBuscaTxt=on&quantTrechos=1&processo=&exercicio=&dataAutuacaoInicio=&dataAutuacaoFim=&dataPubInicio=&dataPubFim=&_relator=1&_auditor=1&_materia=1&_tipoDocumento=1&acao=Executa'
        pagina_jurisprudencia = self._obtem_pag_jurisprudencia(url_busca)
        # import pdb; pdb.set_trace();
        self._exatrai_dados_tabela(pagina_jurisprudencia)


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
                # import pdb; pdb.set_trace();
                doc = {
                    "Doc" : cols[0].get_text(strip=True),
                    # "N_processo" : cols[1].get_text(strip=True).split()[0], (Estava pegando informações a mais)
                    "N_processo": re.match(r'^\d{4,}/\d{3}/\d+', cols[1].get_text(strip=True)).group(0)
                    if re.match(r'^\d{4,}/\d{3}/\d+', cols[1].get_text(strip=True))
                    else cols[1].get_text(strip=True),
                    "Data_Atuação" : cols[2].get_text(strip=True),
                    "Partes" : [parte.strip() for parte in cols[3].get_text(strip=True).split(';')],
                    "Materia" : cols[4].get_text(strip=True),
                    "URL" : cols[0].find('a')['href'] if cols[0].find('a') else ""
                }
                documentos.append(doc)
        return documentos
    

