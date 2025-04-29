### NFR DAQ Interface Main Program ###
from startup import DAQInterface


"""
App Features

- architecture
  - matplotlib (graphs) and customtkinter (GUI)
- custom windows
  - how to accomplish? Anthony
- displaying graphs
- data storage
- live data (feedback says we will wait on this)

"""

if __name__ == "__main__":
    app = DAQInterface()
    app.mainloop()