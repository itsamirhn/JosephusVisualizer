import PySimpleGUI as sg
import numpy as np

from utils import get_image, get_image_data, rotate_image, image_tint
from .josephus import Josephus


class JosephusVisualizer:
    RADIUS = 300
    SOLDIER_SIZE = 90
    SOLDIER_IMAGE = get_image('assets/survivor.png')
    SIZE = (2 * RADIUS + 2 * SOLDIER_SIZE, 2 * RADIUS + 2 * SOLDIER_SIZE)
    ELIMINATED_COLOR = "#ff6b77"

    def __init__(self, josephus: Josephus):

        sg.theme('DarkAmber')
        self.graph = sg.Graph(self.SIZE, (0, 0), self.SIZE, expand_x=True, expand_y=True)
        layout = [[self.graph]]
        self.window = sg.Window('Josephus Problem', layout, resizable=False, finalize=True)

        self.josephus = josephus
        self.draw()

    def get_center(self):
        w, h = self.graph.get_size()
        return w // 2, h // 2

    def get_angles(self):
        return np.linspace(0, 2 * np.pi, len(self.josephus.aliveness()), endpoint=False)

    def get_positions(self):
        center_x, center_y = self.get_center()
        positions = []
        for ang in self.get_angles():
            x = center_x + self.RADIUS * np.sin(ang)
            y = center_y + self.RADIUS * np.cos(ang)
            positions.append((x, y, ang))
        return positions

    def draw_soldier_image(self, x, y, angle, alive):
        image = rotate_image(self.SOLDIER_IMAGE, - angle - np.pi / 2)
        if not alive:
            image = image_tint(image, self.ELIMINATED_COLOR)
        dx = image.width // 2
        dy = image.height // 2
        self.graph.draw_image(data=get_image_data(image), location=(x - dx, y + dy))

    def draw_soldier_id(self, x, y, soldier_id):
        self.graph.draw_circle((x, y), 15, fill_color='white')
        self.graph.draw_text("{}".format(soldier_id), (x, y), font='Helvetica 15', color='black')

    def draw_survivor(self, soldier_id):
        center_x, center_y = self.get_center()
        self.graph.draw_text("Survivor: {}".format(soldier_id), (center_x, center_y),
                             font='Helvetica 30', color='white')

    def draw(self):
        aliveness = self.josephus.aliveness()

        for i, pos in enumerate(self.get_positions()):
            x, y, ang = pos
            self.draw_soldier_image(x, y, ang, aliveness[i])
            self.draw_soldier_id(x, y, i + 1)

        if self.josephus.survivor is not None:
            self.draw_survivor(self.josephus.survivor + 1)

    def step(self):
        victim = self.josephus.kill()
        self.graph.erase()
        self.draw()
        return victim is None

    def run(self):
        finished = False
        while True:
            event, values = self.window.read(timeout=1000 if not finished else None)
            if not finished:
                finished = self.step()
            if event == sg.WIN_CLOSED:
                break

    def __enter__(self):
        self.run()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.window.close()
