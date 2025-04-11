from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from cadastro import TelaCadastro
from inicial import Telainicial

class Main(ScreenManager):
    pass

class Appli(App):
    def build(self):
        geren = Main()
        geren.add_widget(TelaCadastro())
        geren.add_widget(Telainicial())
        return geren


Appli().run()