import re
import json
import os.path
import logging
import sys
from operator import itemgetter
import re
import sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')


def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id


def decode_unicode_references(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data)


# logger = logging.getLogger()
# handler = logging.StreamHandler(sys.stdout)
# formatter = logging.Formatter('%(levelname)-8s %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)
# logging.getLogger("requests").setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)


lsphotos_json = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lsphotos', 'lsphotos.json'))
media_file_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lsphotos'))
instagram_page_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instagram'))


ig_index_head = '''<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Lovestar Bicycle Bags: Custom handmade cycling gear</title>
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Favicons
    ================================================== -->
    <link rel="shortcut icon" href="../img/favicon.ico" type="image/x-icon">
    <link rel="apple-touch-icon" href="../img/apple-touch-icon.png">
    <link rel="apple-touch-icon" sizes="72x72" href="../img/apple-touch-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="114x114" href="../img/apple-touch-icon-114x114.png">

    <!-- Bootstrap -->
    <link rel="stylesheet" type="text/css" href="../css/bootstrap.css">
    <link rel="stylesheet" type="text/css" href="../fonts/font-awesome/css/font-awesome.css">

    <!-- Stylesheet
    ================================================== -->
    <link rel="stylesheet" type="text/css" href="../css/jquery.fancybox.css">
    <link rel="stylesheet" type="text/css" href="../css/style.css">
    <link href="http://fonts.googleapis.com/css?family=Lato:400,700,900,300" rel="stylesheet" type="text/css">
    <link href="http://fonts.googleapis.com/css?family=Open+Sans:400,700,800,600,300" rel="stylesheet" type="text/css">
    <script type="text/javascript" src="../js/jquery.1.11.1.js"></script>
    <script type="text/javascript" src="../js/jquery.fancybox.js"></script>
    <!--    <script type="text/javascript" src="js/lsphotos_all.min.js"></script> -->


    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>

<body id="page-top" data-spy="scroll" data-target=".navbar-fixed-top">

    <!-- Navigation -->
    <div id="nav">
        <nav class="navbar navbar-custom">
            <div class="container">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-main-collapse"> <i class="fa fa-bars"></i> </button>
                    <a class="navbar-brand page-scroll" href="#page-top">Lovestar Instagram</a> </div>

                <!-- Collect the nav links, forms, and other content for toggling -->
                <div class="collapse navbar-collapse navbar-right navbar-main-collapse">
                    <ul class="nav navbar-nav">
                        <!-- Hidden li included to remove active class from about link when scrolled up past about section -->
                        <li class="hidden">
                            <a href="#page-top"></a>
                        </li>
                        <!-- <li> <a class="page-scroll" href="#about">About</a> </li> -->
                        <li> <a class="page-scroll" href="../">Home</a> </li>
                        <li> <a class="page-scroll" href="#page-top">Back to top</a> </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>


    <!-- Instagram Section -->

    <div id="instagram">
        <div class="container">
            <div class="section-title text-center center">


            </div>

            <div class="row">
                <div class="instagram-items ig-items">
'''

ig_index_tail = '''
                </div>
            </div>
        </div>
    </div>






    <div class="scroll">
        <center>
            <a href="instagram1.html" class="next">Next Page</a>
        </center>
    </div>
    <script type="text/javascript" src="../js/bootstrap.js"></script>
    <script type="text/javascript" src="../js/SmoothScroll.js"></script>
    <script type="text/javascript" src="../js/jqBootstrapValidation.js"></script>
    <script type="text/javascript" src="../js/jquery.jscroll.js"></script>
    <script type="text/javascript" src="../js/main.js"></script>
    <script type="text/javascript">
        $('.fancybox').fancybox({
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
        $('.scroll').jscroll({
            nextSelector: 'a.next'
        });
    </script>

</body>

</html>
'''

iter_file_head = '''
<div class="container">
    <div class="row">
        <div class="instagram-items ig-items">
'''


