import requests
from bs4 import BeautifulSoup

class BuscadorTceSp:

    URL_BASE = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar"

    def __init__(self, busca):
        self.nome_busca = busca
        print(f'Buscando por {self.nome_busca}')
        # import pdb; pdb.set_trace()

    def baixa_docs(self):
        url_busca = f'{self.URL_BASE}?txtTdPalvs={self.nome_busca.replace(' ', '+')}&txtExp=&txtQqUma=&txtNenhPalvs=&txtNumIni=&txtNumFim=&tipoBuscaTxt=Documento&_tipoBuscaTxt=on&quantTrechos=1&processo=&exercicio=&dataAutuacaoInicio=&dataAutuacaoFim=&dataPubInicio=&dataPubFim=&_relator=1&_auditor=1&_materia=1&_tipoDocumento=1&acao=Executa'
        self._obtem_pag_jurisprudencia(url_busca)


    

    def _obtem_pag_jurisprudencia( self, url_busca):
        try:
            r = requests.get(url_busca)
            resposta = r.status_code
            print(r.text)
            # import pdb; pdb.set_trace();
        except Exception as e:
            print(f'Erro ao requisitar Jurisprudencia - Erro: {str(e)}')

