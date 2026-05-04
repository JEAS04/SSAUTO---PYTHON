# pip install screeninfo
from screeninfo import get_monitors

for m in get_monitors():
    print(str(m))
    # m.width, m.height, m.x, m.y (coordenadas del monitor)


#monitor = get_monitors()[0]

#print("Ancho:", monitor.width)
#print("Alto:", monitor.height)