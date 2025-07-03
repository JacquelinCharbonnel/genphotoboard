"""
Templates to generate some parts of the HTM and CSS contents of the board
"""

from jinja2 import Template

css_glob = """  
*,
*::after,
*::before {
  margin: 0;
  padding: 0;
  box-sizing: inherit; 
  }"""

css_html = """
html {
  box-sizing: border-box;
  font-size: {{font_size}}; 
  }"""

css_body = """
body {
  font-family: "Nunito", sans-serif;
  color: #333;
  font-weight: 300;
  line-height: 1.6; 
  background-color: {{background_color}};
}"""

css_main = """
main {
  font-family: "Nunito", sans-serif;
  color: #333;
  font-weight: 300;
  line-height: 1.6; 
  background-color: {{background_color}};
}"""

css_container = """
.container {
  width: 90%;
  margin: 1rem auto;
}"""
  
css_ul = """
.container ul {
 display: flex;
   list-style-type: none;
   overflow: hidden;
   margin-block-start: 1em;
   margin-block-end: 1em;
  align-items: center;
}
"""

css_li = """
.container ul li {
    flex: 0 0 20%;
    max-width: 20%;
    position: relative;
}
"""

css_img = """
ul li img {
    padding: 3%;
  }
"""

css_frame_figure = """
.frame_figure {
  width: 100%;
  height: 100%;
  # object-fit: cover;
  object-fit: scale-down; #jc
  display: block; 
}"""

css_frame_text = """
.frame_text {
  font-size: {{font_size}};
  color: {{color}};
  font-weight: {{font_weight}};
}"""

html_head = """
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">

  <link href="https://fonts.googleapis.com/css?family=Josefin+Sans:300,400,400i|Nunito:300,300i" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <link rel="shortcut icon" type="image/png" href="img/favicon.png">
  <link rel="stylesheet" href="photoswipe/dist/photoswipe.css">

  <style>
    {{inline_style}}
  </style>

  <title>CSS Grids Gallery</title>

"""        

html_body = """
    avant
    {{inline_body}}
    après
"""        

html_frame_figure = """
        <a href="{{target}}">
          <img src="{{image}}" alt="Board image" class="frame_figure">
        </a>  
"""

html_frame_text = """
        <a href="{{target}}">
          <div class="frame_text">{{text}}</div>
        </a>  
"""



