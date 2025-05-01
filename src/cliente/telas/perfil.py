from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
import json
from telas.utils import cache_search, CACHE_PATH


class TelaPerfil(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'perfil'

        # Fundo PRETO
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda i,v: setattr(self.bg_rect, 'pos', v),
                  size=lambda i,v: setattr(self.bg_rect, 'size', v))

        outer = AnchorLayout()
        root = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint=(0.8, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Top block: foto e nome
        top_block = FloatLayout(size_hint=(1, 0.22))
        with top_block.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.top_bg = RoundedRectangle(pos=top_block.pos,
                                           size=top_block.size,
                                           radius=[10])
        top_block.bind(pos=lambda i,v: setattr(self.top_bg,'pos',v),
                       size=lambda i,v: setattr(self.top_bg,'size',v))

        foto = Image(
            source='src/cliente/imagens/default profile.jpg',
            size_hint=(None, None), size=(dp(80), dp(80)),
            pos_hint={'x': 0.02, 'top': 0.95}
        )
        self.nome_label = Label(
            text='', font_size='20sp', bold=True,
            color=(1,1,1,1), halign='center', valign='middle',
            size_hint=(None,None), pos_hint={'center_x':0.5,'center_y':0.5}
        )
        self.nome_label.bind(size=lambda inst,val: setattr(inst,'text_size',inst.size))
        top_block.add_widget(foto)
        top_block.add_widget(self.nome_label)
        root.add_widget(top_block)

        # Campos de info (Link, Email, CPF, Endereço)
        for legenda, attr in [
            ('Link do Perfil','info_link'),
            ('E‑mail','info_email'),
            ('CPF','info_cpf'),
            ('Endereço','info_endereco'),
        ]:
            blk = BoxLayout(orientation='vertical', size_hint=(1,None), height=dp(70), padding=dp(8))
            with blk.canvas.before:
                Color(1,1,1,1)
                bg = RoundedRectangle(pos=blk.pos, size=blk.size, radius=[8])
            blk.bind(pos=lambda i,v,bg=bg: setattr(bg,'pos',v),
                     size=lambda i,v,bg=bg: setattr(bg,'size',v))
            lbl = Label(text=f'{legenda}:', font_size='14sp', bold=True,
                        color=(0,0,0,1), halign='left', valign='middle',
                        size_hint=(1,None), height=dp(20))
            lbl.bind(size=lambda i,v: setattr(i,'text_size',i.size))
            val = Label(text='', font_size='16sp', color=(0,0,0,1),
                        halign='left', valign='middle', size_hint=(1,None), height=dp(30))
            val.bind(size=lambda i,v: setattr(i,'text_size',i.size))
            setattr(self, attr, val)
            blk.add_widget(lbl)
            blk.add_widget(val)
            root.add_widget(blk)

        # Botões inferiores: Voltar, Verificar, Editar, Logout
        bottom = BoxLayout(size_hint=(1,0.22), spacing=dp(15))

        btn_back = Button(
            text='Voltar',
            background_normal='', background_color=(1,1,1,1), color=(0,0,0,1), font_size='16sp'
        )
        btn_back.bind(on_release=self.voltar_principal)
        bottom.add_widget(btn_back)

        btn_ver = Button(
            text='Verificar Perfil',
            background_normal='', background_color=(1,1,1,1), color=(0,0,0,1), font_size='16sp'
        )
        btn_ver.bind(on_release=self.verificar_perfil)
        bottom.add_widget(btn_ver)

        btn_edit = Button(
            text='Editar Perfil',
            background_normal='', background_color=(1,1,1,1), color=(0,0,0,1), font_size='16sp'
        )
        btn_edit.bind(on_release=self.editar_perfil)
        bottom.add_widget(btn_edit)

        btn_out = Button(
            text='Logout',
            background_normal='', background_color=(1,1,1,1), color=(0,0,0,1), font_size='16sp'
        )
        btn_out.bind(on_release=self.logout)
        bottom.add_widget(btn_out)

        root.add_widget(bottom)
        outer.add_widget(root)
        self.add_widget(outer)

    def on_pre_enter(self):
        # Carrega dados do cache
        self.nome_label.text    = cache_search('Nome') or ''
        self.info_link.text     = cache_search('Link do Perfil') or ''
        self.info_email.text    = cache_search('Email') or ''
        self.info_cpf.text      = cache_search('CPF') or ''
        self.info_endereco.text = cache_search('Endereço') or ''

    def verificar_perfil(self, instance):
        # Transição para documento
        if self.manager:
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'documento'

    def editar_perfil(self, instance):
        # Transição para edição de perfil
        if self.manager:
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'editar_perfil'

    def voltar_principal(self, instance):
        # Volta para tela principal
        if self.manager:
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'principal'

    def logout(self, instance):
        # Limpa cache e retorna ao login
        try:
            with open(CACHE_PATH,'w',encoding='utf-8') as f:
                json.dump({}, f)
        except Exception as e:
            print('Erro ao limpar cache:', e)
        if self.manager:
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'login'
