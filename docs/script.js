var form = document.getElementById("form");
const results = document.getElementById("results");

function submit() {
    results.style.display = "initial";

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        results.innerHTML = this.responseText;
    }

    xhttp.open("POST", "http://adsheu.pythonanywhere.com/get-data");
    xhttp.send(new FormData(form));
    console.log("sent");
}

form.addEventListener('submit', function(e) {
    e.preventDefault();
    submit();
});