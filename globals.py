from globalmanager import GlobalManager

# creating a single instance of the globalmanager in here that everything can pull from
# there honestly seems like there's no good way for truly global variables in Python across modules
# the poison I picked was using a dict, wrapped in a class rather than properties which felt wrong
globalmanager = GlobalManager()