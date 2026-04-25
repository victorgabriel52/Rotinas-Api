document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cadastroForm1');
    const senhaError = document.getElementById('senhaError1');
    form.addEventListener('submit', function(event) {
        const senha = document.querySelector('input[name="password"]').value;
        if (senha.length < 8) {
            event.preventDefault();
            senhaError.style.display = 'block';
        } else {
            senhaError.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cadastroForm2');
    const senhaError = document.getElementById('senhaError2');
    form.addEventListener('submit', function(event) {
        const senha = form.querySelector('input[name="password"]').value;
        if (senha.length < 8) {
            event.preventDefault();
            senhaError.style.display = 'block';
        } else {
            senhaError.style.display = 'none';
        }
    });
});