const video = document.getElementById('camera');
const canvas = document.getElementById('foto');
const imagem = document.getElementById('imagem');
const capturarBotao = document.getElementById('capturar');
const mensagemElement = document.getElementById('mensagem');
const imagemForm = document.getElementById('imagemForm');

// Acessar a câmera
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            video.srcObject = stream;
        })
        .catch(function(error) {
            console.error('Erro ao acessar a câmera: ', error);
        });
}

// Capturar uma foto
capturarBotao.addEventListener('click', function() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
    
    // Converter a imagem para um objeto Blob
    canvas.toBlob(function(blob) {
        const formData = new FormData();
        formData.append('imagem', blob, 'imagem.png');
        formData.append('matricula', document.getElementById('matricula').value);

        // Enviar a imagem e a matrícula para o servidor
        fetch('/salvarimg', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            mensagemElement.textContent = data.mensagem;
            mensagemElement.style.display = 'block';
        })
        .catch(error => {
            mensagemElement.textContent = 'Erro ao enviar a imagem: ' + error;
            mensagemElement.style.display = 'block';
        });
    }, 'image/png');
});