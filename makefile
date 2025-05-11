CLIENT_DIR = src/cliente
API_DIR    = src
SRC_DIR    = src

VENV_DIR = .venv
PYTHON   = $(VENV_DIR)/bin/python
PIP      = $(PYTHON) -m pip

# Dependencies file
REQS = requirements.txt

.PHONY: venv install run-client run-api run-all

# Cria o ambiente virtual se não existir e atualiza pip
venv:
	@sudo apt install -y libmtdev1
	@sudo apt install -y xclip xsel
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@echo "Ambiente virtual pronto em $(VENV_DIR)"
	@$(PYTHON) -m ensurepip --upgrade
	@$(PIP) install --upgrade pip
	
     
# Instala as dependências no virtualenv
install: venv
	@echo "Instalando dependências..."
	@$(PIP) install -r $(REQS)
	@echo "Instalando Tesseract OCR (sistema)..."
	@sudo apt-get update && sudo apt-get install -y tesseract-ocr
	@sudo apt-get install tesseract-ocr-por
	@echo "Dependências instaladas."

# Comando para rodar a aplicação do cliente
run-client:
	@echo "Iniciando a aplicação cliente..."
	PYTHONPATH=$(CLIENT_DIR) $(PYTHON) -m telas.main

# Comando para rodar a aplicação da API
run-api:
	@echo "Iniciando a aplicação da API..."
	PYTHONPATH=$(SRC_DIR) $(PYTHON) -m $(API_DIR).api.app

run-all:
	@echo "Iniciando cliente e API em paralelo..."
	-@lsof -ti tcp:5000 | xargs -r kill -9
	@$(MAKE) run-api &
	@$(MAKE) run-client &
	
	@wait