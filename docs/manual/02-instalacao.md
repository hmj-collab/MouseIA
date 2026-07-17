# Capítulo 2: Guia de Instalação e Configuração

Este capítulo apresenta o passo a passo completo para instalação da plataforma Mouse IA em ambiente local de desenvolvimento ou homologação.

---

## 1. Instalação do Backend

### Requisitos Prévios
* **Python 3.9+** instalado no sistema.
* Gerenciador de pacotes **pip**.

### Passo a Passo
1. Navegue até o diretório do backend:
   ```bash
   cd backend
   ```
2. Crie e ative um ambiente virtual (venv):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instale as dependências requeridas pelo projeto:
   ```bash
   pip install -r requirements.txt
   ```
4. Aplique as migrações do banco de dados utilizando o Alembic (isso criará as tabelas e relacionamentos necessários no banco SQLite/Postgres):
   ```bash
   alembic upgrade head
   ```
5. Inicie o servidor FastAPI em modo de recarga automática (hot reload):
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   *O backend estará acessível no endereço [http://127.0.0.1:8000](http://127.0.0.1:8000).*

---

## 2. Instalação do Frontend

### Requisitos Prévios
* **Node.js** (versão 18 ou superior) instalado.
* Gerenciador de pacotes **npm**.

### Passo a Passo
1. Navegue até o diretório do frontend:
   ```bash
   cd frontend
   ```
2. Instale os pacotes npm necessários:
   ```bash
   npm install
   ```
3. Inicie o servidor de desenvolvimento Vite:
   ```bash
   npm run dev
   ```
   *O frontend estará disponível localmente em [http://localhost:5173](http://localhost:5173) ou [http://localhost:3000](http://localhost:3000).*

---

## 3. Configuração de Variáveis de Ambiente e Chaves de API
O Mouse IA armazena suas credenciais de segurança e configurações locais no arquivo `.env` localizado na raiz do projeto (ou dentro da pasta `backend`).

### Configurando o arquivo `.env`
Duplique o arquivo `.env.example` para `.env` e preencha as variáveis de acordo com suas necessidades:

```env
# Configurações Gerais
PROJECT_NAME="Mouse IA"
SECRET_KEY="SUA_CHAVE_SECRETA_JWT_AQUI"
ACCESS_TOKEN_EXPIRE_MINUTES=11520  # 8 dias

# Banco de Dados
DATABASE_URL="sqlite:///./mouseia.db"  # Para SQLite local
# DATABASE_URL="postgresql://usuario:senha@localhost:5432/mouseia"  # Para PostgreSQL

# Integrações de IA
GEMINI_API_KEY="AIzaSyYourActualGoogleGeminiApiKeyHere"
```

> [!NOTE]
> Se a variável `GEMINI_API_KEY` não for configurada no arquivo `.env` ou contiver valores fictícios padrão (como `your_gemini_api_key`), a plataforma executará automaticamente um **Fallback Mock Offline**. Isso permite testar todo o fluxo do sistema mesmo sem conexão ativa ou chave válida do Gemini.

---

## 4. Execução de Testes Automatizados
A plataforma conta com uma suíte de testes de integração e testes unitários cobrindo o Correlation Engine, as regras de Threat Intelligence e a geração de análises de IA.

1. Garanta que o ambiente virtual está ativo:
   ```bash
   source .venv/bin/activate
   ```
2. Execute o comando de testes a partir da pasta `/backend`:
   ```bash
   pytest
   ```
3. Para obter mais detalhes ou cobertura de testes, você pode executar:
   ```bash
   pytest -v
   ```
