from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from cadastro import TelaCadastro
from inicial import TelaInicial
from principal import TelaPrincipal
from perfil import TelaPerfil

class Appli(App):
    def build(self):

        #Criando gerenciador de telas
        geren = ScreenManager()

        #Adicionando todas as telas ao ScreenManager
        geren.add_widget(TelaInicial())
        geren.add_widget(TelaCadastro())
        
        geren.add_widget(TelaPerfil())
        geren.add_widget(TelaPrincipal())
        
        
        
        return geren


Appli().run()