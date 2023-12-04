# 📜 Como executar localmente

### 📌 Ative o ambiente virtual:

```bash
. .venv/bin/activate
```

### 📌 Instale as dependências:

-   Ative o ambiente virtual e use o pip para instalar:

```bash
pip install django

pip install djangorestframework 

pip install psycopg2-binary

pip install django-cors-headers 

pip install pika
```

### 📌 Inicialize os serviços do Docker:

```bash
docker compose build --no-cache

docker compose up -d
```

### 📌 Vá para o diretório da aplicação e rode o servidor:

```bash
python3 manage.py runserver
```
