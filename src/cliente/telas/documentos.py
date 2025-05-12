from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from telas.utils import cache_search, show_popup, CACHE_PATH
import requests
import json


class TelaDocumento(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "documento"

        # Fundo azul escuro
        with self.canvas.before:
            Color(0.12, 0.15, 0.2, 1)
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Layout principal
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # Título superior
        layout.add_widget(Label(
            text="Validação de Documento",
            font_size="22sp",
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(40),
            halign="center",
            valign="middle"
        ))

        # Seletor de arquivos
        self.filechooser = FileChooserListView(
            filters=['*.pdf', '*.jpg', '*.png', '*.jpeg'],
            path=".",
            size_hint=(1, 0.75)
        )
        layout.add_widget(self.filechooser)

        # Status
        self.status_label = Label(
            text="Selecione um documento para validar.",
            size_hint=(1, None),
            height=dp(30),
            color=(0.8, 0.9, 1, 1),
            font_size="14sp"
        )
        layout.add_widget(self.status_label)

        # Container de botões
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(10)
        )

        # Botão Voltar
        self.back_button = Button(
            text="Voltar",
            size_hint=(None, 1),
            width=dp(120),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='15sp'
        )
        self.back_button.bind(on_press=self.voltar)
        button_layout.add_widget(self.back_button)

        # Botão Submeter Documento
        self.submit_button = Button(
            text="Submeter Documento",
            size_hint=(1, 1),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='15sp'
        )
        self.submit_button.bind(on_press=self.submeter_documento)
        button_layout.add_widget(self.submit_button)

        layout.add_widget(button_layout)

        # Mensagem inferior
        layout.add_widget(Label(
            text="* Arquivos aceitos: PDF, JPG, PNG",
            font_size="12sp",
            color=(0.6, 0.6, 0.6, 1),
            size_hint=(1, None),
            height=dp(20),
            halign="center",
            valign="middle"
        ))

        self.add_widget(layout)

    def _update_bg(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def on_enter(self):
        try:
            with open(CACHE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {}
        cpf = data.get('CPF', '').strip()
        endereco = data.get('Endereço', '').strip()
        if not cpf or not endereco:
            show_popup("Você não cadastrou o CPF ainda.")

    def voltar(self, instance):
        self.manager.current = 'principal'

    def submeter_documento(self, instance):
        sel = self.filechooser.selection
        if not sel:
            self.status_label.text = "Nenhum documento selecionado!"
        else:
            path = sel[0]
            self.status_label.text = f"Submetendo {path.split('/')[-1]}..."
            self.enviar_documento(path)

    def enviar_documento(self, filepath):
        url = "http://localhost:5000/api/validar_documento"
        cpf = cache_search("CPF")
        if not cpf.strip():
            show_popup("Você ainda não cadastrou seu CPF.")
            return
        try:
            with open(filepath, "rb") as f:
                resp = requests.post(
                    url,
                    files={"documento": f},
                    data={"cpf": cpf}
                )
            if resp.status_code == 200:
                self.status_label.text = "Documento validado com sucesso!"
            else:
                self.status_label.text = f"Falha na validação. Código: {resp.status_code}"
        except Exception as e:
            self.status_label.text = f"Erro ao enviar: {e}"
