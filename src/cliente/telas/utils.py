from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
import platform, subprocess, webbrowser, os
import json

CACHE_PATH = 'src/cliente/cache/cache.json'

def show_popup(message):
    """Função auxiliar que cria e exibe um Popup com título e mensagem."""
    conteudo_vazio = Widget(size_hint=(None, None), size=(0,0))

    popup = Popup(
        title=message,
        content=conteudo_vazio,
        size_hint=(None, None),
        size=(300, 100)
    )

    popup.open()

def cache_search(campo):
        try:
            # Abre o arquivo de cache (supondo que seja um JSON)
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Procura pelo campo "nome" no JSON
            nome_valor = data.get(campo)
            if nome_valor:
                return nome_valor
            else:
                return f"Campo {campo} não encontrado."
        except Exception as e:
            print("Erro ao ler o cache:", e)

def is_wsl():
    try:
        with open('/proc/version', 'r') as f:
            return 'microsoft' in f.read().lower()
    except FileNotFoundError:
        return False

def open_url(url: str):
   
    try:
        if os.name == 'nt':
            os.startfile(url)
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', url])
        elif is_wsl():
            # tenta cmd.exe primeiro
            try:
                subprocess.Popen(['cmd.exe', '/c', 'start', '', url])
            except FileNotFoundError:
                # fallback para PowerShell
                subprocess.Popen(['powershell.exe', 'Start-Process', url])
        else:
            subprocess.Popen(['xdg-open', url])
    except Exception as e:
        print(f'falha no método nativo ({e}), tentando webbrowser…')
        try:
            webbrowser.open(url)
        except Exception as e2:
            print(f'falha no webbrowser: {e2}')
