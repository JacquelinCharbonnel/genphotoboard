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

# from yaml import load, dump
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper

# import templates

# if len(sys.argv)!=2:
#   print(f"""
# usage: {sys.argv[0]} board_name
#   """)
# board_name = sys.argv[1]

# class Board:
#   def __init__(self,fn):
#     stream = open(fn, 'r')    
#     self.data = load(stream, Loader=yaml.CLoader)

#   def __call__(self):
#     return self.data

# board = Board(board_name)()
# board = yaml.load(open(f"{board_name}.yml","r"),Loader=yaml.CLoader)

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

# html_complete = Stream()
# html_body = Stream()
# css = Stream()

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

class Header(Element):
  def __init__(self,html):
    super().__init__("header",classes=None,html=html,css=None)
    html << str(Template(templates.html_header))

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

class Grid(Element):
  def __init__(self,classes,html,css):
    super().__init__("div",["grid"],html=html,css=css)
    with Style("grid",css) as st:
      for l in f"""\
display: grid;
grid-template-columns: repeat({board["grid"]["cols"]}, 1fr);
grid-template-rows: repeat(8, 5vw);
grid-gap: 1.5rem;
grid-template-areas:
{board["grid"]["areas"]}
""".split("\n"):
        self.css << l
        
class Frame(Element):
  def __init__(self,name,id,classes,html,css):
    super().__init__(name,classes,html,css)
    with Style(f"f{id+1}",css) as st:
      self.css << f"grid-area: f{id+1};"

class Figure(Frame):
  def __init__(self,name,id,classes,html,css):
    super().__init__("figure",id,classes,html,css)

    html << f"""<img src="{board['frame'][id]["img"]}" alt="Board image" class="figure">"""

class Div(Frame):
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

# importlib.import_module(sys.argv[1])

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

  # s = Stream()
  # s << "1"
  # s.inc()
  # s << "2"
  # print(s)

  # with Element("test",classes=[]) as e:
  #   e.html << "azerty"
  #   with Element("test2",classes=["un","deux"]) as e:
  #     e.html << "qsdf"
  #   e.html << "azerty"
  
    # print(html)
    # html.clear()

  css << Template(templates.css_glob).render(board["glob"])

  with Body(classes=[],html=html_body,css=css):
    with H1(classes=[],html=html_body,css=css) as h1:
     h1.html << "mon titre"
    with Container(classes=[],html=html_body,css=css) as c:
      with Grid(classes=[],html=html_body,css=css) as g:
        for (i,f) in enumerate(board["frame"]) :
          # with Element(f["elt"],classes=[f"f{i}"]) as elt:
          with eval(f["elt"])(name=f"f{i+1}",id=i,classes=[f"f{i+1}"],html=html_body,css=css) as elt:
            pass
          # if "img" in frame:
          #   elt = "figure"
          # with Frame(f"f{i}"):
          #   pass
          # cl = f"f{i}"
          # with Style(cl) as st:
          #   # st.css << f"grid-column: {f['coord'][0][0]} / span {f['coord'][0][1]}"
          #   # st.css << f"grid-row: {f['coord'][1][0]} / span {f['coord'][1][1]}"
          #   if "img" in f:
          #     st.css << f"grid-area: i{i}"
          #     with Element("figure",[cl]) as fig:
          #       fig.html << "<img ..>"
          #   if "text" in f:
          #     st.css << f"grid-area: t{i}"
          #     with Element("div",[cl]) as text:
          #       text.html << f["text"]
            
  # print(html_body)

  with Html(html=html_complete,css=css):
    with Header(html=html_complete):
      html_complete << Template(templates.html_header).render({"inline_style": css})
    html_complete << html_body  

  with open(f"build/{board_name}","w") as f:  
    print(html_complete, file=f)

  print(html_complete)

  # print(css)
# # print(templates["templates"])
# print(str(templates))
# print(board["body"]["background_color"])
# print(templates.format(**vars()))    
# # print(board["body"])  
# print(vars())
# print(sys.argv[1])