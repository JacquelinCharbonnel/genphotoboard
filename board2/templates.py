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
  background-color: {{background_color}}
}"""

css_container = """
.container {
  width: 60%;
  margin: 2rem auto;
}"""
  
css_grid = """
.grid {
  display: grid;
  grid-template-columns: repeat({{cols}}, 1fr);
  grid-template-rows: repeat({{rows}}, 5vw);
  grid-gap: {{gap}};
  grid-template-areas:
{{areas}};
}"""

css_frame_figure = """
.frame_figure {
  width: 100%;
  height: 100%;
  # object-fit: cover;
  object-fit: scale-down; #jc
  display: block; 
}"""

html_head = """
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">

  <link href="https://fonts.googleapis.com/css?family=Josefin+Sans:300,400,400i|Nunito:300,300i" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <link rel="shortcut icon" type="image/png" href="img/favicon.png">
  <style>
    {{inline_style}}
  </style>
  <script>
  </script>
  <title>CSS Grids Gallery</title>
"""        

html_figure = """
        <a href="{{image}}" target="max">
          <img src="{{image}}" alt="Board image" class="frame_figure">
        </a>  
"""