import random

import PySimpleGUI as sg
import numpy as np

from models import CircularLinkedList
from utils import get_image, get_image_data, rotate_image, image_tint


class JosephusWindow:
    RADIUS = 300
    PERSON_SIZE = 90
    PERSON_IMAGE = get_image('survivor.png')
    SIZE = (2 * RADIUS + 2 * PERSON_SIZE, 2 * RADIUS + 2 * PERSON_SIZE)
    ELIMINATED_COLOR = "#ff6b77"

    def __init__(self, people_count):

        sg.theme('DarkAmber')
        self.graph = sg.Graph(self.SIZE, (0, 0), self.SIZE, expand_x=True, expand_y=True)
        layout = [[self.graph]]
        self.window = sg.Window('Josephus Problem', layout, resizable=False, finalize=True)

        self.current_turn = 0
        self.people_linked_list = CircularLinkedList.range(0, people_count)
        self.people_list = [True] * people_count
        self.draw()

    def draw(self, finished=False):
        w, h = self.graph.get_size()
        center_x, center_y = w // 2, h // 2
        r = self.RADIUS
        people_count = len(self.people_list)
        angles = np.linspace(0, 2 * np.pi, people_count, endpoint=False)
        for i, ang in enumerate(angles):
            image = rotate_image(self.PERSON_IMAGE, - ang - np.pi / 2)
            if not self.people_list[i]:
                image = image_tint(image, self.ELIMINATED_COLOR)
            dx = image.width // 2
            dy = image.height // 2
            x = center_x + r * np.sin(ang)
            y = center_y + r * np.cos(ang)
            self.graph.draw_image(data=get_image_data(image), location=(x - dx, y + dy))
            self.graph.draw_circle((x, y), 15, fill_color='white')
            self.graph.draw_text("{}".format(i + 1), (x, y), font='Helvetica 15', color='black', angle=-ang * 180 / np.pi)
            i += 1
        if finished:
            self.graph.draw_text("Winner: {}".format(self.people_linked_list[0] + 1), (center_x, center_y),
                                 font='Helvetica 30', color='white')

    def step(self):
        size = len(self.people_linked_list)
        if size == 1:
            self.graph.erase()
            self.draw(True)
            return False
        self.current_turn = (self.current_turn + 1) % size
        removing_person = self.people_linked_list[self.current_turn]
        self.people_list[removing_person] = False
        self.people_linked_list.remove(self.current_turn)
        self.graph.erase()
        self.draw()
        return True

    def run(self):
        continues = True
        while True:
            event, values = self.window.read(timeout=1000 if continues else None)
            if continues:
                continues = self.step()
            if event == sg.WIN_CLOSED:
                break

    def __enter__(self):
        self.run()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.window.close()
