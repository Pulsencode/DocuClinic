//clear function
document.getElementById("clearButton").addEventListener("click", goBackAndRefresh);

function goBackAndRefresh() {
    window.location.href = document.referrer;
    window.addEventListener('pageshow', function (event) {
        if (event.persisted) {
            window.location.reload();
        }
    });
}
