import back.back as back


def main():
    g = back.Game(10)
    g.start()
    print(g)

    g.play()

    print(g)
    state = g.get_state()


if __name__ == "__main__":
    main()
