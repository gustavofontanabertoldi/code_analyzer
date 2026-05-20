# 🔍 Automated Code Analyzer (ISO/IEC 25010)

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Maven](https://img.shields.io/badge/Maven-3.9+-orange.svg)
![Java](https://img.shields.io/badge/Java-21-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Sistema de auditoria técnica automatizada focado na análise estática e dinâmica de repositórios **Java (Maven)**. A ferramenta avalia o código-alvo e emite um parecer de conformidade técnico com base nos modelos de qualidade da norma **ISO/IEC 25010**.

---

## 🏗️ Arquitetura do Sistema (Pilares ISO 25010)

O projeto foi desenvolvido de forma estritamente modular, dividindo-se em 4 grandes inteligências de negócio:

### Módulo I: Manutenibilidade (Análise Estática)
* **Complexidade Ciclomática (McCabe):** Análise de ramificações lógicas (`if`, `else if`, `else`) via Árvore de Sintaxe Abstrata (AST) com mapeamento de risco.
* **Acoplamento entre Objetos (CBO):** Medição de interdependência de classes únicas.
* **Duplicação de Código (Dryness):** Detecção de blocos idênticos de código (mínimo de 5 linhas consecutivas).

### Módulo II: Eficiência de Desempenho (Análise Dinâmica)
* **Benchmarking Automático:** Inicialização automatizada do servidor alvo e medição de tempo de resposta em rotas críticas.
* **Análise de Latência sob Estresse:** Disparos assíncronos concorrentes simulando cargas escalonadas (100, 500, 1000 e 5000 requisições) com cálculo percentual de degradação.

### Módulo III: Confiabilidade (Testabilidade)
* **Cobertura de Testes (Coverage):** Integração com o ecossistema **JaCoCo** para leitura e extração de porcentagem real de linhas de código cobertas por testes unitários.
* **Mecanismo de Fallback:** Tolerância a falhas caso o repositório alvo não possua testes configurados, garantindo a robustez do parser.

### Módulo IV: Tomada de Decisão & Relatório
* **Fábrica de Relatórios (Jinja2):** Consolidação de dados em um Dashboard HTML interativo e responsivo.
* **Tomada de Decisão:** Algoritmo que analisa os thresholds da ISO 25010 e emite o veredito final automatizado (*Aprovado / Reprovado com justificativa*).

---

## 📂 Estrutura do Projeto

```text
CODE_ANALYZER/
├── modules/               # Núcleo de análise do sistema
|   ├── benchmark.py       # Cálculo de tempo de uma única request no servidor
│   ├── complexity.py      # Cálculo de McCabe (AST javalang)
|   ├── coupling.py        # Cálculo do CBO
|   ├── coverage.py        # Parser do relatório XML do JaCoCo
|   ├── duplication.py     # Verifica número de duplicações em blocos de 5 linhas
│   ├── latency.py         # Testes de estresse assíncronos (aiohttp)
│   └── report.py          # Mecanismo de renderização HTML (Jinja2)
├── utils/                 # Utilitários de sistema e infraestrutura
|   ├── endpoints_detector.py # Encontra os endpoints do servidor spring-boot
|   ├── file_utils.py      # Faz o filtro e lista os arquivos .java do repositório
|   ├── git_utils.py       # Realiza o clone do repositório pelo link do github
│   ├── java_parser.py     # Inicializador do parser AST
│   ├── project_detector.py # Detecta versão do projeto java e se existe DB
|   └── server_utils.py    # Controle de subprocessos do servidor Java
├── temp/                  # Diretório volátil para clonagem do Blind Test
├── config.py              # Definições de caminhos e constantes globais
├── main.py                # Orquestrador principal do sistema (Maestro)
└── requirements.txt       # Dependências do projeto Python
```

---

## 🐍 Como Executar o Projeto

### Requisitos:
- Python 3.12 ou superior
- Java Development Kit (JDK) 21
- Apache Maven configurado nas variáveis de ambiente (mvn)

### Clonar este repositório
```code
git clone https://github.com/gustavofontanabertoldi/code_analyzer.git
```
Depois abra o repositório dentro do VScode

### Configurar Ambiente Virtual
```code
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual

# No Windows:
.venv\Scripts\activate

# No Linux/Mac:
source .venv/bin/activate
```

### Instale as Dependencias
```code
pip install -r requirements.txt

```

### Execute o Projeto
```code
python main.py

```
Insira a URL do repositório Java solicitada pelo prompt. O sistema processará o código em tempo real e gerará o arquivo dashboard_qualidade.html na raiz do projeto.
