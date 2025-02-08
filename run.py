import sys

from src.crawler import BuscadorTceSp

busca = sys.argv[1]
BuscadorTceSp(busca).baixa_docs()