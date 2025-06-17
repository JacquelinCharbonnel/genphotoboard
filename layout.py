#!/bin/env python

"""
https://www.freecodecamp.org/news/how-to-create-an-image-gallery-with-css-grid-e0f0fd666a5c/
https://visme.co/blog/fr/mise-en-page/
https://developer.mozilla.org/fr/docs/Web/CSS/CSS_grid_layout/Grid_template_areas
"""

import sys, importlib
import board1def
from jinja2 import Template

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import skel

class Board:
  def __init__(self,fn):
    stream = open(fn, 'r')    
    self.data = load(stream, Loader=Loader)

  def __call__(self):
    return self.data

board = Board(sys.argv[1])()
# skel = load(open("skel.yml","r"), Loader=Loader)

frame = \
  [
    {
      "img": "img/im.webp"
      , "coord" : ((0,2),(0,2))
    }
    , {
        "text": "un texte ici"
        , "coord": ((2,2),(0,2))
    }
  ]

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

html = Stream()
css = Stream()

class Element:
  def __init__(self,name,classes=[],html=html,css=css):
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
    self.html << f"</{self.name}>"

  def get_html(self):
    return str(self.html)

class Html(Element):
  def __init__(self):
    super().__init__("html")
    css << Template(skel.html).render(board["html"])

class Body(Element):
  def __init__(self):
    super().__init__("body")
    css << Template(skel.body).render(board["body"])

class H1(Element):
  def __init__(self):
    super().__init__("h1")

class Container(Element):
  def __init__(self):
    super().__init__("div",["container"])

class Grid(Element):
  def __init__(self,classes=[],html=html,css=css):
    super().__init__("div",["grid"],html,css)
    with Style("grid") as st:
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
  def __init__(self,name,id,classes=[],html=html,css=css):
    super().__init__(name,classes,html=html)
    with Style(name) as st:
      self.css << f"grid-area: f{id+1};"

class Figure(Frame):
  def __init__(self,name,id,classes=["figure"],html=html,css=css):
    super().__init__("figure",id,classes,html=html)

    html << f"""<img src="{board['frame'][id]["img"]}" alt="Board image" class="figure">"""

class Div(Frame):
  def __init__(self,name,id,classes=[],html=html,css=css):
    super().__init__("div",id,classes,html=html)

    html << f"""{board['frame'][id]["text"]}"""


class Style:
  def __init__(self,name,css=css):
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

  css << Template(skel.glob).render(board["glob"])

  with Html():
   with Body():
    with H1() as h1:
     h1.html << "mon titre"
    with Container() as c:
      with Grid() as g:
        for (i,f) in enumerate(board["frame"]) :
          # with Element(f["elt"],classes=[f"f{i}"]) as elt:
          with eval(f["elt"])(name=f"f{i+1}",id=i,classes=[f"f{i+1}"]) as elt:
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
            

print(html)
print(css)
# # print(skel["skel"])
# print(str(skel))
# print(board["body"]["background_color"])
# print(skel.format(**vars()))    
# # print(board["body"])  
# print(vars())
# print(sys.argv[1])