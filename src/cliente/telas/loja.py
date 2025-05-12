from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
import json
from telas.utils import CACHE_PATH

class TelaProdutos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "loja"

        # Fundo azul escuro
        with self.canvas.before:
            Color(0.12, 0.15, 0.2, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Layout principal vertical
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # Título
        titulo = Label(
            text="Produtos disponíveis",
            font_size="22sp",
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(40),
            halign='center',
            valign='middle'
        )
        titulo.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        main_layout.add_widget(titulo)

        # Lista de produtos com scroll
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )
        grid.bind(minimum_height=grid.setter('height'))

        produtos = [
            {"image": "src/cliente/imagens/blusa.webp",   "name": "Blusa Esports",   "price": "R$ 199,90"},
            {"image": "src/cliente/imagens/calça1.webp",  "name": "Calça Cargo",     "price": "R$ 249,90"},
            {"image": "src/cliente/imagens/calça2.webp",  "name": "Calça Esportiva", "price": "R$ 149,90"},
            {"image": "src/cliente/imagens/camisa1.webp", "name": "Camisa Verde",    "price": "R$ 129,90"},
            {"image": "src/cliente/imagens/camisa2.webp", "name": "Camisa Azul",     "price": "R$ 119,90"},
            {"image": "src/cliente/imagens/camisa3.webp", "name": "Camisa Branca",   "price": "R$ 99,90"},
        ]
        for prod in produtos:
            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(220),
                padding=dp(5),
                spacing=dp(5)
            )
            # Fundo do cartão
            with card.canvas.before:
                Color(0.22, 0.25, 0.3, 1)
                card.bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
            card.bind(pos=lambda i, v: setattr(card.bg, 'pos', v),
                      size=lambda i, v: setattr(card.bg, 'size', v))

            img = Image(
                source=prod["image"],
                size_hint=(1, None),
                height=dp(140),
                allow_stretch=True,
                keep_ratio=True
            )
            card.add_widget(img)

            lbl = Label(
                text=f"{prod['name']}\n{prod['price']}",
                size_hint=(1, None),
                height=dp(60),
                color=(1, 1, 1, 1),
                font_size='14sp',
                halign='center',
                valign='middle'
            )
            lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
            card.add_widget(lbl)

            grid.add_widget(card)

        scroll.add_widget(grid)
        main_layout.add_widget(scroll)

        # Botão Voltar
        btn_container = BoxLayout(size_hint_y=None, height=dp(60), padding=dp(10))
        back_btn = Button(
            text='Voltar',
            size_hint=(1, None),
            height=dp(40),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='15sp'
        )
        back_btn.bind(on_release=self.go_back)
        btn_container.add_widget(back_btn)
        main_layout.add_widget(btn_container)

        self.add_widget(main_layout)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def go_back(self, *args):
        if self.manager:
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'principal'

    def on_enter(self):
        try:
            with open(CACHE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = {}
        cpf = data.get('CPF', '').strip()
        endereco = data.get('Endereço', '').strip()
        if not cpf or not endereco:
            self.show_popup()

    def show_popup(self):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        msg = Label(
            text='Por favor, adicione CPF e Endereço em "Editar perfil" na aba de "Perfil"',
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1)
        )
        msg.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        content.add_widget(msg)

        btn_ok = Button(
            text='OK',
            size_hint=(1, None),
            height=dp(40),
            background_normal='',
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        content.add_widget(btn_ok)

        popup = Popup(
            title='Cadastro Incompleto',
            content=content,
            size_hint=(0.8, 0.4),
            background_color=(0.15, 0.15, 0.2, 1),
            title_color=(1, 1, 1, 1)
        )
        btn_ok.bind(on_release=lambda *args: self._on_popup_ok(popup))
        popup.open()

    def _on_popup_ok(self, popup):
        popup.dismiss()
        if self.manager:
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'principal'
