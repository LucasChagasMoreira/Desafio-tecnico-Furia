# Variáveis de ambiente
PYTHON = python3
PIP = pip
VENV = venv

# Diretórios
SRC_DIR = src
TEST_DIR = tests

# Comandos
VENV_DIR = $(VENV)

# Instalar dependências
#install: $(VENV_DIR)/bin/activate
#	$(VENV_DIR)/bin/pip install -r requirements.txt

# Criar o ambiente virtual
$(VENV_DIR)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

# Rodar o servidor
run: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/python -m api.app

clean:
	rm -rf $(VENV_DIR) __pycache__

# Gerar o arquivo de dependências
dependencies:
	$(PIP) freeze > requirements.txt

# Para rodar o projeto, use:
# make run
