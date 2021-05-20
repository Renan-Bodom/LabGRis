from perguntas.classes.Perguntas import Pergunta

class Categoria(Pergunta):
    def __init__(self, tituloCategoria, idCategoria, objectPerguntas):
        self._tituloCategoria = tituloCategoria
        self._idCategoria = idCategoria
        self._objectPerguntas = objectPerguntas


    def get_tituloCategoria(self):
        return self._tituloCategoria

    def set_tituloCategoria(self, tituloCat):
        self._tituloCategoria = tituloCat


    '''def get_tituloPergunta(self):
        return self._tituloPergunta

    def set_tituloPergunta(self, perg):
        self._tituloPergunta = perg'''


    def get_idCategoria(self):
        return self._idCategoria

    def set_idCategoria(self, idCat):
        self._idCategoria = idCat


    def get_objectPerguntas(self):
        return self._objectPerguntas

    def set_objectPerguntas(self, perg):
        self._objectPerguntas = perg


    '''def get_alternativas(self):
        return self._alternativas

    def set_alternativas(self, alter):
        self._alternativas = alter'''


    ## Pronto para salvar no banco nomeDoCampo: DadoParaSalvar
    def enviarCategoriaFirebase(self):
        data = {"nome": self._tituloCategoria,
                "idCategoriaMae": self._idCategoria}
        return data

'''
    def updatePerguntasCategoriaFirebase(self, tituloPergunta, alternativas):
        data = {
            "tituloPerguntas/" + tituloPergunta: {
                "tituloPergunta": tituloPergunta,
                "alternativas": alternativas
            }
        }

        return data
'''