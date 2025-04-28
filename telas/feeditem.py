
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from utils import open_url
from utils import cache_search
import requests
import threading

class FeedItem(BoxLayout):
    def __init__(self, title, description, link, image_path='', **kwargs):
        # Configura como coluna vertical
        super().__init__(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None, **kwargs)

        self.title_text = title
        self.desc_text = description
        self.link = link
        
        # Thumbnail (imagem fixa em 200dp de altura)
        thumbnail = Image(
            source=image_path,
            size_hint=(1, None),
            height=dp(200),
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(thumbnail)

        # Título (centralizado abaixo da imagem)
        title_lbl = Label(
            text=title,
            size_hint=(1, None),
            height=dp(30),
            bold=True,
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        title_lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
        self.add_widget(title_lbl)

        # Descrição (centralizada abaixo do título)
        desc_lbl = Label(
            text=description,
            size_hint=(1, None),
            height=dp(40),
            color=(0.7, 0.7, 0.7, 1),
            halign='center',
            valign='top'
        )
        desc_lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
        self.add_widget(desc_lbl)

        # Botão de ação (full width abaixo da descrição)
        action_btn = Button(
            text='Abrir',
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            background_normal='',
            background_color=(1, 1, 1, 1),
            color=(0, 0, 0, 1)
        )
        action_btn.bind(on_release=self.on_open)

        anchor = AnchorLayout(
            size_hint=(1, None),
            height=dp(40),
            anchor_x='center',
            anchor_y='center'
        )
        anchor.add_widget(action_btn)
        self.add_widget(anchor)

        # Ajusta a altura do widget para comportar todos os itens
        total_height = (
            thumbnail.height + title_lbl.height + desc_lbl.height + action_btn.height
            + self.padding[1] * 2 + self.spacing * 3
        )
        self.height = total_height

    def on_open(self, *args):
        # Executa ação de abrir URL e enviar dados via POST em thread separada
        threading.Thread(target=self._handle_open, daemon=True).start()

    def _handle_open(self):
        # Abre o link no navegador
        open_url(self.link)

        email = cache_search('Email')
        # Envia dados do item para API interna
        payload = {
            'Email': email,
            'link': self.link
        }
        try:
            response = requests.post(
                'http://localhost:5000/api/activities',
                json=payload
            )
            # Opcional: verifique status
            if response.ok:
                print('Click registrado com sucesso')
            else:
                print(f'Falha ao registrar click: {response.status_code}')
        except Exception as e:
            print(f'Erro ao enviar requisição POST: {e}')

