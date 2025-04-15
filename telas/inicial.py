from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
import requests

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
        btn_twitter = Button(text="Twitter", size_hint=(1, None), height=dp(40))
        btn_linkedin = Button(text="LinkedIn", size_hint=(1, None), height=dp(40))
        # Você pode vincular ações específicas a cada botão, se necessário:
        btn_facebook.bind(on_press=lambda instance: print("Login com Facebook"))
        btn_google.bind(on_press=lambda instance: print("Login com Google"))
        btn_twitter.bind(on_press=lambda instance: print("Login com Twitter"))
        btn_linkedin.bind(on_press=lambda instance: print("Login com LinkedIn"))
        
        social_layout.add_widget(btn_facebook)
        social_layout.add_widget(btn_google)
        social_layout.add_widget(btn_twitter)
        social_layout.add_widget(btn_linkedin)
        main_layout.add_widget(social_layout)
        
        # Botão ou link de "Esqueci minha senha"
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
                # Constrói a URL para a requisição GET.
                # Supondo que o endpoint seja algo como:
                # http://localhost:5000/api/usuario/<email>
                url = f"http://localhost:5000/api/usuario/{usuario}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    print("Usuário encontrado:", data)
                    
                    self.manager.current = "principal"
                    # Aqui você pode adicionar lógica para verificar a senha recebida 
                    # (por exemplo, enviando um token ou comparando com algum valor)
                else:
                    print("Erro: Usuário não encontrado ou erro no servidor. Status Code:", response.status_code)
            except Exception as e:
                print("Erro ao realizar a requisição GET:", e)
        else:
            print("Preencha todos os campos.")
    
    def ir_para_cadastro(self,instance):
        self.manager.current = "cadastro" 

    def ir_para_principal(self,instance):
        self.manager.current = "principal"
