CLIENT_DIR = src/cliente
API_DIR = src
SRC_DIR = src

# Comando para rodar a aplicação do cliente
run-client:
	@echo "Iniciando a aplicação cliente..."
	PYTHONPATH=$(CLIENT_DIR) python3 -m telas.main

# Comando para rodar a aplicação da API
run-api:
	@echo "Iniciando a aplicação da API..."
	PYTHONPATH=$(SRC_DIR) python3 -m $(API_DIR).api.app

# Comando padrão (executa as duas aplicações)
run-all: run-client run-api
	@echo "Ambas as aplicações foram iniciadas."