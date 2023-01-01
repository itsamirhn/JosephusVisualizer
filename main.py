from models import Josephus, JosephusVisualizer, NumberInputVisualizer


def main():
    with NumberInputVisualizer('Enter Number of soldiers', 'Nex') as count:
        pass
    with NumberInputVisualizer('Enter Step', 'Next') as step:
        pass
    josephus = Josephus(count, step)
    visualizer = JosephusVisualizer(josephus)
    with visualizer:
        pass


if __name__ == '__main__':
    main()
