# TechManager — Sistema de Gestão de TI

Aplicação web demonstrativa para apoiar processos básicos de Gestão de Tecnologia da Informação (GTI), reunindo controle de chamados de suporte e inventário de ativos em um único painel.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-black)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Status-MVP%20acadêmico-success)

## Sobre o projeto

O TechManager simula uma ferramenta interna de uma equipe de suporte de TI. A proposta é demonstrar como processos organizados e informações centralizadas podem contribuir para o acompanhamento de solicitações, a gestão de equipamentos e a tomada de decisão.

## Funcionalidades

- **Dashboard gerencial:** indicadores de chamados abertos, em andamento e concluídos, além do total de ativos.
- **Central de chamados:** registro de solicitações com solicitante, categoria, prioridade e descrição.
- **Acompanhamento:** atualização do status dos chamados.
- **Inventário de ativos:** cadastro de equipamentos com tipo, patrimônio, departamento e situação.
- **Validação de patrimônio:** impede o cadastro de dois equipamentos com a mesma identificação.
- **Banco de dados SQLite:** armazenamento local persistente.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Bootstrap 5

## Como executar localmente

### 1. Pré-requisitos

Instale Python 3.10 ou superior.

### 2. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/techmanager-gti.git
cd techmanager-gti
```

### 3. Crie e ative um ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Execute a aplicação

```bash
python app.py
```

Acesse `http://127.0.0.1:5000` no navegador. O banco SQLite e alguns registros demonstrativos serão criados automaticamente na primeira execução.

## Estrutura do projeto

```text
techmanager-gti/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── tickets.html
│   ├── ticket_form.html
│   ├── assets.html
│   ├── asset_form.html
│   └── 404.html
└── tests/
```

## Relação com Gestão de TI

O projeto aplica conceitos introdutórios de:

- **Gerenciamento de incidentes e solicitações:** registro e acompanhamento de chamados.
- **Gerenciamento de ativos de TI:** inventário e identificação de equipamentos.
- **Indicadores de gestão:** visualização de dados operacionais para apoiar decisões.
- **Padronização de processos:** centralização das informações e definição de status.

O escopo é inspirado em práticas de gerenciamento de serviços, como as difundidas pelo ITIL, sem representar uma implementação oficial ou completa do framework.

## Melhorias futuras

- Autenticação e perfis de acesso (administrador, técnico e solicitante).
- Edição e exclusão de ativos.
- Histórico de movimentação e manutenção dos equipamentos.
- Comentários e histórico de atendimento dos chamados.
- Prazos de atendimento e indicadores de SLA.
- Relatórios com filtros e exportação para CSV/PDF.
- Testes automatizados e implantação em ambiente de produção.

## Observações de segurança

Este repositório é um MVP educacional. Antes de qualquer uso real, é necessário configurar uma chave secreta segura por variável de ambiente, implementar autenticação e autorização, proteção CSRF, validação adicional, logs, backups e configuração de produção. Não utilize dados pessoais ou corporativos reais na demonstração.

## Autoria

Desenvolvido como projeto de portfólio para demonstrar conhecimentos iniciais em Gestão de Tecnologia da Informação e desenvolvimento de aplicações web.

**Autor:** Maxsuel Rodrigues

---

Se este projeto foi útil, considere deixar uma ⭐ no repositório.
