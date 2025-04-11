from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition

class Telainicial(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = "inicial"
        layout = BoxLayout()

        nome = Label(text = "hello")
        cadastro = Button(text = "voltar para o cadastro")

        cadastro.bind(on_press=self.ir_para_cadastro)
        layout.add_widget(nome)
        layout.add_widget(cadastro)

        self.add_widget(layout)

    def ir_para_cadastro(self, instance):
        self.manager.transition = SlideTransition(direction='left', duration=0.5)
        self.manager.current = "cadastro"