#### Cria lista buscando no banco firebase
def criarListaDoBanco(tabelaDoBanco):
    lista = []
    for banco in tabelaDoBanco.each():
        lista.append(banco.val())

    return lista


#### Cria lista buscando no banco firebase usando key()
def criarListaDoBancoKEY(tabelaDoBanco):
    lista = []
    for banco in tabelaDoBanco.each():
        lista.append(banco.key())

    return lista


def identificarAlternativaMarcada(listaPerguntasForm, perg, alter):
    marcadoComo = False
    for pergForm in listaPerguntasForm:
        if isinstance(pergForm.get_tituloAlternativa(), list):
            for checkBox in pergForm.get_tituloAlternativa():
                if perg.get_tituloPergunta() == pergForm.get_tituloPergunta():
                    if alter == checkBox:
                        marcadoComo = True
        else:
            if perg.get_tituloPergunta() == pergForm.get_tituloPergunta():
                if alter == pergForm.get_tituloAlternativa():
                    marcadoComo = True

    return marcadoComo