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

(function() {
    var jsonData = "../strava/strava.json";
    $.getJSON(jsonData)
        .done(function(data) {
            var numberOfResults = Object.size(data.members);
            console.log(numberOfResults);
            data.members = shuffle(data.members);
            $.each(data.members, function(i, item) {
                $('<div class="col-md-3 col-sm-6 skill col-centered"><a href="' + item.strava_link + '"><img src="' + item.profile_pic + '" class="chart"><h4>' + item.first_name + ' ' + item.last_name + '</h4></a></div>').appendTo('.strava')

                if (i === numberOfResults - 1) {
                    return false;
                }
            });
        });
})();


// $(document).ready(function() {
//     $.getJSON('../lsphotos/lsphotos.json', function(data) { //Ajax call
//             console.log('loaded json')
//             var item = data.images[Math.floor(Math.random() * data.images.length)]; //select image at random
//             //build the complete <img> tag
//             $('<div class="container">').appendTo('portfolio')
//             $('<div class="section-title text-center center">').appendTo('#portfolio')
//             $('<h2>Photos</h2>').appendTo('#portfolio')
//             $('<hr>').appendTo('#portfolio')
//             $('</div>').appendTo('#portfolio')
//             $('<div class="row">').appendTo('#portfolio')
//             $('<div class="portfolio-items">').appendTo('#portfolio')
//             $('<div class="col-sm-6 col-md-3 col-lg-3 web">').appendTo('#portfolio')
//             $('<div class="portfolio-item">').appendTo('#portfolio')
//             $('<div class="hover-bg">').appendTo('#portfolio')
//             $('<a href="' + item.media_file_path + '" title="' + item.caption + '" rel="prettyPhoto">').appendTo('#portfolio')
//             $('<div class="hover-text">').appendTo('#portfolio')
//             $('<img src="' + item.media_file_path + '" class="img-responsive" alt=""> </a>').appendTo('#portfolio')
//             $('</div></div>           </div>       </div>').appendTo('#portfolio')
//                 //final divs
//             $('</div>           </div>       </div>').appendTo('#portfolio')
//
//         }
//         .error(console.log('uh oh!'))
//     );
// });
/*
var jsonData = 'lsphotos.json';
var keyArray = Object.keys(jsonData);

function shuffle(o){ //v1.0
    for(var j, x, i = o.length; i; j = parseInt(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};
keyArray = shuffle(keyArray); // shuffle it!

function showImage() {
    for (var i = 0; i < 8; ++i) {
        var current = data[keyArray[i]];
        document.write('<a href="' + current.media_file_path +
        '" title=" + jsondata.photos[random1].caption " rel="prettyPhoto"><div class="hover-text"><h4></h4><small.</small> </div><img src="' +
        current.media_file_path + '" class="img-responsive" alt="Project Title"> </a>');
    }
}
*/

/*
function showImage() {
    document.write('<a href="' + jsonData.photos[random1].media_file_path +
    '" title=" + jsondata.photos[random1].caption " rel="prettyPhoto"><div class="hover-text"><h4></h4><small.</small> </div><img src="' +
    jsonData.photos[random1].media_file_path + '" class="img-responsive" alt="Project Title"> </a>');
}
*/
// http://stackoverflow.com/questions/9991805/javascript-how-to-parse-json-array
//
//
//<div class="col-sm-6 col-md-3 col-lg-3 web">
//    <div class="portfolio-item">
//        <div class="hover-bg">
//            <a href="img/portfolio/03-large.jpg" title="Project description" rel="prettyPhoto">
//                <div class="hover-text">
//                    <h4>Project Title</h4>
//                    <small>Web Design</small> </div>
//                <img src="img/portfolio/03-small.jpg" class="img-responsive" alt="Project Title"> </a>
//        </div>
//    </div>
//</div>
