document.querySelector('.leafcard').addEventListener('click', function() {
    const card = this.querySelector('.card');
    if (card.style.transform === "rotateY(180deg)") {
        card.style.transform = "rotateY(0deg)";
    } else {
        card.style.transform = "rotateY(180deg)";
    }
});
