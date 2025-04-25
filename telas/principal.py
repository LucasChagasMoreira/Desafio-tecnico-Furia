from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
import webbrowser


class FeedItem(BoxLayout):
    def __init__(self, title, description, link, media_src='', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(280)

        # Thumbnail
        thumbnail = AsyncImage(
            source=media_src,
            size_hint=(1, None),
            height=dp(150),
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(thumbnail)

        # Título
        title_lbl = Label(
            text=title,
            size_hint_y=None,
            height=dp(30),
            bold=True,
            color=(1, 1, 1, 1),
            halign='left',
            valign='middle'
        )
        title_lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        self.add_widget(title_lbl)

        # Descrição
        desc_lbl = Label(
            text=description,
            size_hint_y=None,
            height=dp(40),
            color=(0.7, 0.7, 0.7, 1),
            halign='left',
            valign='top'
        )
        desc_lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        self.add_widget(desc_lbl)

        # Botão de ação
        action_btn = Button(
            text='Abrir',
            size_hint=(None, None),
            size=(dp(100), dp(40))
        )
        action_btn.bind(on_release=lambda *_: webbrowser.open(link))
        self.add_widget(action_btn)


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
        foto = Image(
            source='profile.png',
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        nome = Label(
            text='Nome do Usuário',
            font_size='18sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        nome.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        foto_e_nome.add_widget(foto)
        foto_e_nome.add_widget(nome)

        # Campo de texto
        self.campo_extra = TextInput(
            hint_text='Digite aqui...',
            size_hint_y=None,
            height=dp(40),
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )

        # Botões
        boperfil = Button(text='Perfil', size_hint_y=None, height=dp(40), background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        loja = Button(text='Loja', size_hint_y=None, height=dp(40), background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        atividades = Button(text='Atividades', size_hint_y=None, height=dp(40), background_normal='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        boperfil.bind(on_release=self.ir_para_perfil)
        loja.bind(on_release=self.ir_para_loja)

        left.add_widget(foto_e_nome)
        left.add_widget(self.campo_extra)
        left.add_widget(boperfil)
        left.add_widget(loja)
        left.add_widget(atividades)

        # Painel direito: feed rolável
        scroll = ScrollView(size_hint=(0.7, 1))
        self.feed_box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10), size_hint_y=None)
        self.feed_box.bind(minimum_height=self.feed_box.setter('height'))
        scroll.add_widget(self.feed_box)

        outer.add_widget(left)
        outer.add_widget(scroll)
        self.add_widget(outer)

    def on_pre_enter(self):
        self.feed_box.clear_widgets()
        exemplos = [
            {
                'title': 'Notícia: Lançamento de Produto',
                'description': 'Conheça o novo produto que vai revolucionar o mercado.',
                'link': 'https://exemplo.com/noticia1',
                'media_src': 'https://picsum.photos/400/150?random=1'
            },
            {
                'title': 'Vídeo: Tutorial Kivy',
                'description': 'Aprenda como criar interfaces incríveis com Kivy.',
                'link': 'https://youtube.com/watch?v=dQw4w9WgXcQ',
                'media_src': 'https://picsum.photos/400/150?random=2'
            },
            {
                'title': 'Artigo: Novas Tecnologias',
                'description': 'As tendências de tecnologia para os próximos anos.',
                'link': 'https://exemplo.com/artigo',
                'media_src': 'https://picsum.photos/400/150?random=3'
            },
            {
                'title': 'Blog: Dicas de Programação',
                'description': 'Melhore seu código com estas dicas práticas.',
                'link': 'https://blog.exemplo.com/dicas',
                'media_src': 'https://picsum.photos/400/150?random=4'
            }
        ]
        for e in exemplos:
            item = FeedItem(e['title'], e['description'], e['link'], e['media_src'])
            self.feed_box.add_widget(item)

    def ir_para_perfil(self, instance):
        self.manager.current = 'perfil'

    def ir_para_loja(self, instance):
        self.manager.current = 'loja'