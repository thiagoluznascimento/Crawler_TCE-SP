import requests
from bs4 import BeautifulSoup

class BuscadorTceSp:

    URL_BUSCA = "https://www.tce.sp.gov.br/jurisprudencia/"

    def baixa_docs(self):
        self._obtem_pag_jurisprudencia(self.URL_BUSCA)

    def _obtem_pag_jurisprudencia( self, URL_BUSCA):
        try:
            r = requests.get(self.URL_BUSCA, auth=('user', 'pass'))
            resposta = r.status_code
            print(resposta)
            import pdb; pdb.set_trace();
        except Exception as e:
            print(f'Erro ao requisitar Jurisprudencia - Erro: {str(e)}')

