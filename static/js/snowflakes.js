function snowFlakes(){
    // Судя по стилю кода - писал его другой разработчик, лет так 10 назад. Код просто скопировали. Имеет место быть. Устаревшие литералы, объявление переменных через var.
    var canvas = document.getElementById("index-sale-banner-canvas");
    var parent = canvas.parentNode;
    var screenw = parent.getBoundingClientRect().width;
    var screenh = 150;

    var ctx = canvas.getContext("2d");

    var flakesn = 50;
    var flakes = new Array();

    for (var i = 0; i < flakesn; i++) {
        flakes.push({
            x: Math.random() * screenw,
            y: Math.random() * screenh,
            r: Math.random() * 3 + 1,
            d: Math.random() * flakesn,
        });
    }

    function drawFlake() {
        ctx.clearRect(0, 0, screenw, screenh);
        ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
        ctx.beginPath();

        for (var i = 0; i < flakesn; i++) {
            var f = flakes[i];
            ctx.moveTo(f.x, f.y);
            ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2, true);
        }

        ctx.fill();
        reload();
    }

    var angle = 0;

    function reload() {
        angle += 0.01;

        for (var i = 0; i < flakesn; i++) {
            var f = flakes[i];
            f.x += Math.sin(angle) * 2;
            f.y += Math.cos(angle + f.d) + 1 + f.r / 25;

            if (f.x > screenw + 5 || f.x < -5 || f.y > screenh) {
                if (i % 5 > 0) {
                    flakes[i] = {
                        x: Math.random() * screenw,
                        y: -10,
                        r: f.r,
                        d: f.d,
                    };
                } else {
                    if (Math.sin(angle) > 0) {
                        flakes[i] = {
                            x: -5,
                            y: Math.random() * screenh,
                            r: f.r,
                            d: f.d,
                        };
                    } else {
                        flakes[i] = {
                            x: screenw + 5,
                            y: Math.random() * screenh,
                            r: f.r,
                            d: f.d,
                        };
                    }
                }
            }
        }
    }
    setInterval(drawFlake, 35);
}

document.addEventListener("DOMContentLoaded", function () {
    setTimeout(snowFlakes, 1000);
});
