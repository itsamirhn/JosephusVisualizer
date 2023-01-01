from models import Josephus, JosephusVisualizer


def main():
    n = int(input("Enter number of people: "))
    k = int(input("Enter step: "))
    josephus = Josephus(n, k)
    visualizer = JosephusVisualizer(josephus)
    with visualizer:
        pass


if __name__ == '__main__':
    main()
