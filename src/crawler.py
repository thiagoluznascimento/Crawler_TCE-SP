import re
import os

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]

print(f"Conectado ao banco de dados: {MONGO_DB_NAME}")

collection = db.jurisprudencias


class BuscadorTceSp:
    URL_BASE = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar"

    def __init__(self, busca):
        self.nome_busca = busca
        print(f"Buscando por {self.nome_busca}...")

    def baixa_docs(self):
        documentos = []
        offset = 0
        url_base_busca = f"{self.URL_BASE}?txtTdPalvs={self.nome_busca.replace(' ', '+')}&acao=Executa"

        # Obtem a página inicial para calcular o total de páginas
        pagina_jurisprudencia = self._obtem_pag_jurisprudencia(url_base_busca)
        total_paginas = self._obtem_total_pag(pagina_jurisprudencia)
        print(f"Total de páginas encontradas: {total_paginas}")

        # Percorre todas as páginas disponíveis
        for pagina in range(total_paginas):
            print(f"Buscando página {pagina + 1} de {total_paginas}...")
            url_paginada = f"{url_base_busca}&offset={offset}"
            pagina_jurisprudencia = self._obtem_pag_jurisprudencia(url_paginada)
            documentos.extend(self._extrai_dados_tabela(pagina_jurisprudencia))
            offset += 10  # Avança para a próxima página

        self._salva_no_mongo(documentos)

    def _obtem_pag_jurisprudencia(self, url_busca):
        """Faz requisição ao TCE-SP e retorna resultado HTML"""
        try:
            response = requests.get(url_busca)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Erro ao requisitar Jurisprudência: {str(e)}")
            return ""

    def _extrai_dados_tabela(self, pagina_jurisprudencia):
        """Extrai dados da tabela contendo as informações"""
        soup = BeautifulSoup(pagina_jurisprudencia, "html.parser")
        rows = soup.select("table.table-docs tbody tr")
        documentos = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 8:
                doc = {
                    "Doc": cols[0].get_text(strip=True),
                    "N_processo": self._extrair_numero_processo(
                        cols[1].get_text(strip=True)
                    ),
                    "Data_Autuação": cols[2].get_text(strip=True),
                    "Partes": [
                        cols[3].get_text(strip=True),
                        cols[4].get_text(strip=True),
                    ],
                    "Matéria": cols[5].get_text(strip=True),
                    "URL": cols[0].find("a")["href"] if cols[0].find("a") else "",
                }
                documentos.append(doc)
        return documentos

    def _extrair_numero_processo(self, texto):
        """Extrai o número do processo do campo correspondente"""
        match = re.match(r"^\d{1,}/\d{3,}/\d{2}", texto)
        return match.group(0) if match else texto

    def _obtem_total_pag(self, pagina_jurisprudencia):
        """Retorna o total de páginas da paginação"""
        soup = BeautifulSoup(pagina_jurisprudencia, "html.parser")
        paginas = soup.find_all("a", class_="page-link")

        # Encontra o maior número de offset disponível
        offsets = [
            int(link["href"].split("offset=")[-1])
            for link in paginas
            if "offset=" in link["href"]
        ]
        max_offset = max(offsets, default=0)

        # offset aumentando de 10 em 10, calcula o total de páginas
        total_paginas = (max_offset // 10) + 1
        return total_paginas

    def _salva_no_mongo(self, dados):
        """Salva os dados extraídos no MongoAtlas"""
        if dados:
            collection.insert_many(dados)
            print(f"{len(dados)} documentos inseridos no MongoDB com sucesso!")
        else:
            print("Nenhum documento encontrado para salvar.")
