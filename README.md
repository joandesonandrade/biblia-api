# biblia-api
API para consultar a bíblia

**rápido**, **fácil** e **eficiente**.

Python + Fastapi + MongoDB

### Baixar dados
Baixe o banco de dados
Obrigado [@thiagobodruk](https://github.com/thiagobodruk) por fornecer a bíblia estruturada em JSON 

https://github.com/thiagobodruk/biblia

Salve o arquivo JSON dentro da pasta `database`

### Enviar dados para o mongodb
execute o comando

`python uploadDatabaseToMongoDB.py`

Certifique-se de renomear o arquivo `.env.example` para `.env`
e preenche-lo com os seus dados de configuração, mova o arquivo `.env` para `docker/.env.prod`.

### Requerimentos
Certifique-se de rodar os comandos de requirements

`python -m pip install -r requirements.txt`

### Deploy
Use o Docker para deploy
`docker build -t biblia-api .`

### Teste
`curl --location --request GET 'http://127.0.0.1:3000/search/is/6/8'`
param book/abbrev/verse