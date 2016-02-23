
import os
import sys, getopt
import uuid
from string import Template
from markdown import markdown

def render_slide(source, global_config):
    src_file = open(source, 'r')
    config = global_config.copy()
    content = ""
    uid = str(uuid.uuid4()) 
    config['uuid'] = uid   
    for line in src_file:
        if line.startswith("@"):
            p=line[1:-1].split(":",1)
            config[p[0]]=p[1]
        else:
            content = content + line

    src_file.close()
    if config.get("rendering","") == "markdown":
        content = markdown(content)
    config['content'] = content    
    ## print "render with config " + str(config) + " and content " + content

    template_name = config.get("template", "content").strip() + ".html"
    template_file = open("templates/" + template_name, 'r')    
    template = Template(template_file.read())
    template_file.close()
    rendered_content = template.safe_substitute(config)

    return { 'content' : rendered_content,  'uuid': uid,  'notes': config.get("notes", "")}


def generate_slides(base_dir, config,outputfile):
    notes = {};
    content = []
    chapters = os.listdir(base_dir)
    chapters.sort()
    for chapter in chapters:
        current_path = base_dir + "/" + chapter        
        if os.path.isdir(current_path):
            slides = os.listdir(current_path)
            slides.sort()
            content.append("<section>")
            for slide in slides :
                print "processing " + chapter + " " + slide
                res = render_slide(current_path + "/" + slide, config)
                #print "res=" + str(res)
                content.append(res['content'])
                notes[res['uuid']]= res['notes']                
            content.append("</section>")
        else:
            res = render_slide(current_path, config)
            content.append(res['content'])
            notes[res['uuid']]= res['notes']                

    template_file = open("templates/index.html" , 'r')    
    template = Template(template_file.read())
    template_file.close()
    
    config['content'] = "".join(content)
    config['notes'] = str(notes)
    rendered_content = template.safe_substitute(config)
    
    result_file = open(outputfile , 'w')
    result_file.write(rendered_content)
    result_file.close()

    ## print str(renditions)

def main(argv=None):

  inputdir ="src/slides"
  config_file = "slides.config"
  outputfile= "generated.html"

  print "args " + str(argv) 

  try:
      opts, args = getopt.getopt(argv[1:],"i:c:o:",["source=","config=","out="])
  except getopt.GetoptError:
      print 'assemble.py -c <slides.config> -i <inputdir> -o <outputfile>'
      sys.exit(2)    

  print "parsed opts " + str(opts)

  for opt, arg in opts:
      print "opt=" + opt
      if opt in ("-i", "--source"):
         inputdir = arg
      elif opt in ("-c", "--config"):
         config_file = arg
      elif opt in ("-o", "--out"):
         outputfile = arg

  print "running generation with input %s " % inputdir
  src_file = open(config_file, 'r')
  config = {}
  for line in src_file:
      if line.startswith("@"):
          p=line[1:-1].split(":",1)
          config[p[0]]=p[1]
  src_file.close()
  generate_slides(inputdir, config, outputfile)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
