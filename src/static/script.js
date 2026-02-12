document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("download-form");
    const btn = document.getElementById("download-btn");
    const loading = document.getElementById("loading");

    if (!form) return; // evita erro em outras páginas

    form.addEventListener("submit", () => {
        btn.disabled = true;
        btn.innerText = "Aguarde...";
        loading.style.display = "flex";
    });

});

