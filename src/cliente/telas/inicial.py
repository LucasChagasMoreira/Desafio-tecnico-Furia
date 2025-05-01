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
from kivy.graphics import Color, Rectangle
import json
import requests
import threading
from telas.utils import open_url, CACHE_PATH
import time

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"

        # fundo cinza escuro
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: setattr(self._bg, 'pos', self.pos),
                  size=lambda *a: setattr(self._bg, 'size', self.size))

        main = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(40)
        )

        # Título
        main.add_widget(Label(
            text="Desafio técnico Furia",
            font_size="24sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(40)
        ))

        # Container centralizado
        container = AnchorLayout(anchor_x='center', anchor_y='center')
        form = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint=(None, None),
            size=(dp(300), dp(320))
        )

        # Legenda e E-mail / usuário
        form.add_widget(Label(
            text="E-mail ou usuário",
            size_hint=(1, None),
            height=dp(20),
            color=(1, 1, 1, 1)
        ))
        self.username = TextInput(
            hint_text="Digite seu e-mail ou usuário",
            hint_text_color=(0.5, 0.5, 0.5, 1),  # cinza claro para o texto de dica
            multiline=False,
            size_hint=(1, None),
            height=dp(45),
            background_normal='',  # Sem fundo padrão
            background_active='',  # Sem fundo ativo
            background_color=(1, 1, 1, 1),  # Fundo branco para o campo de entrada
            foreground_color=(0.5, 0.5, 0.5, 1),  # Cinza médio para o texto
            cursor_color=(0, 0, 0, 1),  # Cor do cursor (preto)
            padding=(dp(12), dp(12))
        )

        # Desenha a borda fora da área de texto (não sobre o texto)
        
        form.add_widget(self.username)

        # Legenda e Senha
        form.add_widget(Label(
            text="Senha",
            size_hint=(1, None),
            height=dp(20),
            color=(1, 1, 1, 1)
        ))
        self.password = TextInput(
            hint_text="Digite sua senha(aceita qualquer senha)",
            hint_text_color=(0.5, 0.5, 0.5, 1),
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=dp(45),
            background_normal='',
            background_active='',
            background_color=(0.98, 0.98, 0.98, 1),
            foreground_color=(0.5, 0.5, 0.5, 1),  # cinza médio para o texto
            cursor_color=(1, 1, 1, 1),
            padding=(dp(12), dp(12))
        )
        
        form.add_widget(self.password)

        # Botão Entrar
        btn_login = Button(
            text="Entrar",
            size_hint=(1, None),
            height=dp(45),
            background_normal='',
            background_color=(0.8, 0.8, 0.8, 1),
            color=(0, 0, 0, 1)
        )
        btn_login.bind(on_press=self.fazer_login)
        form.add_widget(btn_login)

        # Espaço extra antes dos botões sociais
        form.add_widget(Widget(size_hint=(1, None), height=dp(20)))

        # Botões sociais
        social = GridLayout(cols=2, spacing=dp(10), size_hint=(1, None), height=dp(45))
        for text, handler in [("Facebook", self.on_facebook_login), ("Google", self.on_google_login)]:
            b = Button(
                text=text,
                size_hint=(1, None),
                height=dp(45),
                background_normal='',
                background_color=(0.8, 0.8, 0.8, 1),
                color=(0, 0, 0, 1)
            )
            b.bind(on_press=handler)
            social.add_widget(b)
        form.add_widget(social)

        # Criar conta
        btn_create = Button(
            text="Criar Conta",
            size_hint=(1, None),
            height=dp(45),
            background_normal='',
            background_color=(0.8, 0.8, 0.8, 1),
            color=(0, 0, 0, 1)
        )
        btn_create.bind(on_press=self.ir_para_cadastro)
        form.add_widget(btn_create)

        container.add_widget(form)
        main.add_widget(container)
        self.add_widget(main)
        
    # ... métodos de login e navegação permanecem iguais ...

    def fazer_login(self, instance):
        u = self.username.text
        s = self.password.text
        if not u or not s:
            print("Preencha todos os campos.")
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
