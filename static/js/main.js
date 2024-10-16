//clear function
function goBackAndRefresh() {
    // window.location.href = document.referrer;
    window.addEventListener('pageshow', function (event) {
        if (event.persisted) {
            window.location.reload();
        }
    });
}
document.getElementById("clearButton").addEventListener("click", goBackAndRefresh);
