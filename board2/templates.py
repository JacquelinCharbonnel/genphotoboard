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

css_main = ""

css_container = """
.container {
  width: 90%;
  margin: 1rem auto;
}"""
  
css_grid = """
.grid {
  display: grid;
  grid-template-columns: repeat({{cols}}, 1fr);
  grid-template-rows: repeat({{rows}}, 5vw);
  grid-gap: {{gap}};
  justify-items: center;
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
  <script>
    window.onload = () => {
      const modale = document.querySelector("#modale");
      const close = document.querySelector(".close");
      const links = document.querySelectorAll(".grid figure a");
      console.log(links)

      for (let link of links) {
        link.addEventListener("click", function(e) {
          e.preventDefault();

          console.log(link)
          const image = modale.querySelector(".modale-content img");
          image.src = this.href;

          modale.classList.add("show");
        }) ;
      }

      close.addEventListener("click", function() {
        modale.classList.remove("show");
      }) ;

      modale.addEventListener("click", function() {
        modale.classList.remove("show");
      }) ;
    }
  </script>

  <title>CSS Grids Gallery</title>

"""        

html_frame_figure = """
        <a href="{{image}}" target="max">
          <img src="{{image}}" alt="Board image" class="frame_figure">
        </a>  
"""

html_frame_text = """
        <div class="frame_text">{{text}}</div>
"""

html_modale = """
    <div id="modale" class="modale">
      <span class="close">&times;</span>
      <div class="modale-content">
        <img src="" alt="" />
      </div>
    </div>
"""

css_modale = """

.modale {
  display: none;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  background-color: {{background}};
}

.modale.show {
  display: initial;
}

.modale-content {
  width: 90%;
  margin: auto;
  /* max-width: 1200px; */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
}

.modale-content img {
  width: 100%;
} 

.close {
  color: white ;
  font-size: 2em;
  position: fixed;
  top: 10px;
  right: 10px;
  cursor: pointer;
}
"""      

