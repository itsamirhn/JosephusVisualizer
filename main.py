from gui import JosephusWindow


def main():
    n = int(input("Enter the number of people: "))
    window = JosephusWindow(n)
    with window:
        pass


if __name__ == '__main__':
    main()
