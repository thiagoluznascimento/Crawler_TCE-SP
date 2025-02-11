# RPA(Robotic Process Automation) / TCE-SP
Objetivo desse projeto é desenvolver um robô para automação de processos utilizando Python. O robô será responsável por extrair todos os documentos do site do TCE-SP, que sejam relacionados a “fraude em escolas” salvar esses dados em um formato adequado (por exemplo, CSV, JSON). 
O site para raspagem de dados é https://www.tce.sp.gov.br/jurisprudencia/

## Preparação do ambiente de desenvolvimento  
Para executar o projeto, é necessário ter o **Python 3.12.3** instalado e seguir os passos abaixo:  

1. Clonar o repositório:  
   ```bash
   git clone https://github.com/thiagoluznascimento/Crawler_TCE-SP.git
   ```  

2. Criar um ambiente virtual:  
   ```bash
   python3 -m venv venv
   ```  

3. Ativar o ambiente virtual:  
   ```bash
   source venv/bin/activate
   ```  
4. Instalar as dependências:  
   ```bash
   pip install -r requirements.txt
   ```  
---

## Configuração do MongoDB Atlas  
Para armazenar os dados no **MongoDB Atlas**, siga os passos abaixo:  

1. Criar uma conta no [MongoDB Atlas](https://www.mongodb.com/atlas/database).  
2. Criar um novo **cluster** e adicionar um usuário com permissões de leitura e escrita.  
3. Obter a **string de conexão** no formato:  
   ```
   mongodb+srv://<usuário>:<senha>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority
   ```  
4. Criar um arquivo `.env` na raiz do projeto e configurar a variável `MONGO_URL` com sua string de conexão. Você pode usar o arquivo `.env.example` como referência:  
   ```bash
   cp .env.example .env
   ```  
5. Certifique-se de que seu cluster permite conexões da sua **IP whitelist**.  

---

## Como executar o programa  
Para executar o projeto, utilize o seguinte comando:  

```bash
python3 run.py "fraude em escolas"
```

Os dados extraídos serão automaticamente armazenados no **MongoDB Atlas**.

---

## Considerações  
Caso queira salvar localmente as informações raspadas, utilize a **branch `hotfix`**, que permite baixar os dados em um arquivo JSON diretamente para sua máquina.  

1. Mudar para a branch `hotfix`:  
   ```bash
   git checkout hotfix
   ```  

2. Executar o projeto na branch `hotfix`:  
   ```bash
   python3 run.py "fraude em escolas"
   ```

---

# Descrição do desafio RPA(Robotic Process Automation) - TURIVIUS

Desafio a ser apresentado para a empresa Turivius

## Objetivo
Objetivo do desafio é desenvolver um robô de automação de processos utilizando Python e as bibliotecas
requests_html, Selenium e Scrapy. O candidato deverá demonstrar habilidades em navegação web, extração de
dados e manipulação de informações, utilizando essas ferramentas.

## Descrição do desafio
O robô será responsável por extrair todos os documentos do site do TCE-SP, que sejam relacionados a “fraude em escolas” salvar esses dados em um formato adequado (por exemplo, CSV, JSON). 
O site para raspagem de dados é https://www.tce.sp.gov.br/jurisprudencia/

class BuscadorTceSp:

    URL_BUSCA = "https://www.tce.sp.gov.br/jurisprudencia/"

    def baixa_docs(self):
        self._obtem_pag_jurisprudencia(self.URL_BUSCA)

    def _obtem_pag_jurisprudencia( self, URL_BUSCA):
        try:
            r = requests.get(self.URL_BUSCA, auth=('user', 'pass'))
            resposta = r.status_code
            import pdb; pdb.set_trace();
            print(resposta.text)
        except Exception as e:    
            print(f'Erro ao requisitar Jurisprudencia - Erro: {str(e)}')



A imagem abaixo exibe uma sugestão de pesquisa

![pesquisa de jurisprudência](image.png)

## Formato do arquivo de saída:

| Doc  | N processo|  Data Autuação |               Partes                  |     Matéria  |    URL     |
|------|-----------|----------------|---------------------------------------|--------------|------------|
| Desp | XXXXXXXXX | DD-MM-YYYY     |  [‘Parte a’, ‘parte b’, ‘parte c’]    |     EBDAp    | http:link  |
|      |    ...    |     ...        |              ...                      |     ...      |   ...      |
| Desp | XXXXXXXXX | DD-MM-YYYY     |  [‘Parte a’, ‘parte b’, ‘parte c’]    |     EBDAp    | http:link  |


## Requisitos:
1. Utilizar biblioteca raspagem de dados para fazer o scraping do site e extrair os dados necessários.
2. Priorizar performance na raspagem dos dados.
3. Extrair e salvar os dados em um banco de dados (Postgresql, MySQL e etc)
4. A modelagem da tabela no banco de dados deve ser otimizada para recuperação de informação baseada em data, matéria e Doc, ou seja através de index e outras estruturas de recuperação de informação.
5. O código deve ser pensado de modo a ser colocado em ambiente de produção, isto é com variaveis de ambiente localizadas em arquivos de separados (por exemplo, .env)
6. Documentar o código de forma clara e concisa, explicando a lógica por trás das ações realizadas.

## Critérios de Avaliação:
1. Funcionalidade: O robô deve ser capaz de extrair corretamente os dados do site fornecido
2. Qualidade do código: O código deve ser limpo, bem estruturado e seguir as melhores práticas de
desenvolvimento em Python, utilizando PEP8
3. Utilização eficaz das ferramentas: O candidato deve demonstrar habilidade no uso de pelo menos umas das seguintes bibliotecas: 
* requests_html 
* Selenium
* Scrapy
* BeautifulSoap(bs4)
4. Documentação: O código deve estar devidamente documentado, explicando a lógica por trás das ações
realizadas e qualquer configuração necessária.
5. Robustez: O robô deve ser capaz de lidar com situações de exceção de forma adequada, como falhas de
conexão ou mudanças na estrutura do site.

## Diferencial:
1. Uso preferencial: Implementar a solução utilizando request_html ou bs4;
2. Entrega da solução containerizada: Desenhar a solução para rodar em containers Docker/K8s;
3. Testes de Software: Desenvolver testes funcionais e de unidade para garantir funcionalidades esperadas;
4. SGBD orientados a Documento: Fazer o armazenamento das informações extraídas em algum dos seguintes banco
de dados como Mongo, Dynamodb ou engines como Opensearch/Elastisearch.
