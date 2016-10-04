// courtesy of http://stackoverflow.com/a/6274381/648350
function shuffle(o) { //v1.0
    for (var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};
// courtesy of http://stackoverflow.com/a/6700/648350
Object.size = function(obj) {
    var size = 0,
        key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

$(document).ready(function() {
    var jsonData = "../lsphotos/lsphotos.json";
    $.getJSON(jsonData)
        .done(function(data) {
            var numberOfResults = Object.size(data.images);
            console.log(numberOfResults);
            data.images = shuffle(data.images);
            $.each(data.images, function(i, item) {
                $('<div class="col-sm-6 col-md-3 col-lg-3 web"><div class="instagram-item"><div class="hover-bg"><a href="' + item.instagram_url + '" title="' + item.caption + '" rel="prettyPhoto"><div class="hover-text"><h4></h4><small>' + item.caption + '</small> </div><img src="' + item.media_file_path + '" class="img-responsive" alt=""> </a></div></div></div>').appendTo('.instagram-items')
                console.log($('.instagram-item').position());
                if (i === 7) {
                    return false;
                }
            });
        });
});
