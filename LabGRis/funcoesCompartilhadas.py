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