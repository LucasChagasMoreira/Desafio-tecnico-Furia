from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
import json
from telas.utils import cache_search, CACHE_PATH
import requests
import threading

class TelaEditarPerfil(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'editar_perfil'

        # Fundo escuro
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda inst, val: setattr(self.bg_rect, 'pos', val),
                  size=lambda inst, val: setattr(self.bg_rect, 'size', val))

        # Formulário vertical
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        self.inputs = {}
        for label_text, key in [
            ('Nome', 'Nome'),
            ('Link do Perfil', 'Link do Perfil'),
            ('E‑mail', 'Email'),
            ('CPF', 'CPF'),
            ('Endereço', 'Endereço')
        ]:
            lbl = Label(
                text=label_text,
                size_hint_y=None,
                height=dp(20),
                color=(1, 1, 1, 1),
                halign='left'
            )
            lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
            ti = TextInput(
                multiline=False,
                size_hint_y=None,
                height=dp(40),
                background_color=(0.2, 0.2, 0.2, 1),
                foreground_color=(1, 1, 1, 1)
            )
            layout.add_widget(lbl)
            layout.add_widget(ti)
            self.inputs[key] = ti

        # Botões Salvar e Cancelar
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(15))
        btn_save = Button(
            text='Salvar',
            background_normal='', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1)
        )
        btn_save.bind(on_release=self.salvar)
        btn_cancel = Button(
            text='Cancelar',
            background_normal='', background_color=(1, 0.4, 0.4, 1), color=(1, 1, 1, 1)
        )
        btn_cancel.bind(on_release=self.cancelar)
        btn_layout.add_widget(btn_save)
        btn_layout.add_widget(btn_cancel)
        layout.add_widget(btn_layout)

        self.add_widget(layout)

    def on_pre_enter(self):
        # Carrega dados do cache ao entrar na tela
        for key, ti in self.inputs.items():
            if key == 'Link do Perfil':
                ti.text = "https://www.exemplo.com"
            else:
                try:
                    ti.text = cache_search(key) or ''
                except Exception as e:
                    print(f"Erro ao carregar '{key}' do cache: {e}")

    def salvar(self, instance):
        # 1) Grava dados no cache
        try:
            cache_data = {k: inp.text for k, inp in self.inputs.items()}
            with open(CACHE_PATH, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f)
        except Exception as e:
            print('Erro ao salvar no cache:', e)
            return

        # 2) Envia atualização à API em background
        def enviar_post():
            url = "http://localhost:5000/api/atualizar_usuario"
            try:
                resp = requests.post(url, json=cache_data, timeout=5)
                if resp.ok:
                    print("API: usuário atualizado com sucesso →", resp.json())
                else:
                    print(f"API: falhou ({resp.status_code}) →", resp.text)
            except Exception as e:
                print("API: erro na requisição →", e)

        threading.Thread(target=enviar_post, daemon=True).start()

        # 3) Volta para a tela de perfil
        if self.manager:
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'perfil'

    def cancelar(self, instance):
        # Descarta e volta para perfil
        if self.manager:
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'perfil'
