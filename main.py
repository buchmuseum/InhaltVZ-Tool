from infrastructure.logging_config import setup_logging

import tkinter as tk

from gui.main_window import MainWindow



def main():

    setup_logging()


    root = tk.Tk()


    app = MainWindow(
        root
    )


    root.mainloop()



if __name__ == "__main__":

    main()