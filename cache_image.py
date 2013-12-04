"""
Script to download images from url and save it to local 

Usage:
cache_image(source='http://www.google.com/image1.jpg', path='/home/jimit/images/', size=(128, 128))
example valid calls : 
cache_image.cache_image(source='/home/vinod/python/webapps/navaalo/navaalo/static/images/mobiles/',path='/home/vinod/choiceman_thumbnails/main_page/',size=(175,175))
cache_image.cache_image(source='/home/vinod/python/webapps/navaalo/navaalo/static/images/mobiles/',path='/home/vinod/choiceman_thumbnails/',size=(46,50))
cache_image(source='http://www.myteenagewerewolf.com/home/lauren/public_html/wp-content/uploads/2010/11/RADIO-2.jpg',path='/home/vinod/choiceman_thumbnails/',size=(46,50))
cache_image.cache_image(source='/home/vinod/python/webapps/navaalo/navaalo/static/images/mobiles/micromax-canvas-doodle-a111.jpg',path='/home/vinod/choiceman_thumbnails/main_page/',size=(175,175))
"""
import sys,traceback
import os
import urllib2
import urllib
import StringIO
from PIL import Image
import re 



class ImageCacheError(Exception):
    def __init__(self,message):
        traceback.print_exc(file=sys.stdout)

class BadInputError(Exception):
    def __init__(self,message):
        print message

def get_image_format(url):
    extension = os.path.splitext(url)[1][1:]
    print "extension is ",extension
    return extension.upper()

def get_image_name(fullpathname):
    extension = fullpathname.split('/')[-1]
    return extension

def validate_params(inputdict):
    print inputdict
    if 'http' in inputdict['source'] :
        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        url_string = inputdict['source']
        isvalid =  regex.search(url)
        if not isvalid:
            raise ValueError("url entered is not in valid format")


        

def cache_image(**kwargs):
    if not 'algorithm' in kwargs.keys():
        kwargs['algorithm'] = 'ANTIALIAS'

    try:
        if 'http://' in kwargs['source']:
            image = urllib2.urlopen(urllib.quote(kwargs['source'].encode('utf8'), safe="%/:=&?~#+!$,;'@()*[]"))
            image.name = kwargs['source']
            format_ = get_image_format(kwargs['source'])
            generateThumbnailAndSave(image,kwargs,format_)
        elif '.jpeg' in kwargs['source'] or '.png' in kwargs['source'] or '.jpg' in kwargs['source']:
            image = open(kwargs['source'])
            format_ = get_image_format(kwargs['source'])
            generateThumbnailAndSave(image,kwargs,format_)
        else:
            perform_execute(kwargs)

    except (urllib2.URLError, urllib2.HTTPError) as e:
        # :todo permanent fix: KeyError is being handled as a
        # temporary fix in case of URI being an IRI
        # ie. Internationalized RI in which there are unicode chars.
        # The urllib.quote fails for these
        raise ImageCacheError(e.message)
    except IOError as e:
        raise ImageCacheError(e.message)

def perform_execute(kwargs):
    filenames = os.listdir(kwargs['source'])
    for filename in filenames:

        image = open(kwargs['source']+filename)
        print "filename is",filename
        format_ = get_image_format(kwargs['source']+filename)
        print image
        generateThumbnailAndSave(image,kwargs,format_)


def generateThumbnailAndSave(image,kwargs,format_):
 
    format_ = 'JPEG' if format_ == 'JPG' else format_
    #on some machine JPG gives error
    try:
        im = StringIO.StringIO(image.read())
        print im
        image_lib_obj = Image.open(im)
        if image_lib_obj.mode != "RGB":
            image_lib_obj = image_lib_obj.convert("RGB")
        image_lib_obj.thumbnail(kwargs['size'],getattr(Image,kwargs['algorithm']))
        path = kwargs['path']+get_image_name(image.name)
        image_lib_obj.save(path, format_)
    except IOError as e:
        raise ImageCacheError(e.message)
    except Exception as e:
        raise ImageCacheError(e.message)

