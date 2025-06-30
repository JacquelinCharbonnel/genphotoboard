#!/bin/env python

"""
Jacquelin Charbonnel 2025

https://www.freecodecamp.org/news/how-to-create-an-image-gallery-with-css-grid-e0f0fd666a5c/
https://visme.co/blog/fr/mise-en-page/
https://developer.mozilla.org/fr/docs/Web/CSS/CSS_grid_layout/Grid_template_areas
https://www.youtube.com/watch?v=2R525oEOl2s
https://www.pierre-giraud.com/grille-css-guide-complet-grid-layout/
https://www.ionos.fr/digitalguide/sites-internet/creation-de-sites-internet/grilles-css/

https://layout.bradwoods.io/customize
https://www.cssportal.com/css-flexbox-generator/

https://tutorialzine.com/2017/02/freebie-4-bootstrap-galleries
https://fr.piwigo.org/piwigo-cest-quoi

https://lokeshdhakar.com/projects/lightbox2/#examplesc
https://www.digitalia.be/software/slimbox2/#downloadc
https://photoswipe.com/
https://github.com/dimsemenov/Magnific-Popup
"""

import sys, os, importlib
import board1def
import yaml
from jinja2 import Template

class Stream:
  def __init__(self):
    self.clear()

  def clear(self):
    self.indent = 0
    self.stream = []
    
  def inc(self):
    self.indent += 1
  def dec(self):
    self.indent -=1

  def __lshift__(self,s):
    self.stream += [ f"{" "*2*self.indent}{s}" ]

  def __str__(self):
    return "\n".join(self.stream)

class Element:
  def __init__(self,name,classes,html,css):
    self.name = name
    self.html = html
    self.css = css
    self.classes = classes

    s = f"<{self.name}"
    if self.classes:
      s += f' class="{",".join(self.classes)}"'
    s += ">"

    self.html << s
    self.html.inc()

  def __enter__(self):
    return self

  def __exit__(self,type,value,traceback):
    self.html.dec()
    self.html << f"</{self.name}> <!-- {self.classes} -->"

  def get_html(self):
    return str(self.html)

class Html(Element):
  def __init__(self,templates,html,css):
    super().__init__("html",None,html,css)
    css << Template(templates.css_html).render(board["html"])

class Head(Element):
  def __init__(self,html):
    super().__init__("head",classes=None,html=html,css=None)
    # html << Template(templates.html_head)

class Body(Element):
  def __init__(self,classes,templates,html,css):
    super().__init__("body",classes=classes,html=html,css=css)
    css << Template(templates.css_body).render(board["body"])

class Main(Element):
  def __init__(self,classes,templates,html,css):
    super().__init__("main",classes,html=html,css=css)
    css << Template(templates.css_main).render(board["main"])

class H1(Element):
  def __init__(self,classes,html,css):
    super().__init__("h1",classes=classes,html=html,css=css)

class Container(Element):
  def __init__(self,classes,templates,html,css):
    super().__init__("div",["container"],html=html,css=css)
    css << Template(templates.css_container).render(board["container"])

class Grid(Element):
  def __init__(self,classes,templates,html,css):
    super().__init__("div",["grid"],html=html,css=css)
    css << Template(templates.css_grid).render(board["grid"])
        
class Frame(Element):
  def __init__(self,name,id,classes,templates,html,css):
    super().__init__(name,classes,html,css)
    with Style(f"f{id+1}",css) as st:
      self.css << f"grid-area: f{id+1};"

class Figure(Frame):
  def __init__(self,name,id,classes,templates,html,css):
    super().__init__("figure",id,classes,templates,html,css)

    # html << f"""<img src="{board['frame'][id]["img"]}" alt="Board image" class="frame_figure">"""
    html << Template(templates.html_frame_figure).render({"image": board['frame'][id]["img"]})

class Text(Frame):
  def __init__(self,name,id,classes,templates,html,css):
    super().__init__("div",id,classes,templates,html,css)

    html << Template(templates.html_frame_text).render({"text": board['frame'][id]["text"]})
    # html << f"""{board['frame'][id]["text"]}"""

class Style:
  def __init__(self,name,css):
    self.name = name
    self.css = css

  def __enter__(self):
    s = f".{self.name} {{"
    self.css << s
    self.css.inc()
    return self

  def __exit__(self,type,value,traceback):
    self.css.dec()
    self.css << "}\n"

  def get_css(self):
    return str(self.css)

class Page:
  def __init__(self):
    pass

class BoardPage(Page):
  def __init__(self,board):
    self.board = board

  def render(self): 
    board = self.board

    template_file = board["template_file"]
    print(template_file)   
    template_spec = importlib.util.spec_from_file_location("templates", template_file)
    templates = importlib.util.module_from_spec(template_spec)
    sys.modules["templates"] = templates
    template_spec.loader.exec_module(templates)

    html_complete = Stream()
    html_body = Stream()
    css = Stream()

    css << Template(templates.css_glob).render(board["glob"])
    css << Template(templates.css_modale).render(board["modale"])

    with Body(classes=[],templates=templates,html=html_body,css=css):
      with Main(classes=[],templates=templates,html=html_body,css=css):
      #  with H1(classes=[],html=html_body,css=css) as h1:
      #   h1.html << "mon titre"
       with Container(classes=[],templates=templates,html=html_body,css=css) as c:
        with Grid(classes=[],templates=templates,html=html_body,css=css) as g:
          css << Template(templates.css_frame_figure).render(board["frame_figure"])
          css << Template(templates.css_frame_text).render(board["frame_text"])
          for (i,f) in enumerate(board["frame"]) :
            # with Element(f["elt"],classes=[f"f{i}"]) as elt:
            with eval(f["elt"])(name=f"f{i+1}",id=i,classes=[f"f{i+1}"],templates=templates,html=html_body,css=css) as elt:
              pass

      html_body << Template(templates.html_modale).render({})

    html_complete << "<!DOCTYPE html>"
    with Html(html=html_complete,templates=templates,css=css):
      with Head(html=html_complete):
        html_complete << Template(templates.html_head).render({"inline_style": css})
      html_complete << html_body  

    # html_file = os.path.join(board_dir,"index.html")
    with open(board["output_file"],"w") as f:  
      print(html_complete, file=f)

    print(html_complete)


if __name__=="__main__":

  if len(sys.argv)!=3:
    print(f"""
usage: {sys.argv[0]} working_dir board_name
    """)
    exit(1)
  board_dir = sys.argv[1]
  board_name = sys.argv[2]
  board_def = os.path.join(board_dir,board_name)

  board = yaml.load(open(board_def,"r"),Loader=yaml.CLoader)

  os.chdir(board_dir)

  page = BoardPage(board)
  page.render()
  
