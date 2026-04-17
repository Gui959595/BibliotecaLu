document.getElementById("meuForm").addEventListener("submit", function(event) {

  let nome = document.getElementById("nome").value.trim();
  let autor = document.getElementById("autor").value.trim();
  let ano = document.getElementById("ano").value.trim();

  // 🔸 valida campos vazios
  if (!nome || !autor ) {
    alert("⚠️ *Nome* e *Autor* são campos obrigatórios!")
    event.preventDefault();
    return;
  }

  // 🔸 valida ano
  if (ano <=0 || ano > new Date().getFullYear()) {
    alert("⚠️ Ano inválido!");
    event.preventDefault();
    return;
  }

  // 🔸 sucesso
  alert("✅ Livro cadastrado !")


  

});