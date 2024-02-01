document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        document.body.className = 'fade-in';
    } , 10)
});

function transitionToPage(page) {
    document.body.className = 'fade-out';
    setTimeout(() => {
        window.location.href = page;
    } , 250)
}
