# AI Image Classifier + MySQL (Local)

Pipeline:

-   Receebe uma imagem
-   Computa SHA256 (deduplication)
-   Gera, no formato "description \| category", uma descricao, usando LLaVA via Ollama (local)
-   Armazena os dados por MySQL (Docker)

------------------------------------------------------------------------

## Requisitos

-   Python 3.10+
-   Docker Desktop
-   Ollama (with LLaVA model installed)

------------------------------------------------------------------------

## Setup

### 1) MySQL (Docker)

``` bash
docker run --name imagedescription-mysql \
  -e MYSQL_ROOT_PASSWORD=senha123 \
  -e MYSQL_DATABASE=smartimg \
  -p 3306:3306 \
  -d mysql:8
```

------------------------------------------------------------------------

### 2) Aplicar Schema

PowerShell:

``` bash
get-content .\schema.sql | docker exec -i imagedescription-mysql mysql -uroot -psenha123
```

------------------------------------------------------------------------

### 3) Download Vision Model

``` bash
ollama pull llava
```

------------------------------------------------------------------------

### 4) Python Environment

``` bash
python -m venv .venv
```

PowerShell:

``` bash
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Rodar

``` bash
python main.py testimage0.jpg
```

------------------------------------------------------------------------

## Verificar database

``` bash
docker exec -it imagedescription-mysql mysql \
  -uroot -psenha123 \
  -e "use smartimg; select id, filename, category from images order by id desc limit 10;"
```

------------------------------------------------------------------------

## Arquitetura

-   ai.py → chama LLaVA via Ollama (local inference)
-   db.py → relaciona com o MySQL 
-   main.py → pipeline completa (hash + dedup + AI + insert)
-   schema.sql → definicoes da tabela 

------------------------------------------------------------------------

## Notes

-   Totalmente local e sem cust
-   Deduplication por SHA256
-   Design modular
