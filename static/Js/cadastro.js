const form = document.querySelector('form');
const mensagemElement = document.getElementById("mensagem");

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const formData = new FormData(form);

    const response = await fetch('/salvar', {
        method: 'POST',
        body: formData
    });

    if (response.status === 200) {
        const data = await response.json();
        mensagemElement.textContent = data.mensagem;
        mensagemElement.style.display = "block";
    }
});

function excluirCadastro(button) {
const matricula = button.parentElement.querySelector('.matricula').value;

    if (confirm(`Tem certeza que deseja excluir o cadastro com matrícula ${matricula}?`)) {
        // Você pode enviar a matrícula para o Flask aqui
        excluirCadastroNoFlask(matricula);
    }
}

async function excluirCadastroNoFlask(matricula) {
    const response = await fetch(`/excluir/${matricula}`, {
        method: 'DELETE',
    });

    if (response.status === 200) {
        const data = await response.json();
        mensagemElement.textContent = data.mensagem;
        mensagemElement.style.display = "block";
    }
}