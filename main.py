from models import Josephus, JosephusVisualizer


def main():
    n = int(input("Enter the number of people: "))
    josephus = Josephus(n)
    visualizer = JosephusVisualizer(josephus)
    with visualizer:
        pass


if __name__ == '__main__':
    main()
