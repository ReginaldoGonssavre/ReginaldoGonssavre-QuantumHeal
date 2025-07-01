# Guia de Deployment - QuantumHeal

Este documento detalha os passos para fazer o deployment do backend (FastAPI) e do frontend (React) da QuantumHeal.

## Pré-requisitos

- Docker e Docker Compose instalados.
- Python 3.9+ e pip (para desenvolvimento local).
- Node.js e npm (para desenvolvimento local do frontend).

## 1. Deployment do Backend (FastAPI)

O backend é empacotado em um contêiner Docker para facilitar o deployment.

### 1.1. Construir a Imagem Docker

Navegue até o diretório `backend` e construa a imagem Docker:

```bash
cd backend
docker build -t quantumheal-backend .
```

### 1.2. Executar o Contêiner Docker

Você pode executar o contêiner diretamente:

```bash
docker run -p 8000:8000 quantumheal-backend
```

Isso iniciará o servidor FastAPI na porta `8000` do seu host.

### 1.3. Deployment com Docker Compose (Recomendado para Desenvolvimento/Produção Simples)

Para orquestrar o backend e o frontend (e futuramente um banco de dados), usaremos Docker Compose. Crie um arquivo `docker-compose.yml` na raiz do projeto `quantum_heal` (será criado na próxima etapa).

## 2. Deployment do Frontend (React)

O frontend também pode ser servido via Docker.

### 2.1. Construir a Imagem Docker (para Produção)

Navegue até o diretório `frontend` e construa a imagem Docker. Este processo irá primeiro construir a aplicação React e depois servi-la com um servidor web leve (como Nginx).

```bash
cd frontend
docker build -t quantumheal-frontend .
```

**Nota:** Você precisará de um `Dockerfile` no diretório `frontend` para isso. (Será criado na próxima etapa).

### 2.2. Executar o Contêiner Docker

```bash
docker run -p 3000:80 quantumheal-frontend
```

Isso servirá a aplicação React na porta `3000` do seu host.

## 3. Orquestração com Docker Compose

Para rodar ambos os serviços (backend e frontend) juntos, crie um arquivo `docker-compose.yml` na raiz do projeto `quantum_heal`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - PYTHONUNBUFFERED=1

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
```

### 3.1. Iniciar os Serviços

Navegue até a raiz do projeto `quantum_heal` e execute:

```bash
docker-compose up --build
```

Isso construirá as imagens (se necessário) e iniciará ambos os contêineres. O frontend estará acessível em `http://localhost:3000` e o backend em `http://localhost:8000`.

### 3.2. Parar os Serviços

```bash
docker-compose down
```

## 4. Deployment em Nuvem (Ex: Azure, GCP)

Para deployment em produção, recomendamos o uso de serviços de contêiner gerenciados, como Azure Container Apps, Google Cloud Run ou Kubernetes Engine.

- **Azure Container Apps / Google Cloud Run:** Ideal para microserviços. Você pode implantar o backend e o frontend como serviços separados.
- **Kubernetes Engine (GKE / AKS):** Para orquestração mais complexa e escalabilidade avançada.

**Passos Gerais:**

1.  Autenticar na sua conta de nuvem.
2.  Construir e enviar as imagens Docker para um registro de contêiner (ex: Azure Container Registry, Google Container Registry).
3.  Criar e configurar os serviços de contêiner na plataforma de nuvem, apontando para as imagens no registro.
4.  Configurar balanceadores de carga e domínios personalizados, se necessário.

*Detalhes específicos de cada plataforma de nuvem serão fornecidos em documentações separadas ou através de tutoriais dos provedores.*