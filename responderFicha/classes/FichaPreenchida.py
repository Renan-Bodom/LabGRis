from categorias.classes.Categorias import Categoria
import datetime

class FichaPreenchida:
    def __init__(self, tituloFicha, idUsuario, objectCategorias, modeloFicha):
        self._idUsuario = idUsuario
        self._tituloFicha = tituloFicha
        self._objectCategorias = objectCategorias
        self._modeloFicha = modeloFicha

    def get_idUsuario(self):
        return self._idUsuario

    def set_idUsuario(self, equip):
        self._idUsuario = equip


    def get_tituloFicha(self):
        return self._tituloFicha

    def set_tituloFicha(self, tituloFic):
        self._tituloFicha = tituloFic


    def get_objectCategorias(self):
        return self._objectCategorias

    def set_objectCategorias(self, categ):
        self._objectCategorias = categ


    def get_modeloFicha(self):
        return self._modeloFicha

    def set_modeloFicha(self, modelo):
        self._modeloFicha = modelo


    ## Pronto para salvar no banco nomeDoCampo: DadoParaSalvar
    def enviarFichaFirebase(self):
        data = {#"equipe": self._tituloFicha,
                "keyFicha": self._tituloFicha,
                "tituloFicha": self._tituloFicha,
                "idUsuario": "Renan",
                "modeloFicha": self._modeloFicha,
                "data": datetime.datetime.now().strftime("%d/%m/%Y")
        }
        return data

    def updateFichaCategoriaFirebase(self, tituloCategoria, idCategoria, cont):
        data = {
            "categorias/" + str(cont) + "/": {
                "tituloCategoria": tituloCategoria
                #"idCategoria": idCategoria
            }
        }

        return data

    def updateFichaPerguntasFirebase(self, pergunta, alternativas, cont):

        data = {
            "perguntas/" + str(cont) + "/": {
                "tituloPergunta": pergunta
                #"alternativas": alternativas
            }
        }

        return data

    def updateFichaAlternativasFirebase(self, alternativa, cont, marcadoComo):

        data = {
            "alternativas/" + str(cont) + "/": {
                "tituloAlternativa": alternativa,
                "resposta": marcadoComo
            }
        }

        return data


    def updateFichaAlternativasDissertativaFirebase(self, respostaDissertativa, cont):

        data = {
            "resposta": respostaDissertativa
        }

        return data