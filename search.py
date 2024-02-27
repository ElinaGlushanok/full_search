import os
import sys
import pygame
import requests
from adjust_ll_span import adjust_ll_span


def show_map(ll_spn, type="map", add_params=None):
    map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={type}"
    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)
    if not response:
        sys.exit(1)
    map = "map.png"
    try:
        with open(map, "wb") as file:
            file.write(response.content)
    except IOError:
        sys.exit(2)

    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    screen.blit(pygame.image.load(map), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        continue

    pygame.quit()
    os.remove(map)


place = " ".join(sys.argv[1:])
if not place:
    print('Введите данные')
    sys.exit(0)
ll, spn = adjust_ll_span(place)
show_map(spn, "map", add_params=f"pt={ll}")
