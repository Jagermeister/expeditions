"""Entry point"""
from view import viewfactory as vf
from model.main import GamesManager

def main():
    """simple game loop to link a view with our model logic"""
    model = GamesManager()
    view = vf.factory_create()
    view.init(model)
    while 1:
        view.handle_events()
        view.update()
        view.display()
    view.quit()

if __name__ == '__main__':
    main()