from globalmanager import GlobalManager

# creating a single instance of the globalmanager in here that everything can pull from
# created the global manager so it's easier in the future the avoid race conditions accessing global vars
globalmanager = GlobalManager()