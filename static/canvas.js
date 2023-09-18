let canvas;
let context;
let isDrawing;

window.onload = function () {
    canvas = document.getElementById("canvas");
    context = canvas.getContext("2d");

    context.strokeStyle = '#FFFFFF';
    context.lineWidth = 10;
    context.lineCap = 'round';
    context.lineJoin = 'round'

    canvas.onmousedown = startDrawing;
    canvas.onmouseup = stopDrawing;
    canvas.onmousemove = draw;

    context.fillStyle = "#000000";
    context.fillRect(0, 0, canvas.width, canvas.height);

    function startDrawing(e) {
        isDrawing = true;
        context.beginPath();
        context.moveTo(e.pageX - canvas.offsetLeft, e.pageY - canvas.offsetTop);
    }

    function draw(e) {
        if (isDrawing) {
           let x = e.pageX - canvas.offsetLeft;
           let y = e.pageY - canvas.offsetTop;
        
           context.lineTo(x, y);
           context.stroke();
        }
     }

    function stopDrawing() {
        isDrawing = false;
    }

    document.getElementById("clear").addEventListener("click", function() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.fillRect(0, 0, canvas.width, canvas.height);
    });

    document.getElementById("recognize").addEventListener("click", function() {
        let image = canvas.toDataURL();
        $.ajax({
            url: '/recognize',
            type: 'POST',
            data: {"img": image},
            success: function(response) {
                console.log(response);
                document.getElementById("result").innerHTML = response;
            }
        })
    });
}

