from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button

class TelaPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "principal"
        
        tela1 = BoxLayout()

        left = BoxLayout(orientation="vertical",
                         spacing=dp(10),
                         padding=dp(10),
                         size_hint=(0.3, 1))
        
        right = BoxLayout(orientation="vertical",
                          size_hint=(0.5, 1))
        right.add_widget(Label(text=""))  # ou deixe sem widgets, se preferir

        foto_e_nome = BoxLayout(orientation="horizontal",
                                size_hint_y = 0.3)
        
        
        foto = Image(source="../foto.png", 
                              allow_stretch=False, 
                              keep_ratio=True,
                              size_hint = (0.4,1 ))
        
        nome = Label(text="Nome do Usuário", font_size="15sp",
                           size_hint=(1, 0.6))

        boperfil = Button(text = "Perfil")
        boperfil.bind(on_press=self.ir_para_perfil)

        loja = Button(text = "loja")
        atividades = Button(text = "atividades")

        with left.canvas.before:
            Color(1, 0.5, 0, 1)  # cor laranja (R=1, G=0.5, B=0, A=1)
            left.rect = Rectangle(pos=left.pos, size=left.size)
        
        # Atualiza o retângulo quando a posição ou tamanho do layout mudar
        left.bind(pos=lambda instance, value: setattr(left.rect, 'pos', instance.pos),
                  size=lambda instance, value: setattr(left.rect, 'size', instance.size))

        
        foto_e_nome.add_widget(foto)
        foto_e_nome.add_widget(nome)

        # Adiciona os widgets ao container da esquerda
        left.add_widget(foto_e_nome)
        left.add_widget(boperfil)
        left.add_widget(loja)
        left.add_widget(atividades)
        
        # Adiciona os dois containers à tela principal
        tela1.add_widget(left)
        tela1.add_widget(right)

        self.add_widget(tela1)
        
    def ir_para_perfil(self,instance):
        self.manager.current = "perfil"
