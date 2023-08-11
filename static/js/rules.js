function rulesButtonOn() {
    var rulesContainer = document.querySelector('.right-rules');

    rulesContainer.style = "display:block;z-index:1000;";
    document.querySelector('.black-screen').style.display = 'block';
}

function rulesButtonOff() {
    var rulesContainer = document.querySelector('.right-rules');

    rulesContainer.style = "display:none;z-index:1000;";
    document.querySelector('.black-screen').style.display = 'none';
}
