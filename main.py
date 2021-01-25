from App import *


# Will return a list of profiles found in the profiles directory (and make one if it doesn't exist)
def get_profiles():
    try:
        os.mkdir("profiles")
    except FileExistsError:
        print("profiles found:" + str(os.listdir("profiles")))
    return os.listdir("profiles")


def run():
    app = App()
    app.show_select_profile(get_profiles())
    app.mainloop()


if __name__ == '__main__':
    run()
