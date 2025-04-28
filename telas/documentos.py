from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from utils import cache_search, show_popup
import requests

class TelaDocumento(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "documento"
        
        # Layout principal 
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Selecionar o documento
        self.filechooser = FileChooserListView(
            filters=['*.pdf', '*.jpg', '*.png'],
            path="."
        )
        layout.add_widget(self.filechooser)
        
        self.status_label = Label(
            text="Selecione um documento para validar.",
            size_hint=(1, None),
            height=dp(30)
        )
        layout.add_widget(self.status_label)
        
        # Container para botões
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(50),
            spacing=dp(10)
        )
        
        # Botão Voltar
        self.back_button = Button(
            text="Voltar",
            size_hint=(None, 1),
            width=dp(100)
        )
        self.back_button.bind(on_press=self.voltar)
        button_layout.add_widget(self.back_button)
        
        # Botão Submeter Documento
        self.submit_button = Button(
            text="Submeter Documento",
            size_hint=(1, 1)
        )
        self.submit_button.bind(on_press=self.submeter_documento)
        button_layout.add_widget(self.submit_button)
        
        layout.add_widget(button_layout)
        
        # Adiciona o layout à Screen
        self.add_widget(layout)

    def voltar(self, instance):
        # Retorna para a tela anterior ou nome especificado
        # Substitua 'tela_inicial' pelo nome correto da sua tela de origem
        self.manager.current = 'principal'

    def submeter_documento(self, instance):
        selection = self.filechooser.selection
        if not selection:
            self.status_label.text = "Nenhum documento selecionado!"
        else:
            filepath = selection[0]
            self.status_label.text = f"Documento selecionado: {filepath}\nSubmetendo..."
            self.enviar_documento(filepath)
    
    def enviar_documento(self, filepath):
        url = "http://localhost:5000/api/validar_documento"
        cpf = cache_search("CPF")
        
        if cpf == " ":
            show_popup("Você ainda não cadastrou seu CPF.")
            return

        try:
            with open(filepath, "rb") as file_obj:
                response = requests.post(
                    url,
                    files={"documento": file_obj},
                    data={"cpf": cpf}
                )
                
                if response.status_code == 200:
                    self.status_label.text = "Documento validado com sucesso!"
                else:
                    self.status_label.text = f"Falha na validação do documento. Código: {response.status_code}"
        except Exception as e:
            self.status_label.text = f"Erro ao enviar o documento: {e}"