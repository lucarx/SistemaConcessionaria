# Sistema de Concessionária

Um sistema completo de gerenciamento para concessionárias de veículos, desenvolvido em Python com SQLite, oferecendo tanto interface de terminal quanto interface gráfica.

## Características

- **Dupla Interface**: Terminal e GUI (tkinter)
- **Base de Dados SQLite**: Armazenamento local eficiente
- **Gestão Completa**: Veículos, clientes, vendas e funcionários
- **Relatórios**: Estatísticas e resumos de vendas
- **Busca Avançada**: Pesquisa de veículos por múltiplos critérios
- **Interface Intuitiva**: Fácil de usar em ambas as modalidades

## Funcionalidades

### Gestão de Veículos
- Adicionar, editar e remover veículos
- Controle de status (Disponível/Vendido)
- Informações detalhadas (marca, modelo, ano, cor, preço, quilometragem, etc.)

### Gestão de Clientes
- Cadastro completo de clientes
- Informações de contato e documentação
- Histórico de compras

### Gestão de Vendas
- Registro de vendas com detalhes completos
- Associação cliente-veículo
- Métodos de pagamento
- Observações e notas

### Gestão de Funcionários
- Cadastro de funcionários
- Informações de cargo e salário
- Controle de acesso

### Relatórios
- Resumo de vendas
- Estatísticas gerais
- Veículos disponíveis
- Total de clientes

## Instalação

1. **Clone ou baixe o projeto**
2. **Certifique-se de ter Python 3.6+ instalado**
3. **Execute o sistema:**

\`\`\`bash
python main.py
\`\`\`

## Uso

### Primeira Execução

1. Execute `python main.py`
2. Escolha a opção "3. Inicializar Base de Dados"
3. Isso criará a base de dados SQLite e populará com dados de exemplo

### Interfaces Disponíveis

#### Interface de Terminal
- Navegação por menus numerados
- Ideal para servidores ou sistemas sem interface gráfica
- Todas as funcionalidades disponíveis

#### Interface Gráfica (GUI)
- Interface moderna com tkinter
- Tabelas interativas
- Formulários intuitivos
- Ideal para uso desktop

## Estrutura do Projeto

\`\`\`
sistema-concessionaria/
├── main.py                 # Ponto de entrada principal
├── database.py             # Gerenciador de base de dados
├── terminal_interface.py   # Interface de terminal
├── gui_interface.py        # Interface gráfica
├── scripts/
│   ├── create_database.py  # Criação da base de dados
│   └── seed_database.py    # Dados de exemplo
├── data/
│   └── dealership.db       # Base de dados SQLite (criada automaticamente)
├── requirements.txt        # Dependências (apenas bibliotecas padrão)
└── README.md              # Este arquivo
\`\`\`

## Base de Dados

O sistema utiliza SQLite com as seguintes tabelas:

- **vehicles**: Informações dos veículos
- **customers**: Dados dos clientes
- **sales**: Registros de vendas
- **employees**: Informações dos funcionários

## Exemplos de Uso

### Adicionar um Veículo (Terminal)
1. Escolha "1. Gerenciar Veículos"
2. Escolha "1. Adicionar Veículo"
3. Preencha as informações solicitadas

### Registrar uma Venda (GUI)
1. Clique em "Vendas"
2. Clique em "Registrar Venda"
3. Selecione cliente e veículo
4. Defina preço e método de pagamento
5. Clique em "Registrar Venda"

## Personalização

O sistema é facilmente extensível:

- **Novos campos**: Modifique `database.py` e as interfaces
- **Novos relatórios**: Adicione métodos em `DatabaseManager`
- **Nova interface**: Implemente seguindo o padrão das existentes

## Requisitos do Sistema

- Python 3.6 ou superior
- SQLite3 (incluído no Python)
- tkinter (incluído na maioria das instalações Python)

### Instalação do tkinter (se necessário)

- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **CentOS/RHEL**: `sudo yum install tkinter`
- **macOS/Windows**: Geralmente já incluído

## Suporte

Este sistema foi desenvolvido para ser robusto e fácil de usar. Em caso de problemas:

1. Verifique se o Python 3.6+ está instalado
2. Certifique-se de que o tkinter está disponível (para GUI)
3. Verifique as permissões de escrita na pasta do projeto
4. Execute a inicialização da base de dados se for a primeira vez

## Licença

Este projeto é de código aberto e pode ser usado e modificado livremente.
