console.log('JavaScript perguntas!');

// Botão para inserir novas perguntas
function btnNovaPergunta(){
    var novoPergunta = document.getElementById("novaPergunta");
    novoPergunta.style.display = "inline";

    var perguntaCad = document.getElementById("CRUDPergunta");
    perguntaCad.style.display = "none";
}


// Funções para cadastro de alternativas
function btnAlter(){
    //-------------------- Add input e botão para add mais
    var alter = document.getElementById("AltOuDis");
    alter.innerHTML = "<button name='btnAlternativas' type='button' onclick='AddInput()' class='btn btn-secondary btn-sm'>Mais alternativas!</button><br><br><input type='text' name='alternativas' required><br>";


    //---------------------- Add botão cadastrar
    var btnCadastrar = document.getElementById("btnCadastrar");
    btnCadastrar.innerHTML = "<button name='formPerguntas' type='submit' class='btn btn-primary'>Cadastrar</button>";
    //btnCadastrar.innerHTML = "AQUI";


    //----------------------- Altera cor do botão selecionado
    var btnAlternativas = document.getElementsByName("btnAlternativas");
    btnAlternativas.setAttribute("class", "btn btn-danger");

    //----------------------- Remove o botão duplicado
    var botaoAlteracao = document.getElementById("botaoCadastrarAlteracao");
    botaoAlteracao.style.display = "none";
}


// Funções para cadastrar como dissertativa
function btnDiss(){
    //------------- Mostra que escolheu pergunta dissertativa
    var alter = document.getElementById("AltOuDis");
    alter.innerHTML = "Pergunta definida como dissertativa";

    //-------------- Mostra o botão cadastrar
    var btnCadastrar = document.getElementById("btnCadastrar");
    btnCadastrar.innerHTML = "<button name='formPerguntasDissertativa' type='submit' class='btn btn-primary'>Cadastrar</button>";
    //btnCadastrar.innerHTML = "AQUI";

    //--------------- Moda a cor do botão selecionado
    var btnDissertativa = document.getElementsByName("btnDissertativa");
    btnDissertativa.setAttribute("class", "btn btn-danger");

    //----------------------- Remove o botão duplicado
    var botaoAlteracao = document.getElementById("botaoCadastrarAlteracao");
    botaoAlteracao.style.display = "none";
}


// Adiciona novos campos para alternativas
var CountProds = 1;
function AddInput() {
    h = CountProds;
    var form = document.getElementById("AltOuDis");
    var input = document.createElement("INPUT");
    var div = document.createElement("div");

    input.setAttribute("type", "text");
    input.setAttribute("name", "alternativas");
    var id = "alternativasInput" + h
    input.setAttribute("id", id);

    form.appendChild(input);
    document.getElementById(id).required = true;
    form.appendChild(document.createElement("br"))
    CountProds++;
}