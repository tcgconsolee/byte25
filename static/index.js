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
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "../static/library", true);
            xhr.responseType = 'document';
            let imgs = [];
            xhr.onload = () => {
            if (xhr.status === 200) {
                var elements = xhr.response.getElementsByTagName("a");
                for (x of elements) {
                    if ( x.href.match(/\.(jpe?g|png|gif)$/) ) { 
                        let img = document.createElement("img");
                        img.src = x.href;
                        imgs.push(img)
                    } 
                };
                let r1 = Math.floor(Math.random()*imgs.length-0.1)
                let r2 = Math.floor(Math.random()*imgs.length-0.1)
                while (r1==r2) {
                    r2 = Math.floor(Math.random()*(imgs.length-1))
                }
                let img1 = imgs[r1];
                let img2 = imgs[r2];
                document.getElementsByClassName('rollimg')[0].innerHTML='';
                document.getElementsByClassName('rollimg')[1].innerHTML='';  
                document.getElementsByClassName('rollimg')[0].append(img1);
                document.getElementsByClassName('rollimg')[1].append(img2);
            } 
            else {
                alert('Request failed. Returned status of ' + xhr.status);
            }
            }
            xhr.send()
        }, 500);
    }, 2000);
})