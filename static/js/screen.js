window.onload = function() {
    initPublishSearchItemEffect();
}

function initPublishSearchItemEffect(){
    var array = [];
    var dds = [];
    var dls = document.getElementsByTagName('dl');

    for (var i = 0; i < dls.length - 1; i++) {
        dds = dls[i].getElementsByTagName('dd');
        for (var j = 0; j < dds.length; j++) {
            array.push(dds[j]);
        };
    }

    for (var i = 0; i < array.length; i++) {
        array[i].onclick = function() {
            var color = this.getAttribute("color");
            var font  = this.getAttribute("font");

            color = color == null || color == "transparent" ? "#01ff00" : "transparent";
            font = font == null || font == "#666" ? "#fff" : "#666";

            this.style.backgroundColor = color;
            this.style.color = font;

            this.setAttribute("color",color);
            this.setAttribute("font",font);
        }
    }
}