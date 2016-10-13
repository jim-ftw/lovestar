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
    $.getScript("../js/jquery.fancybox.pack.js")
    var jsonData = "../lsphotos/lsphotos.json";
    $.getJSON(jsonData)
        .done(function(data) {
            var numberOfResults = Object.size(data.images);
            data.images = shuffle(data.images);
            $.each(data.images, function(i, item) {
                var utcSeconds = item.utc_date;
                var d = new Date(0);
                d.setUTCSeconds(utcSeconds);
                $('<div class="col-sm-6 col-md-3 col-lg-3"><div class="instagram-item"><div class="hover-bg"><a href="' + item.media_file_path + '" title="' + item.caption + '" rel="lightbox"><div class="hover-text"><h4>' + item.owner.username + '</h4><small>' + item.caption + '</small> </div><img src="' + item.media_file_path + '" class="img-responsive" alt="' + item.caption + '"> </a></div></div></div>').appendTo('.instagram-items');
                $('.instagram-item a').fancybox({
                    padding: 0,
                    helpers: {
                        title: {
                            type: 'outside'
                        },
                        overlay: {
                            locked: false,
                            closeClick: true,
                            css: {
                                'background': 'rgba(0, 0, 0, 0.7)'
                            }
                        }
                    }
                });

            });
        });
});
