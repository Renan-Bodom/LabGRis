from categorias.classes.Categorias import Categoria

class Ficha:
    def __init__(self, tituloFicha, idUsuario, objectCategorias):
        self._idUsuario = idUsuario
        self._tituloFicha = tituloFicha
        self._objectCategorias = objectCategorias

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

    ## Pronto para salvar no banco nomeDoCampo: DadoParaSalvar
    def enviarFichaFirebase(self):
        data = {#"equipe": self._tituloFicha,
                "keyFicha": self._tituloFicha,
                "tituloFicha": self._tituloFicha,
                "idUsuario": self._idUsuario}
        return data

    def updateFichaCategoriaFirebase(self, tituloCategoria, idCategoria, cont):
        data = {
            "categorias/" + str(cont) + "/": {
                "tituloCategoria": tituloCategoria
                #"idCategoria": idCategoria
            }
        }
        return data