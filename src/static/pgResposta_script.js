document.addEventListener("DOMContentLoaded", () => {
    const ckbxAlt = document.getElementById("ckbxAlterar");
    const inpNome = document.getElementById("inpNomeMidia");
    const inpArtista = document.getElementById("inpArtistaMidia");
    const respForm = document.getElementById("respForm");


    function atualizarCampos() {
        inpNome.disabled = !ckbxAlt.checked;
        inpArtista.disabled = !ckbxAlt.checked;
    };

    function desabilitarEnvio(e){
        if (ckbxAlt.checked){
            if(inpNome.value.trim().length < 3 || inpArtista.value.trim().length < 3){
                e.preventDefault();
                window.alert("Nome da musica ou artista tem que ser maior que 3!")
            };
        };
    };

    ckbxAlt.addEventListener("change", atualizarCampos);
    respForm.addEventListener("submit", desabilitarEnvio);
    atualizarCampos();
});
