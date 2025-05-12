from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
import json
import requests
from telas.utils import show_popup, CACHE_PATH


class TelaCadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "cadastro"

        # Fundo azul escuro
        with self.canvas.before:
            Color(0.12, 0.15, 0.2, 1)
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        layout = BoxLayout(orientation="vertical", padding=[dp(20)] * 4, spacing=dp(20))

        # Cabeçalho com subtítulo
        header = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(100), spacing=dp(10))
        title = Label(
            text="Cadastro de Usuário",
            font_size="26sp",
            bold=True,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(40)
        )
        title.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        subtitle = Label(
            text="Complete com suas informações básicas",
            font_size="16sp",
            color=(0.8, 0.9, 1, 1),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(20)
        )
        subtitle.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        header.add_widget(title)
        header.add_widget(subtitle)
        layout.add_widget(header)

        # Função auxiliar para criar campo
        def criar_campo(label_text, hint_text, attr_name):
            container = BoxLayout(orientation='vertical', spacing=dp(5), size_hint=(1, None), height=dp(80))

            label = Label(
                text=label_text,
                font_size="16sp",
                color=(0.8, 0.9, 1, 1),
                size_hint=(1, None),
                height=dp(20),
                halign='left',
                valign='middle'
            )
            label.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))

            input_box = TextInput(
                hint_text=hint_text,
                hint_text_color=(0.6, 0.6, 0.6, 1),
                font_size="16sp",
                foreground_color=(1, 1, 1, 1),
                background_color=(0.22, 0.25, 0.3, 1),
                padding=[dp(10), dp(10)],
                size_hint=(1, None),
                height=dp(45),
                background_normal='',
                multiline=False
            )
            setattr(self, attr_name, input_box)

            container.add_widget(label)
            container.add_widget(input_box)

            return container

        layout.add_widget(criar_campo("Nome", "Digite seu nome", 'nome'))
        layout.add_widget(criar_campo("E-mail", "Digite seu e-mail", 'email'))
        layout.add_widget(criar_campo("Endereço", "Endereço (opcional)", 'endereco'))
        layout.add_widget(criar_campo("CPF", "Ex: 123456789-10", 'cpf'))

        # Espaço
        layout.add_widget(Widget(size_hint=(1, None), height=dp(20)))

        # Botão de Cadastrar
        btn_box = BoxLayout(size_hint=(1, None), height=dp(50), padding=[dp(40), 0, dp(40), 0])
        btn = Button(
            text="Cadastrar",
            font_size="18sp",
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),  # Azul vibrante
            color=(1, 1, 1, 1),
            size_hint=(1, 1)
        )
        btn.bind(on_press=self.cadastrar)
        btn_box.add_widget(btn)
        layout.add_widget(btn_box)

        # Rodapé informativo
        footer = Label(
            text="Já possui conta? Volte à tela de login.",
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height=dp(30),
            halign="center",
            valign="middle"
        )
        footer.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        layout.add_widget(footer)

        self.add_widget(layout)

    def _update_bg(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def cadastrar(self, instance):
        if self.nome.text and self.email.text:
            data = {
                "Nome": self.nome.text,
                "Email": self.email.text,
                "Endereco": self.endereco.text,
                "CPF": self.cpf.text
            }
            try:
                response = requests.post("http://localhost:5000/api/usuario", json=data)
                if response.status_code == 201:
                    show_popup("Dados salvos com sucesso!")
                    with open(CACHE_PATH, "w", encoding="utf-8") as f:
                        json.dump(data, f)
                    self.nome.text = self.email.text = self.endereco.text = self.cpf.text = ""
                    self.manager.current = "login"
                    return 0
                else:
                    show_popup(f"Erro: {response.status_code}")
                    return 2
            except:
                show_popup("Erro ao conectar ao servidor")
                return 3
        else:
            show_popup("Preencha todos os campos")
            return 2

    def ir_para_inicial(self, instance):
        self.manager.current = "login"
