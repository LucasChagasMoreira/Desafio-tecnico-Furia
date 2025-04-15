from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
import requests

class TelaDocumento(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "documento"
        
        # Layout principal vertical
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # FileChooser nativo para selecionar o documento
        self.filechooser = FileChooserListView(
            filters=['*.pdf', '*.jpg', '*.png'],
            path="."  # Diretório inicial – ajuste conforme necessário
        )
        layout.add_widget(self.filechooser)
        
        # Label para exibir status/mensagens para o usuário
        self.status_label = Label(
            text="Selecione um documento para validar.",
            size_hint=(1, None),
            height=dp(30)
        )
        layout.add_widget(self.status_label)
        
        # Botão para submeter o documento
        self.submit_button = Button(
            text="Submeter Documento",
            size_hint=(1, None),
            height=dp(50)
        )
        self.submit_button.bind(on_press=self.submeter_documento)
        layout.add_widget(self.submit_button)
        
        # Adiciona o layout principal à Screen
        self.add_widget(layout)

    def submeter_documento(self, instance):
        # Verifica se algum arquivo foi selecionado no FileChooser
        selection = self.filechooser.selection
        if not selection:
            self.status_label.text = "Nenhum documento selecionado!"
        else:
            filepath = selection[0]
            self.status_label.text = f"Documento selecionado: {filepath}\nSubmetendo..."
            self.enviar_documento(filepath)
    
    def enviar_documento(self, filepath):
        # URL do endpoint de validação – ajuste conforme necessário
        url = "http://localhost:5000/api/validar_documento"
        try:
            with open(filepath, "rb") as file_obj:
                # Envia o arquivo para a API. A chave "documento" deve ser a mesma esperada pelo backend.
                response = requests.post(url, files={"documento": file_obj})
                
                if response.status_code == 200:
                    self.status_label.text = "Documento validado com sucesso!"
                else:
                    self.status_label.text = f"Falha na validação do documento. Código: {response.status_code}"
        except Exception as e:
            self.status_label.text = f"Erro ao enviar o documento: {e}"