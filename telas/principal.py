from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from telas.utils import cache_search
from telas.feeditem import FeedItem


class TelaPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'principal'

        # Fundo preto
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda i, v: setattr(self.bg_rect, 'pos', v),
                  size=lambda i, v: setattr(self.bg_rect, 'size', v))

        outer = BoxLayout(orientation='horizontal')

        # Painel esquerdo
        left = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20),
            size_hint=(0.3, 1)
        )
        with left.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.left_bg = RoundedRectangle(pos=left.pos, size=left.size, radius=[8])
        left.bind(pos=lambda i, v: setattr(self.left_bg, 'pos', v),
                  size=lambda i, v: setattr(self.left_bg, 'size', v))

        # Foto e nome
        foto_e_nome = BoxLayout(orientation='vertical', size_hint_y=0.3)
        self.foto = Image(
            source='imagens/default profile.jpg',
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        self.nome = Label(
            text='Nome do Usuário',
            font_size='18sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.nome.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        foto_e_nome.add_widget(self.foto)
        foto_e_nome.add_widget(self.nome)


        # Botões
        boperfil = Button(text='Perfil', size_hint_y=None, height=dp(40), background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        loja = Button(text='Loja', size_hint_y=None, height=dp(40), background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        config = Button(text='Configurações', size_hint_y=None, height=dp(40), background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        boperfil.bind(on_release=self.ir_para_perfil)
        loja.bind(on_release=self.ir_para_loja)

        left.add_widget(foto_e_nome)
        left.add_widget(boperfil)
        left.add_widget(loja)
        left.add_widget(config)

        # Painel direito: feed rolável
        scroll = ScrollView(size_hint=(0.7, 1))
        self.feed_box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10), size_hint_y=None)
        self.feed_box.bind(minimum_height=self.feed_box.setter('height'))
        scroll.add_widget(self.feed_box)

        outer.add_widget(left)
        outer.add_widget(scroll)
        self.add_widget(outer)

    def on_pre_enter(self):
        self.nome.text = cache_search("Nome") or ' '
        self.feed_box.clear_widgets()
        exemplos = [
            {
                'title': 'LTA Sul: “Eles precisam de mais experiência no palco”, comenta Thinkcard, técnico da FURIA',
                'description': 'Confira como foi a coletiva de imprensa com a comissão técnica dos panteras',
                'link': 'https://www.pichauarena.com.br/lol/thinkcard-tecnico-da-furia/',
                'image_path': 'imagens/imagem1.webp'
            },
            {
                'title': 'FalleN analisa nova FURIA e fala sobre troca de função: "Ainda posso atuar em alto nível',
                'description': 'Brasileiro comenta sobre chegada de novos jogadores, mudança da equipe e mais; confira',
                'link': 'https://draft5.gg/noticia/fallen-analisa-nova-furia-e-fala-sobre-troca-de-funcao-ainda-posso-atuar-em-alto-nivel',
                'image_path': 'imagens/fallen.jpg'
            },
            {
                'title': 'Team Liquid se classifica com folga para os playoffs da CFBL 2025',
                'description': 'Cavalaria lidera a fase de grupos com 10 vitórias e 18 de saldo',
                'link': 'https://www.gamersegames.com.br/2025/04/10/team-liquid-se-classifica-com-folga-para-os-playoffs-da-cfbl-2025/',
                'image_path': 'imagens/liquid.webp'
            },
            {
                'title': 'AO VIVO: RED x FXW7 & FUR x LOUD | LTA SUL FASE DE GRUPOS DIA 2 | ILHA DAS LENDAS',
                'description': '🏆 Dia 2 da fase de grupos da Lta sul, confrontos parelhos, Loud embalada 🏆',
                'link': 'https://youtu.be/ZAXN5x8t21U',
                'image_path': 'imagens/lol.png'
            }

        ]
        for e in exemplos:
            item = FeedItem(e['title'], e['description'], e['link'], e['image_path'])
            self.feed_box.add_widget(item)

    def ir_para_perfil(self, instance):
        self.manager.current = 'perfil'

    def ir_para_loja(self, instance):
        self.manager.current = 'loja'