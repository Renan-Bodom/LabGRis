from .Alternativas import Alternativa


class Pergunta(Alternativa):
    def __init__(self, tituloPergunta, alternativa):
        self._tituloPergunta = tituloPergunta
        Alternativa.__init__(self, alternativa)

    def get_tituloPergunta(self):
        return self._tituloPergunta

    def set_tituloPergunta(self, tituloPerg):
        self._tituloPergunta = tituloPerg

    '''    def get_alternativa(self):
            return self._alternativa

        def set_alternativa(self, perg):
            self._alternativa = perg'''

    ## Pronto para salvar no banco nomeDoCampo: DadoParaSalvar
    def enviarPerguntaFirebase(self, alternativa):
        objectAlternativa = Alternativa(alternativa)
        data = {"enunciado": self._tituloPergunta,
                # "alternativas": self._alternativa}
                "alternativas": objectAlternativa.get_tituloAlternativa()}
        return data

    ## Salva como dissertativa
    def enviarPerguntaDissertativaFirebase(self):
        data = {"enunciado": self._tituloPergunta,
                "alternativas": "dissertativa"}
        return data