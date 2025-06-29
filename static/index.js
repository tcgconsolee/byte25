const die = document.getElementsByClassName("rolldie")[0]
const anime = document.getElementsByClassName("dieanimation")[0]
document.querySelector('.rolldie > img').addEventListener('click', () => {
    document.querySelector('.rolldie > img').style.display = "none"
    die.style.animation = "shrink 500ms forwards"
    setTimeout(() => {
        anime.style.animation = "rolldie 1s none"
    }, 500);
    setTimeout(() => {
        die.style.animation = "largen 500ms forwards"
        setTimeout(() => {
            anime.style.animation = "none"
            document.querySelector('.rolldie > img').style.display = "block"
            fetch('/list-images')
                .then(response => response.json())
                .then(images => {
                    let r1 = Math.floor(Math.random() * images.length);
                    let r2 = Math.floor(Math.random() * images.length);
                    while (r1 === r2) {
                        r2 = Math.floor(Math.random() * images.length);
                    } 
                    let img1 = document.createElement("img");
                    img1.src = "/static/" + images[r1];
                    let img2 = document.createElement("img");
                    img2.src = "/static/" + images[r2];
                    const rollDivs = document.getElementsByClassName('rollimg');
                    rollDivs[0].innerHTML = '';
                    rollDivs[1].innerHTML = '';
                    rollDivs[0].appendChild(img1);
                    rollDivs[1].appendChild(img2);
                })
        }, 500);
    }, 2000);
})