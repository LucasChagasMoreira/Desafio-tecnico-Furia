from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

class TelaPerfil(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "perfil"

        # === Fundo laranja para a tela inteira ===
        with self.canvas.before:
            Color(1, 0.5, 0, 1)  # Cor laranja (R=1, G=0.5, B=0, A=1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Layout principal vertical para distribuir:
        # 1) Cabeçalho (foto + nome) - FloatLayout
        # 2) BoxLayout para info do meio
        # 3) BoxLayout para o Logout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # === TOPO: FloatLayout para posicionar foto e nome ===
        top_section = FloatLayout(size_hint=(1, 0.2))

        # Foto no canto superior esquerdo
        foto = Image(
            source='profile.png',  # caminho da sua imagem
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            pos_hint={'x': 0.02, 'top': 0.95}  # levemente afastado das bordas
        )

        # Nome centralizado no meio (horizontal e vertical)
        nome_label = Label(
            text="Nome do Usuário",
            font_size='20sp',
            halign='center',
            valign='middle',
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # centro do FloatLayout
        )
        # Ajustar text_size para centralizar internamente
        nome_label.bind(
            size=lambda instance, value: setattr(instance, 'text_size', instance.size)
        )

        top_section.add_widget(foto)
        top_section.add_widget(nome_label)

        # === SEÇÃO DO MEIO: informações de perfil ===
        middle_section = BoxLayout(orientation='vertical', size_hint=(1, 0.6), spacing=dp(10))

        info_link = Label(text="Link do Perfil", font_size='16sp', halign='center', valign='middle')
        info_email = Label(text="email cadastrado", font_size='16sp', halign='center', valign='middle')
        info_cpf = Label(text="cpf cadastrado", font_size='16sp', halign='center', valign='middle')
        info_endereco = Label(text="endereco cadastrado", font_size='16sp', halign='center', valign='middle')

        for lbl in [info_link, info_email, info_cpf, info_endereco]:
            lbl.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))

        middle_section.add_widget(info_link)
        middle_section.add_widget(info_email)
        middle_section.add_widget(info_cpf)
        middle_section.add_widget(info_endereco)

        # === BASE: botão Logout ===
        bottom_section = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), padding=dp(10))
        btn_logout = Button(text="Logout", size_hint=(1, None), height=dp(45))
        bottom_section.add_widget(btn_logout)

        # Adiciona tudo ao layout principal
        main_layout.add_widget(top_section)
        main_layout.add_widget(middle_section)
        main_layout.add_widget(bottom_section)

        # Adiciona o layout principal à tela
        self.add_widget(main_layout)

    def _update_bg(self, instance, value):
        """Mantém o retângulo de fundo do tamanho da tela."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size



