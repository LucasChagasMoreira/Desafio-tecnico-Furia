from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
import json
import requests
from telas.utils import show_popup, CACHE_PATH

class TelaCadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "cadastro"

        # Fundo cinza
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Layout principal
        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(20)] * 4,
            spacing=dp(20)
        )

        # Título centralizado
        titulo = Label(
            text="Cadastro",
            font_size="32sp",
            size_hint=(1, None),
            height=dp(60),
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1)
        )
        titulo.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        layout.add_widget(titulo)

        # Função auxiliar para criar campo centralizado com label alinhado à esquerda
        def criar_campo(label_text, hint_text, attr_name):
            container_width = dp(380)
            input_width = dp(300)
            padding_left = (container_width - input_width) / 2

            # Container vertical
            container = BoxLayout(
                orientation='vertical',
                size_hint=(None, None),
                size=(container_width, dp(80)),
                spacing=dp(5)
            )
            # Label alinhado à esquerda do input via padding
            label_row = BoxLayout(
                size_hint=(1, None),
                height=dp(20),
                padding=[padding_left, 0, 0, 0]
            )
            lbl = Label(
                text=label_text,
                size_hint=(None, None),
                size=(input_width, dp(20)),
                font_size='18sp',
                halign='left',
                valign='middle',
                color=(1, 1, 1, 1)
            )
            lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
            label_row.add_widget(lbl)
            container.add_widget(label_row)

            # Row para input com padding igual
            row = BoxLayout(
                size_hint=(1, None),
                height=dp(50),
                padding=[padding_left, 0, 0, 0]
            )
            ti = TextInput(
                hint_text=hint_text,
                size_hint=(None, None),
                size=(input_width, dp(50)),
                font_size='20sp',
                multiline=False,
                background_color=(1, 1, 1, 1),
                foreground_color=(0, 0, 0, 1)
            )
            setattr(self, attr_name, ti)
            row.add_widget(ti)
            container.add_widget(row)

            # Centralizar horizontalmente
            wrapper = AnchorLayout(
                size_hint=(1, None),
                height=dp(80),
                anchor_x='center',
                anchor_y='center'
            )
            wrapper.add_widget(container)
            return wrapper

        # Campos de input
        layout.add_widget(criar_campo("Nome:", "Digite seu nome", 'nome'))
        layout.add_widget(criar_campo("Email:", "Digite seu email", 'email'))
        layout.add_widget(criar_campo("Endereço:", "Endereço (opcional)", 'endereco'))
        layout.add_widget(criar_campo("CPF:", "(ex: 123456789-10) (opcional)", 'cpf'))

        # Espaço antes do botão
        layout.add_widget(Widget(size_hint=(1, None), height=dp(40)))

        # Botão Cadastrar centralizado
        btn_row = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50)
        )
        btn_row.add_widget(Widget(size_hint_x=1))
        confirmar = Button(
            text="Cadastrar",
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            font_size="20sp",
            background_normal='',
            background_color=(1, 1, 1, 1),
            color=(0, 0, 0, 1)
        )
        confirmar.bind(on_press=self.cadastrar)
        btn_row.add_widget(confirmar)
        btn_row.add_widget(Widget(size_hint_x=1))
        layout.add_widget(btn_row)

        self.add_widget(layout)

    def _update_bg(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def cadastrar(self, instance):
        if self.nome.text and self.email.text:
            data = {"Nome": self.nome.text, "Email": self.email.text,
                    "Endereco": self.endereco.text, "CPF": self.cpf.text}
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