def reset_dir():
    for the_file in os.listdir(instagram_page_folder):
        file_path = os.path.join(instagram_page_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    ig_index_file = os.path.join(instagram_page_folder, 'instagram.html')
    with open(ig_index_file, 'w') as f:
        f.write(ig_index_head)
    logging.info('Instagram folder reset')


def write_photo_entry(file_name, media_file_path, caption, owner, thumbnail_path):
    with open(file_name, 'a') as myfile:
        myfile.write('          <div class="col-sm-6 col-md-3 col-lg-3">')
        myfile.write('\n')
        myfile.write('              <div class="instagram-item">')
        myfile.write('\n')
        myfile.write('                  <div class="hover-bg">')
        myfile.write('\n')
        myfile.write('                  <a tabindex="1" href="../' + media_file_path + '" title="' + caption + '" rel="lightbox" class="fancybox">')
        myfile.write('\n')
        myfile.write('                      <div class="hover-text">')
        myfile.write('\n')
        myfile.write('                      <h4>' + owner + '</h4>')
        myfile.write('\n')
        myfile.write('                      <small>' + caption + '</small> </div>')
        myfile.write('\n')
        myfile.write('                      <img src="../' + thumbnail_path + '" class="img-responsive lazy" alt="' + caption + '">')
        myfile.write('\n')
        myfile.write('                  </a>')
        myfile.write('\n')
        myfile.write('                  </div>')
        myfile.write('\n')
        myfile.write('              </div>')
        myfile.write('\n')
        myfile.write('          </div>')
        myfile.write('\n')


def create_index_html():
    f = open(lsphotos_json, 'r')
    insta_dict = json.loads(f.read())
    insta_dict = sorted(insta_dict['images'], key=itemgetter('date'), reverse=True)
    iter_num = 0
    ig_index_file = os.path.join(instagram_page_folder, 'instagram.html')
    with open(ig_index_file, 'w') as f:
        f.write(ig_index_head)
    for item in insta_dict:
        caption = decode_unicode_references(item['caption'])
        write_photo_entry(ig_index_file, item['media_file_path'], caption, item['owner']['username'], item['thumbnail_path'])
        iter_num += 1
        if iter_num == 20:
            with open(ig_index_file, 'a') as f:
                f.write(ig_index_tail)
            logging.info('created instagram index file')
            break


def create_page_html():
    f = open(lsphotos_json, 'r')
    insta_dict = json.loads(f.read())
    insta_dict_items = len(insta_dict['images'])
    insta_dict = sorted(insta_dict['images'], key=itemgetter('date'), reverse=True)
    iter_num = 0
    page_num = 1
    ig_iter_file = os.path.join(instagram_page_folder, 'instagram' + str(page_num) + '.html')
    with open(ig_iter_file, 'a') as f:
        f.write('<div class="container">\n')
        f.write('   <div class="row">\n')
        f.write('       <div class="instagram-items ig-items">\n')
    for item in insta_dict:
        iter_num += 1
        if iter_num < 20:
            pass
        elif iter_num == 20:
            caption = decode_unicode_references(item['caption'])
            write_photo_entry(ig_iter_file, item['media_file_path'], caption, item['owner']['username'], item['thumbnail_path'])
        else:
            if iter_num % 20 == 0:
                ig_iter_file = os.path.join(instagram_page_folder, 'instagram' + str(page_num) + '.html')
                with open(ig_iter_file, 'a') as f:
                    f.write('<div class="container">\n')
                    f.write('   <div class="row">\n')
                    f.write('       <div class="instagram-items ig-items">\n')
            caption = decode_unicode_references(item['caption'])
            write_photo_entry(ig_iter_file, item['media_file_path'], caption, item['owner']['username'], item['thumbnail_path'])
            if iter_num % 20 == 0 and iter_num < insta_dict_items:
                ig_iter_file = os.path.join(instagram_page_folder, 'instagram' + str(page_num) + '.html')
                with open(ig_iter_file, 'a') as f:
                    f.write('<div class="scroll">')
                    f.write('<center>')
                    f.write('<a href="instagram' + str(page_num + 1) + '.html" class="next">Next Page</a>')
                    f.write('</center>')
                page_num += 1
                logging.info('created page number ' + str(page_num))


def pretty_html():
    for the_file in os.listdir(instagram_page_folder):
        file_path = os.path.join(instagram_page_folder, the_file)
        with open(file_path, 'r') as f:
            text = f.read()
        soup = BeautifulSoup(text, "html.parser")
        prettyHTML = soup.prettify()
        with open(file_path, 'w') as f:
            f.write(prettyHTML)
        logging.info('prettified ' + str(file_path))


def iterate_json():
    f = open(lsphotos_json, 'r')
    insta_dict = json.loads(f.read())
    insta_dict_items = len(insta_dict['images'])
    insta_dict = sorted(insta_dict['images'], key=itemgetter('date'), reverse=True)
    iter_num = 1
    page_num = 1
    ig_iter_file = os.path.join(instagram_page_folder, 'instagram' + str(page_num) + '.html')
    ig_index_file = os.path.join(instagram_page_folder, 'instagram.html')
    for item in insta_dict:
        ig_iter_file = os.path.join(instagram_page_folder, 'instagram' + str(page_num) + '.html')
        caption = decode_unicode_references(item['caption'])
        if iter_num < 21:
            write_photo_entry(ig_index_file, item['media_file_path'], caption, item['owner']['username'], item['thumbnail_path'])
        else:
            write_photo_entry(ig_iter_file, item['media_file_path'], caption, item['owner']['username'], item['thumbnail_path'])
            if iter_num % 20 == 0 and iter_num < insta_dict_items:
                with open(ig_iter_file, 'r+') as f:
                    content = f.read()
                    f.seek(0, 0)
                    f.write(iter_file_head + '\n' + content)
                with open(ig_iter_file, 'a') as f:
                    f.write('<div class="scroll">')
                    f.write('<center>')
                    f.write('<a href="instagram' + str(page_num + 1) + '.html" class="next">Next Page</a>')
                    f.write('</center>')
                logging.info('page written ' + str(page_num))
                page_num += 1
        iter_num += 1
    with open(ig_index_file, 'a') as f:
        f.write(ig_index_tail)

# reset_dir()
# # create_index_html()
# # create_page_html()
# # pretty_html()
# iterate_json()
