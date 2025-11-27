# INF1407 - Trabalho 2 - Backend (API)

Este repositório contém o **Back-end** do Trabalho 2 de Programação para Web (2025/2). O projeto consiste em uma API RESTful desenvolvida com Django Rest Framework (DRF) para gerenciar um sistema de avaliação de jogos.

## Membros do Grupo
* **Felipe de Aragão Falcão** - Matrícula: 2120360
* **Ricardo Bastos Leta Vieira** - Matrícula: 2110526

---

## Links Importantes

* **Este Repositório (Backend):** [https://github.com/ricleta/INF1407-Trabalho2-Back](https://github.com/ricleta/INF1407-Trabalho2-Back)
* **Repositório do Frontend:** [https://github.com/ricleta/INF1407-Trabalho2-Front](https://github.com/ricleta/INF1407-Trabalho2-Front)
* **API Publicada (Deploy):** [https://ricleta.pythonanywhere.com/](https://ricleta.pythonanywhere.com/)
* **Frontend Publicado (Github Pages):** [https://ricleta.github.io/INF1407-Trabalho2-Front/](https://ricleta.github.io/INF1407-Trabalho2-Front/)

> **Documentação Interativa (Swagger):** [https://ricleta.pythonanywhere.com/swagger/](https://ricleta.pythonanywhere.com/swagger/)

---

## Escopo do Backend

O backend foi desenvolvido exclusivamente como uma API, sem renderização de templates HTML para o usuário final. Suas principais características são:

* **Framework:** Django 4.2 + Django Rest Framework (DRF).
* **Banco de Dados:** SQLite (padrão do Django).
* **Autenticação:** Token Authentication (DRF).
* **Permissões:** Controle de acesso baseado em grupos (`developer` e `reviewer`) e autenticação (`IsAuthenticatedOrReadOnly`).
* **Documentação:** Swagger/OpenAPI gerado automaticamente via `drf-yasg`.
* **Funcionalidades:**
    * CRUD de Jogos e Avaliações.
    * Registro de usuários e atribuição de grupos.
    * Endpoints de segurança (Login, Logout, Troca de Senha, Esqueci a Senha via e-mail SMTP).

---

## Instruções de Instalação e Execução Local

1.  **Clonar o repositório:**
    ```bash
    git clone [https://github.com/ricleta/INF1407-Trabalho2-Back.git](https://github.com/ricleta/INF1407-Trabalho2-Back.git)
    cd INF1407-Trabalho2-Back
    ```

2.  **Criar e ativar o ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instalar dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar o Banco de Dados:**
    Execute as migrações para criar as tabelas e os grupos de usuário padrão:
    ```bash
    python manage.py migrate
    ```

5.  **Executar o servidor:**
    ```bash
    python manage.py runserver
    ```
    A API estará disponível em `http://localhost:8000/`.

---

## Relato de Desenvolvimento (Backend)

### O que funcionou
* **Arquitetura REST:** A separação total das views em `APIView` e `ViewSets` retornando apenas JSON funcionou perfeitamente, permitindo que o frontend fosse completamente independente.
* **Autenticação e Grupos:** A lógica de criar grupos (`developer`, `reviewer`) via *signals* pós-migração e verificar permissões nas Views garantiu a segurança dos endpoints.
* **Swagger:** A integração com `drf_yasg` facilitou muito o teste dos endpoints sem precisar do frontend pronto.
* **Recuperação de Senha: (Possivelmente alterar)** A configuração do envio de e-mail (SMTP Relay) para resgate de senha foi implementada com sucesso na `ForgotPasswordView`.

### O que não funcionou
* **Mensagens de Erro: (Possivelmente alterar)** O DRF retorna erros de validação em formatos variados (às vezes lista, às vezes dicionário). Isso gerou dificuldade para padronizar o tratamento desses erros no frontend.
* [cite_start]**CORS: (Possivelmente alterar)** Durante o desenvolvimento local, configurar o `django-cors-headers` corretamente para aceitar requisições do frontend rodando em portas diferentes exigiu ajustes nas configurações[cite: 29].

---

## Critérios Atendidos (Backend)
* [x] Desenvolvido em Django (sem templates HTML de usuário).
* [x] CRUD completo (Banco de Dados).
* [x] Publicado em provedor Web (PythonAnywhere).
* [x] Endpoints protegidos (Token Auth).
* [x] Documentação Swagger.