#!/bin/env python

"""
Jacquelin Charbonnel 2025

https://www.freecodecamp.org/news/how-to-create-an-image-gallery-with-css-grid-e0f0fd666a5c/
https://visme.co/blog/fr/mise-en-page/
https://developer.mozilla.org/fr/docs/Web/CSS/CSS_grid_layout/Grid_template_areas
"""

import sys, importlib
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
  def __init__(self,html,css):
    super().__init__("html",None,html,css)
    css << Template(templates.css_html).render(board["html"])

class Head(Element):
  def __init__(self,html):
    super().__init__("head",classes=None,html=html,css=None)
    # html << Template(templates.html_head)

class Body(Element):
  def __init__(self,classes,html,css):
    super().__init__("body",classes=classes,html=html,css=css)
    css << Template(templates.css_body).render(board["body"])

class H1(Element):
  def __init__(self,classes,html,css):
    super().__init__("h1",classes=classes,html=html,css=css)

class Container(Element):
  def __init__(self,classes,html,css):
    super().__init__("div",["container"],html=html,css=css)
    css << Template(templates.css_container).render(board["container"])

class Grid(Element):
  def __init__(self,classes,html,css):
    super().__init__("div",["grid"],html=html,css=css)
    css << Template(templates.css_grid).render(board["grid"])
        
class Frame(Element):
  def __init__(self,name,id,classes,html,css):
    super().__init__(name,classes,html,css)
    with Style(f"f{id+1}",css) as st:
      self.css << f"grid-area: f{id+1};"

class Figure(Frame):
  def __init__(self,name,id,classes,html,css):
    super().__init__("figure",id,classes,html,css)

    html << f"""<img src="{board['frame'][id]["img"]}" alt="Board image" class="frame_figure">"""

class Text(Frame):
  def __init__(self,name,id,classes,html,css):
    super().__init__("div",id,classes,html,css)

    html << f"""{board['frame'][id]["text"]}"""

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

if __name__=="__main__":

  if len(sys.argv)!=2:
    print(f"""
usage: {sys.argv[0]} board_name
    """)
  board_name = sys.argv[1]

  board = yaml.load(open(f"{board_name}.yml","r"),Loader=yaml.CLoader)

  templates = importlib.import_module(board["template"])

  html_complete = Stream()
  html_body = Stream()
  css = Stream()

  css << Template(templates.css_glob).render(board["glob"])

  with Body(classes=[],html=html_body,css=css):
    with H1(classes=[],html=html_body,css=css) as h1:
     h1.html << "mon titre"
    with Container(classes=[],html=html_body,css=css) as c:
      with Grid(classes=[],html=html_body,css=css) as g:
        css << Template(templates.css_frame_figure).render(board["frame_figure"])
        for (i,f) in enumerate(board["frame"]) :
          # with Element(f["elt"],classes=[f"f{i}"]) as elt:
          with eval(f["elt"])(name=f"f{i+1}",id=i,classes=[f"f{i+1}"],html=html_body,css=css) as elt:
            pass

  html_complete << "<!DOCTYPE html>"
  with Html(html=html_complete,css=css):
    with Head(html=html_complete):
      html_complete << Template(templates.html_head).render({"inline_style": css})
    html_complete << html_body  

  with open(f"build/{board_name}.html","w") as f:  
    print(html_complete, file=f)

  print(html_complete)

