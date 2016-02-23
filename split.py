
import os
import sys, getopt

from pyquery import PyQuery  

def  _dump_slide(slide, idx_slide, outputdir):

    html = PyQuery(slide).html();
    slide_name = '%03d.html' % idx_slide
    print "dump slide {} in dir {}".format(idx_slide, outputdir)    
    dump = open(os.path.join(outputdir,slide_name), 'w+')
    dump.write("@template:content_bare\n")
    dump.write(html.encode('utf-8','replace'))
    dump.close()

def _split(inputfile, outputdir):
    source = open(inputfile, 'r')
    html = source.read()
    source.close()

    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)

    idx_slide=0
    idx_section=0

    parsed = PyQuery(html)
    
    for section in parsed('section'):
        slide = PyQuery(section)        
        if slide.has_class('stack'):
            idx_section+=1
            stack_path = os.path.join(outputdir,'%02d' % idx_section )
            os.mkdir(stack_path)
            for sub_slide in PyQuery(slide.html())('section'):
                idx_slide+=1
                _dump_slide(sub_slide, idx_slide, stack_path)
        else: 
            if not slide.parent().has_class('stack'):
                idx_slide+=1
                _dump_slide(slide, idx_slide, outputdir)                    

def main(argv=None):

  inputfile = 'source.html'
  outputdir= 'out'

  try:
      opts, args = getopt.getopt(argv[1:],"i:o:",["source=","out="])
  except getopt.GetoptError:
      print 'split.py -i <inputfile> -o <outputdir>'
      sys.exit(2)    

  for opt, arg in opts:
      if opt in ("-i", "--source"):
         inputfile = arg
      elif opt in ("-o", "--out"):
         outputdir = arg

  _split(inputfile,outputdir)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
