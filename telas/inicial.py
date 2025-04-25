from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock
import json
import requests
import threading
import os
from utils import open_url
import time

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"

        # Layout principal vertical
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Título
        title_label = Label(text="Login", font_size="24sp", size_hint=(1, 0.2))
        main_layout.add_widget(title_label)
        
        # Formulário de login
        form_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint=(1, 0.35))
        self.username_input = TextInput(
            hint_text="E-mail ou usuário",
            multiline=False,
            size_hint=(1, None),
            height=dp(40)
        )
        self.password_input = TextInput(
            hint_text="Senha",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=dp(40)
        )
        # Botão de login
        login_button = Button(
            text="Entrar",
            size_hint=(1, None),
            height=dp(40)
        )
        login_button.bind(on_press=self.fazer_login)
        form_layout.add_widget(self.username_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(login_button)
        main_layout.add_widget(form_layout)
        
        # Login com redes sociais (2 colunas)
        social_layout = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.25))
        btn_facebook = Button(text="Facebook", size_hint=(1, None), height=dp(40))
        btn_google = Button(text="Google", size_hint=(1, None), height=dp(40))
        
        #btn_facebook.bind(on_press=self.on_facebook_login)
        btn_google.bind(on_press=self.on_google_login)
        
        social_layout.add_widget(btn_facebook)
        social_layout.add_widget(btn_google)
        main_layout.add_widget(social_layout)
        
        # Botão ou link de "criar conta"
        create_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        create_button = Button(text="Criar Conta", size_hint=(1, 1))
        create_button.bind(on_press=self.ir_para_cadastro)
        create_layout.add_widget(create_button)
        main_layout.add_widget(create_layout)
        
        self.add_widget(main_layout)

    def fazer_login(self, instance):
        # Captura as entradas do usuário
        usuario = self.username_input.text
        senha = self.password_input.text
        print("Tentando login com:", usuario)
        
        # Verifica se os campos não estão vazios
        if usuario and senha:
            try:

                url = f"http://localhost:5000/api/usuario/{usuario}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    print("Usuário encontrado:", data)
                    
                    # Salva os dados retornados no arquivo JSON "cache.json"
                    try:
                        with open("../cache/cache.json", "w", encoding="utf-8") as cache_file:
                            json.dump(data, cache_file, indent=4)
                        print("Dados salvos no cache com sucesso!")
                    except Exception as cache_error:
                        print("Erro ao salvar o cache:", cache_error)

                    self.manager.current = "principal"
                else:
                    print("Erro: Usuário não encontrado ou erro no servidor. Status Code:", response.status_code)
            except Exception as e:
                print("Erro ao realizar a requisição GET:", e)
        else:
            print("Preencha todos os campos.")
    
    def on_google_login(self, instance):
        # 1) abre o browser para o OAuth
        open_url('http://localhost:5000/auth/login')
        # 2) dispara o polling em background
        threading.Thread(target=self._poll_for_credentials, daemon=True).start()

    def _poll_for_credentials(self):
        url = 'http://localhost:5000/auth/credentials'
        while True:
            try:
                resp = requests.get(url)
                resp.raise_for_status()
                creds = resp.json()
                print(creds)
                # suponha que seu backend devolva um campo 'access_token'
                if creds.get('Nome'):
                    Clock.schedule_once(lambda dt: self._on_credentials_received(creds))
                    return
            except Exception:
                pass
            time.sleep(1)  # espera 1s antes de tentar de novo

    def _on_credentials_received(self, creds):
    
        try:
            cache_path = "../cache/cache.json"
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(creds, f)
            print(f'Credenciais salvas em {cache_path}')
        except Exception as e:
            print(f'Erro ao salvar credenciais no cache: {e}')

        # 2) Navega para a tela de perfil
        self.manager.current = 'perfil'
    
    def _on_auth_failure(self):
            print("Timeout: não recebeu credenciais do Flask")

    def ir_para_cadastro(self,instance):
        self.manager.current = "cadastro" 

    def ir_para_principal(self,instance):
        self.manager.current = "principal"
