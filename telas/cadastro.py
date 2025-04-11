from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

class TelaCadastro(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = "cadastro"

        layout = BoxLayout(orientation = "vertical")

        
        self.nome = TextInput(
            hint_text="Digite seu nome aqui",
            multiline=False  # Defina como False se quiser apenas uma linha
        )
        self.cpf = TextInput(
            hint_text="Digite seu cpf aqui",
            multiline=False  # Defina como False se quiser apenas uma linha
        )
        self.endereco = TextInput(
            hint_text="Digite seu endereço aqui",
            multiline=False  # Defina como False se quiser apenas uma linha
        )

        layout.add_widget(self.nome)
        layout.add_widget(self.cpf)
        layout.add_widget(self.endereco)

        confirmar = Button(text = "Cadastrar")

        layout.add_widget(confirmar)
        confirmar.bind(on_press=self.cadastrar)
        self.add_widget(layout)

    def cadastrar(self, instance):
        if self.nome.text and self.cpf.text and self.endereco.text:
            # Salva as informações em um arquivo txt (append para adicionar novos registros)
            with open("../dados/dados.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write("Nome: {}\nCPF: {}\nEndereço: {}\n".format(
                    self.nome.text, self.cpf.text, self.endereco.text))
                arquivo.write("-" * 40 + "\n")
            print("Dados salvos com sucesso!")

            # Limpa os campos após salvar os dados
            self.nome.text = ""
            self.cpf.text = ""
            self.endereco.text = ""
        else:
            print("Por favor, preencha todos os campos.")
    
    def ir_para_inicial(self, instance):
        self.manager.current = "inicial"