# QuantumHeal - Documentação Técnica

## Visão Geral

QuantumHeal é uma plataforma SaaS B2B, construída sobre a AigroQuantumSaaS, para acelerar a descoberta de medicamentos e a medicina personalizada através de simulação quântica e IA.

Este documento serve como o hub central para toda a documentação técnica do projeto.

## Estrutura do Projeto

```
quantum_heal/
├── .git/            # Repositório Git
├── .gitignore       # Arquivos a serem ignorados pelo Git
├── backend/         # Código do backend (FastAPI, Qiskit)
│   ├── main.py      # Lógica principal da API
│   └── requirements.txt # Dependências Python
│   └── Dockerfile   # Dockerfile para o backend
├── docs/            # Documentação do projeto
│   ├── README.md    # Este arquivo
│   ├── partnerships.md # Estratégia de Parcerias
│   ├── pitch_deck.md # Pitch Deck da Startup
│   ├── deployment.md # Guia de Deployment
├── frontend/        # Código do frontend (React)
│   ├── src/         # Código fonte do React
│   ├── package.json # Dependências Node.js
│   └── Dockerfile   # Dockerfile para o frontend
├── site/            # Site institucional estático
│   └── index.html   # Página principal do site
└── docker-compose.yml # Orquestração de serviços Docker
```

## Como Rodar o Projeto Localmente

Para rodar o backend e o frontend localmente usando Docker Compose, siga estes passos:

1.  **Pré-requisitos:** Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

2.  **Navegue até o diretório raiz do projeto:**
    ```bash
    cd quantum_heal
    ```

3.  **Inicie os serviços:**
    ```bash
    docker-compose up --build
    ```
    Este comando construirá as imagens Docker para o backend e o frontend (se ainda não existirem) e iniciará os contêineres.

4.  **Acesse a aplicação:**
    -   **Frontend:** Abra seu navegador e acesse `http://localhost:3000`
    -   **Backend API (Docs):** Acesse `http://localhost:8000/docs` para a documentação interativa da API (Swagger UI).

5.  **Para parar os serviços:**
    ```bash
    docker-compose down
    ```

## Documentação da API

O backend da QuantumHeal é construído com FastAPI, que gera automaticamente uma documentação interativa da API (Swagger UI) e uma especificação OpenAPI.

-   **Swagger UI:** Acesse `http://localhost:8000/docs`
-   **Redoc:** Acesse `http://localhost:8000/redoc`

### Endpoints Principais:

-   `GET /`: Health check da API.
-   `POST /simulate`: Inicia uma simulação de química quântica para uma molécula. Aceita um objeto `Molecule` no corpo da requisição e retorna um `SimulationResult`.

Para detalhes completos sobre os modelos de dados (`Molecule`, `SimulationResult`) e os parâmetros de cada endpoint, consulte a documentação interativa da API.

## Próximos Passos

1.  Implementar a Prova de Conceito da simulação quântica.
2.  Desenvolver o MVP do frontend.
3.  Criar o Pitch Deck e o site institucional.
4.  **Adicionar estratégia de testes.**
5.  **Definir pipeline de CI/CD.**
6.  **Documentar considerações de segurança.**
7.  **Listar futuras melhorias e roadmap.**