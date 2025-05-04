from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from telas.cadastro import TelaCadastro
from telas.inicial import TelaInicial
from telas.principal import TelaPrincipal
from telas.perfil import TelaPerfil
from telas.documentos import TelaDocumento
from telas.loja import TelaProdutos
from telas.editarperfil import TelaEditarPerfil

class Appli(App):
    def build(self):

        #Criando gerenciador de telas
        geren = ScreenManager() 

        geren.add_widget(TelaInicial())
        geren.add_widget(TelaDocumento())
        geren.add_widget(TelaPerfil())
        geren.add_widget(TelaEditarPerfil())
        geren.add_widget(TelaPrincipal())
        geren.add_widget(TelaProdutos())
        geren.add_widget(TelaCadastro())
        
        return geren


Appli().run()