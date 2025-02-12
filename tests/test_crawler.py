from unittest.mock import patch, Mock
from unittest import TestCase

from src.crawler import BuscadorTceSp

class TestBuscadorTceSp(TestCase):
    
    def setUp(self):
        self.nome_busca = "fraude em escolas"
        self.instancia_crawler = BuscadorTceSp(self.nome_busca)
        self.URL_BASE = "https://www.tce.sp.gov.br/jurisprudencia/pesquisar"
        self.url_busca = f"{self.URL_BASE}?txtTdPalvs={self.nome_busca.replace(' ', '+')}&acao=Executa"

        with open('./tests/fixtures/paginas/resultado_busca.html') as f:
            self.pagina_resultado_busca = f.read()
        

    def test__obtem_pag_jurisprudencia(self):
        with patch('requests.get', return_value=Mock(text=self.pagina_resultado_busca)) as mock_get:
            html_obtido = self.instancia_crawler._obtem_pag_jurisprudencia(self.url_busca)
            self.assertEqual(self.pagina_resultado_busca, html_obtido, "Pagina diferente da esperada.")
            self.assertEqual(mock_get.call_count, 1, "O numero de chamada é diferente do esperado.")
