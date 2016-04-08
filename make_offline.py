
import os
import urllib2
import uuid
import md5
import sys, getopt

from BeautifulSoup import BeautifulSoup

def  _dump_slide(slide, idx_slide, outputdir):

    html = PyQuery(slide).html();
    slide_name = '%03d.html' % idx_slide
    print "dump slide {} in dir {}".format(idx_slide, outputdir)    
    dump = open(os.path.join(outputdir,slide_name), 'w+')
    dump.write("@template:content_bare\n")
    dump.write(html.encode('utf-8','replace'))
    dump.close()

def _offline(inputfile):
    source = open(inputfile, 'r')
    html = source.read()
    source.close()

    source = open(inputfile, 'rb')
    htmlout = unicode(source.read(), "utf-8")
    source.close()
  
    wdir = os.path.dirname(inputfile)
    outputfile = os.path.join(wdir, 'offline.html')
    imgdir_path = os.path.join(wdir,'img')
    if not os.path.exists(imgdir_path):
       os.mkdir(imgdir_path)

    soup = BeautifulSoup(html)
    for img in soup.findAll('img'):
       if (img['data-src'].startswith("http")):
           imgfilename = md5.new(img['data-src']).hexdigest() + ".png"
           if (not os.path.exists(os.path.join(imgdir_path, imgfilename))):
              print("downloading image " + img['data-src'])           
              imgstream = urllib2.urlopen(img['data-src'])
              with open(os.path.join(imgdir_path, imgfilename),'wb') as output:
                 output.write(imgstream.read())
           else:
               print("image " + img['data-src'] + " already in cache")           
           targetFilename = "img/" + imgfilename
           print " translating " + img['data-src']  + " to " + targetFilename 
           #img['data-src'] = "img/" + imgfilename
           htmlout = htmlout.replace(img['data-src'], targetFilename)
    offline_html = str(soup)
    
    out = open(outputfile,'wb')
    #out.write(offline_html)
    out.write(htmlout.encode("utf-8"))
    out.close()



def main(argv=None):

  inputfile = 'index.html'
  try:
      opts, args = getopt.getopt(argv[1:],"i:",["source="])
  except getopt.GetoptError:
      print 'make_offline.py -i <inputfile>'
      sys.exit(2)    

  for opt, arg in opts:
      if opt in ("-i", "--source"):
         inputfile = arg

  _offline(inputfile)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
