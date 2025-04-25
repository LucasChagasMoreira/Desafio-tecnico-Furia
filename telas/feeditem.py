import webbrowser
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class FeedItem(BoxLayout):
    def __init__(self, title, link, media_src='', media_type='image', **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(100)
        self.spacing = dp(10)
        self.padding = dp(10)

        # mostra imagem ou thumbnail de vídeo
        if media_type == 'image':
            img = AsyncImage(source=media_src, size_hint=(None, None),
                             size=(dp(80), dp(80)))
        else:
            # use thumbnail e abra o vídeo ao clicar
            img = AsyncImage(source=media_src, size_hint=(None, None),
                             size=(dp(80), dp(80)))
        self.add_widget(img)

        # conteúdo texto + botão
        info = BoxLayout(orientation='vertical')
        lbl = Label(
            text=title,
            size_hint_y=None,
            height=dp(50),
            color=(1,1,1,1),
            halign='left',
            valign='middle'
        )
        lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
        btn = Button(
            text='Abrir',
            size_hint=(None, None),
            size=(dp(80), dp(30))
        )
        btn.bind(on_release=lambda *_: webbrowser.open(link))
        info.add_widget(lbl)
        info.add_widget(btn)

        self.add_widget(info)
