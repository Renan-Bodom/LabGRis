class Alternativa:
    def __init__(self, tituloAlternativa):
        self._tituloAlternativa = tituloAlternativa


    def get_tituloAlternativa(self):
        return self._tituloAlternativa

    def set_tituloAlternativa(self, tituloAlt):
        self._tituloAlternativa = tituloAlt


    ## Pronto para salvar no banco nomeDoCampo: DadoParaSalvar
    def enviarAlternativaFirebase(self):
        data = {"descrição": self._tituloAlternativa}
        return data