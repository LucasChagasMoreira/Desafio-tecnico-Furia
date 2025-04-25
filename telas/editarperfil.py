from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
import json
from utils import cache_search

class TelaEditarPerfil(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'editar_perfil'

        # Fundo cinza claro
        with self.canvas.before:
            Color(0.95,0.95,0.95,1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda i,v: setattr(self.bg_rect,'pos',v), size=lambda i,v: setattr(self.bg_rect,'size',v))

        # Formulário vertical
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        self.inputs = {}
        for label_text, key in [
            ('Nome','Nome'),('Link do Perfil','Link do Perfil'),
            ('E‑mail','Email'),('CPF','CPF'),('Endereço','Endereço')
        ]:
            lbl = Label(text=label_text, size_hint_y=None, height=dp(20), color=(0,0,0,1), halign='left')
            lbl.bind(size=lambda i,v: setattr(i,'text_size',i.size))
            ti = TextInput(
                text=cache_search(key) or '', multiline=False,
                size_hint_y=None, height=dp(40),
                background_color=(1,1,1,1), foreground_color=(0,0,0,1)
            )
            layout.add_widget(lbl)
            layout.add_widget(ti)
            self.inputs[key] = ti

        # Botões Salvar e Cancelar
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(15))
        btn_save = Button(
            text='Salvar',
            background_normal='', background_color=(0.2,0.6,1,1), color=(1,1,1,1)
        )
        btn_save.bind(on_release=self.salvar)
        btn_cancel = Button(
            text='Cancelar',
            background_normal='', background_color=(1,0.4,0.4,1), color=(1,1,1,1)
        )
        btn_cancel.bind(on_release=self.cancelar)
        btn_layout.add_widget(btn_save)
        btn_layout.add_widget(btn_cancel)
        layout.add_widget(btn_layout)

        self.add_widget(layout)

    def salvar(self, instance):
        # Grava dados no cache
        try:
            with open("../cache/cache.json",'w',encoding='utf-8') as f:
                cache = {k: inp.text for k, inp in self.inputs.items()}
                json.dump(cache, f)
        except Exception as e:
            print('Erro ao salvar:', e)
        # Volta para perfil
        if self.manager:
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'perfil'

    def cancelar(self, instance):
        # Descarta e volta para perfil
        if self.manager:
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'perfil'