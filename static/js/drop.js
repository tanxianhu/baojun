window.onload = function() {
    drop();
}

function drop() {
    $('.ul_list > h2').each(function(index, obj) {
        $(obj).bind('click', function(event) {
            $('.ul_list > ul:eq(' + index + ')').stop();
            $('.ul_list > ul:eq(' + index + ')').slideToggle();
            var dr = $('.ul_list > h2:eq(' + index + ') > img:eq(0)').attr("dr");
            fangxiang = dr == null || dr == "rotate(0deg)" ? "rotate(90deg)" : "rotate(0deg)";
            $('.ul_list > h2:eq(' + index + ') > img').attr("dr", fangxiang);
            $('.ul_list > h2:eq(' + index + ') > img').css("transform", fangxiang);
        });
    });
}
