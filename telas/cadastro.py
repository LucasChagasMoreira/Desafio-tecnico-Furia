from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from validate_docbr import CPF
from utils import show_popup
import requests

class TelaCadastro(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # atributo usado para a troca de telas
        self.name = "cadastro"

        #layout do cadastro
        layout = BoxLayout(
            orientation = "vertical",
            height=60,
            
        )

        #caixa de texto do nome
        self.nome = TextInput(
            hint_text="Digite seu nome aqui",
            size_hint=(1, None),
            height=60,
            font_size = "20dp",
            multiline=False  
        )

        #caixa de texto do cpf
        self.email = TextInput(
            hint_text="Digite seu email aqui",
            size_hint=(1, None),
            height=60,
            font_size = "20dp",
            multiline=False 
        )
        '''
        # caixa de texto do endereço
        self.endereco = TextInput(
            hint_text="Digite seu endereço aqui",
            size_hint=(1, None),
            height=60,
            font_size = "20dp",
            multiline=False
        )
'''
        #adiciona os blocos de texto ao layout
        layout.add_widget(self.nome)
        layout.add_widget(self.email)
        confirmar = Button(text = "Cadastrar")

        layout.add_widget(confirmar)
        confirmar.bind(on_press=self.cadastrar)
        self.add_widget(layout)

    def cadastrar(self, instance):
        # Verifica se todos os campos foram preenchidos
        if self.nome.text and self.email.text:

            # Preparar os dados para envio em formato JSON
            data = {
                "nome": self.nome.text,
                "email": self.email.text
            }

            # Define a URL da API; ajuste conforme a sua configuração
            url = "http://localhost:5000/api/usuario"

            try:
                # Envia a requisição POST com os dados
                response = requests.post(url, json=data)
                if response.status_code == 201:
                    show_popup("Dados salvos com sucesso!")
                    print("Dados salvos com sucesso!")
                    # Limpa os campos após o sucesso
                    self.nome.text = ""
                    self.email.text = ""
                    #retorna a aba de login
                    self.manager.current = "login"
                    return 0
                else:
                    show_popup("Erro ao salvar os dados: " + str(response.status_code))
                    print("Erro ao salvar os dados: ", response.status_code)
                    return 2
            except Exception as e:
                show_popup("Erro ao conectar com o servidor!")
                print("Erro ao conectar com o servidor: ", e)
                return 3
        else:
            show_popup("Por favor, preencha todos os campos.")
            print("Por favor, preencha todos os campos.")
            return 2
    
    #função para a trocar para tela inicial
    def ir_para_inicial(self, instance):
        self.manager.current = "login"