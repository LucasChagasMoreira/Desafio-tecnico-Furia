from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
import json
import requests
import threading
from telas.utils import open_url, CACHE_PATH, show_popup
import time

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"

        # Fundo com gradiente suave
        with self.canvas.before:
            Color(0.12, 0.15, 0.2, 1)  # Azul escuro mais moderno
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: setattr(self._bg, 'pos', self.pos),
                  size=lambda *a: setattr(self._bg, 'size', self.size))

        # Layout principal com margens responsivas
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(30), dp(20), dp(30)],
            spacing=dp(10)
        )

        # Cabeçalho com logo/título
        header = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(80),
            padding=[0, dp(20), 0, dp(10)]
        )
        
        # Título mais elegante
        header.add_widget(Label(
            text="FURIA",
            font_size=dp(32),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(40)
        ))
        
        header.add_widget(Label(
            text="Sistema de Monitoramento",
            font_size=dp(16),
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(1, None),
            height=dp(20)
        ))
        
        main_layout.add_widget(header)

        # Container centralizado do formulário com sombra
        container = AnchorLayout(anchor_x='center', anchor_y='center')
        
        # Card estilo Material Design
        card = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(360), dp(480)),
            padding=[dp(30), dp(30), dp(30), dp(30)],
            spacing=dp(15)
        )
        
        # Adiciona "sombra" ao card usando retângulo com cor de fundo
        with card.canvas.before:
            Color(0.18, 0.2, 0.25, 1)  # Cor um pouco mais clara que o fundo
            self._card_bg = Rectangle(pos=card.pos, size=card.size, radius=[(dp(8), dp(8)) for _ in range(4)])
        card.bind(pos=lambda *a: setattr(self._card_bg, 'pos', card.pos),
                  size=lambda *a: setattr(self._card_bg, 'size', card.size))
        
        
        # Email
        email_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(70),
            spacing=dp(5)
        )
        
        email_container.add_widget(Label(
            text="E-mail",
            size_hint=(1, None),
            height=dp(20),
            halign='left',
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        self.username = TextInput(
            hint_text="Digite seu e-mail",
            hint_text_color=(0.6, 0.6, 0.6, 1),
            multiline=False,
            size_hint=(1, None),
            height=dp(45),
            background_normal='',
            background_active='',
            background_color=(0.22, 0.25, 0.3, 1),  # Fundo mais escuro para o input
            foreground_color=(1, 1, 1, 1),  # Texto branco
            cursor_color=(0.8, 0.8, 0.8, 1),
            padding=[dp(15), dp(12)],
            font_size=dp(16)
        )
        email_container.add_widget(self.username)
        card.add_widget(email_container)
        
        # Senha
        senha_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(70),
            spacing=dp(5)
        )
        
        senha_container.add_widget(Label(
            text="Senha",
            size_hint=(1, None),
            height=dp(20),
            halign='left',
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        self.password = TextInput(
            hint_text="Digite sua senha",
            hint_text_color=(0.6, 0.6, 0.6, 1),
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=dp(45),
            background_normal='',
            background_active='',
            background_color=(0.22, 0.25, 0.3, 1),  # Fundo mais escuro para o input
            foreground_color=(1, 1, 1, 1),  # Texto branco
            cursor_color=(0.8, 0.8, 0.8, 1),
            padding=[dp(15), dp(12)],
            font_size=dp(16)
        )
        senha_container.add_widget(self.password)
        card.add_widget(senha_container)
        
        # Botão de login principal com cor de destaque
        btn_login = Button(
            text="ENTRAR",
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),  # Azul destaque
            color=(1, 1, 1, 1),
            font_size=dp(16),
            bold=True
        )
        btn_login.bind(on_press=self.fazer_login)
        card.add_widget(btn_login)
        
        # Separador "OU"
        separator = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(40)
        )
        
        line_left = Widget(size_hint=(1, None), height=dp(1))
        with line_left.canvas:
            Color(0.3, 0.3, 0.3, 1)
            Line(points=[0, dp(0.5), line_left.width, dp(0.5)], width=1)
        
        separator.add_widget(line_left)
        
        separator.add_widget(Label(
            text="OU",
            size_hint=(None, None),
            size=(dp(40), dp(20)),
            color=(0.7, 0.7, 0.7, 1)
        ))
        
        line_right = Widget(size_hint=(1, None), height=dp(1))
        with line_right.canvas:
            Color(0.3, 0.3, 0.3, 1)
            Line(points=[0, dp(0.5), line_right.width, dp(0.5)], width=1)
        
        separator.add_widget(line_right)
        card.add_widget(separator)
        
        # Botões sociais com ícones modernos
        social_container = GridLayout(
            cols=2, 
            spacing=dp(15), 
            size_hint=(1, None), 
            height=dp(50),
            padding=[0, dp(5)]
        )
        
        # Botão Facebook
        facebook_btn = Button(
            text="Facebook",
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_color=(0.23, 0.35, 0.6, 1),  # Azul Facebook
            color=(1, 1, 1, 1)
        )
        facebook_btn.bind(on_press=self.on_facebook_login)
        social_container.add_widget(facebook_btn)
        
        # Botão Google
        google_btn = Button(
            text="Google",
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_color=(0.95, 0.27, 0.21, 1),  # Vermelho Google
            color=(1, 1, 1, 1)
        )
        google_btn.bind(on_press=self.on_google_login)
        social_container.add_widget(google_btn)
        
        card.add_widget(social_container)
        
        # Botão de criar conta
        card.add_widget(Widget(size_hint=(1, None), height=dp(10)))  # Espaçador
        
        criar_conta_btn = Button(
            text="CRIAR NOVA CONTA",
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_color=(0.25, 0.28, 0.33, 1),  # Cinza escuro
            color=(0.8, 0.8, 0.8, 1)
        )
        criar_conta_btn.bind(on_press=self.ir_para_cadastro)
        card.add_widget(criar_conta_btn)
        
        container.add_widget(card)
        main_layout.add_widget(container)
        self.add_widget(main_layout)
        
    def fazer_login(self, instance):
        u = self.username.text
        s = self.password.text
        if not u or not s:
            show_popup("Preencha todos os campos.")
            return
        try:
            r = requests.get(f"http://localhost:5000/api/usuario/{u}")
            if r.status_code == 200:
                with open(CACHE_PATH, "w", encoding="utf-8") as f:
                    json.dump(r.json(), f, indent=4, ensure_ascii=False)
                self.manager.current = "principal"
            else:
                print(f"Erro: {r.status_code}")
        except Exception as e:
            print("Erro ao conectar:", e)

    def on_google_login(self, instance):
        open_url('http://localhost:5000/auth/login')
        threading.Thread(target=self._poll, daemon=True).start()

    def on_facebook_login(self, instance):
        try:
            r = requests.get('http://localhost:5000/auth/facebook')
            r.raise_for_status()
            with open(CACHE_PATH, 'w', encoding='utf-8') as f:
                json.dump(r.json(), f, indent=4, ensure_ascii=False)
            self.manager.current = 'perfil'
        except Exception as e:
            print("Erro Facebook:", e)

    def _poll(self):
        url = 'http://localhost:5000/auth/credentials'
        while True:
            try:
                r = requests.get(url)
                r.raise_for_status()
                creds = r.json()
                if creds.get('Nome'):
                    Clock.schedule_once(lambda dt: self._save(creds))
                    return
            except:
                pass
            time.sleep(1)

    def _save(self, creds):
        with open(CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump(creds, f, indent=4, ensure_ascii=False)
        self.manager.current = 'perfil'

    def ir_para_cadastro(self, instance):
        self.manager.current = "cadastro"