from ui import *
from constants import *

panel = Panel( (WIDTH - 350, 470), 345, 110, (8, 3, 12), alpha=128 )
panel.color = (0,0,0)

UItoggle = TextUI("Press 'U' to show parameter panel", (WIDTH-180, 120), (55, 120, 255))

ScaleText = TextUI("Scale ", (WIDTH-245,520), (255,255,255))
sliderScale = Slider(WIDTH-280, 550, 40, 0, 100, 180, 10, 80)

decesoButton = Button("Deaths")

Etiquetas = TextUI("Tags: ", (WIDTH-245, 490), (255,255,255))
toggleEtiquetas = ToggleButton( (WIDTH-160, 480), 20, 20, False )