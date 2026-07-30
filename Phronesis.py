import tkinter as tk

from windows.splash import SplashScreen
from startup import Startup
from windows.dashboard import Dashboard

root = tk.Tk()

splash = SplashScreen(root)

startup = Startup(splash)
startup.run()

Dashboard(root)

splash.close()

root.mainloop()