from .Alternativas import Alternativa


class Pergunta(Alternativa):
    def __init__(self, tituloPergunta, alternativa, multiplasRespostas = False):
        self._tituloPergunta = tituloPergunta
        Alternativa.__init__(self, alternativa)
        self._multiplasRespostas = multiplasRespostas

    def get_tituloPergunta(self):
        return self._tituloPergunta

    def set_tituloPergunta(self, tituloPerg):
        self._tituloPergunta = tituloPerg

    def get_multiplasRespostas(self):
        return self._multiplasRespostas

    def set_multiplasRespostas(self, multplaResposta):
        self._multiplasRespostas = multplaResposta

    '''    def get_alternativa(self):
            return self._alternativa

        def set_alternativa(self, perg):
            self._alternativa = perg'''


#---------------------- Cadastrado de perguntas ------------------
    ## Pronto para salvar no banco nomeDoCampo: DadoParaSalvar
    def enviarPerguntaFirebase(self, alternativa):
        objectAlternativa = Alternativa(alternativa)
        data = {"tituloPergunta": self._tituloPergunta,
                "fechada": True,
                "multiplasRespostas": False,
                # "alternativas": self._alternativa}
                "alternativas": objectAlternativa.get_tituloAlternativa()}
        return data


    def enviarPerguntaMultiplasRespostasFirebase(self, alternativa):
        objectAlternativa = Alternativa(alternativa)
        data = {"tituloPergunta": self._tituloPergunta,
                "fechada": True,
                "multiplasRespostas": True,
                # "alternativas": self._alternativa}
                "alternativas": objectAlternativa.get_tituloAlternativa()}
        return data


    ## Salva como dissertativa
    def enviarPerguntaDissertativaFirebase(self):
        data = {"tituloPergunta": self._tituloPergunta,
                "fechada": False,
                "multiplasRespostas": False}
        return data


#----------------------------- Padrão para responder fichas --------------

    ## Pronto para salvar no banco nomeDoCampo: DadoParaSalvar
    def enviarModeloPerguntaFirebase(self, alternativa):
        objectAlternativa = Alternativa(alternativa)
        data = {"tituloPergunta": self._tituloPergunta,
                "fechada": True,
                "multiplasRespostas": False}
        cont = 0
        for alt in objectAlternativa.get_tituloAlternativa():
            data['alternativas/' + str(cont) + '/tituloAlternativa/'] = alt
            data['alternativas/' + str(cont) + '/resposta/'] = False
            cont = cont + 1
        return data


    def enviarModeloPerguntaMultiplasRespostasFirebase(self, alternativa):
        objectAlternativa = Alternativa(alternativa)
        data = {"tituloPergunta": self._tituloPergunta,
                "fechada": True,
                "multiplasRespostas": True}
        cont = 0
        for alt in objectAlternativa.get_tituloAlternativa():
            data['alternativas/' + str(cont) + '/tituloAlternativa/'] = alt
            data['alternativas/' + str(cont) + '/resposta/'] = False
            cont = cont + 1
        return data


    ## Salva como dissertativa
    def enviarModeloPerguntaDissertativaFirebase(self):
        data = {"tituloPergunta": self._tituloPergunta,
                "fechada": False,
                "multiplasRespostas": False,
                "resposta": ""}
        return data
