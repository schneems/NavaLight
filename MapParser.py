import ast
import os.path

def getdata(file):
    "Reads data from a file."
    with open(file) as f:
        return ast.literal_eval(f.read())
def savedata(file, data):
    "Writes data to a file."
    with open(file, "w") as f:
        f.write(str(data))

# Map data is structured as follows:
#
# An entire map consists of a single list.
#     The first item is a dictionary. It contains streets. The street name is the key.
#         Within each street, there is a list.
#             The first item of the list is a list. In it there are list indices for the junctions and objects it is connected to.
#             The second item is what type of road this is. It can be:
#                 Track (track)
#                     Small tracks.
#                 Lane (lane)
#                     Roads that are only wide enough for one vehicle.
#                 Lane with passing places (passlane)
#                     Roads that are only wide enough for one vehicle, however with places for vehicles to pass each other.
#                 Cul-de-sac (culdesac)
#                     T - shaped roads with no through passage.
#                 Circle roads (circle)
#                     Circlular roads that join onto themselves. These usually have only one or two ways in, but can have more.
#                 Road (road)
#                     Normal roads.
#                 B Roads (b)
#                     B roads, such as B1.
#                 A Roads (a)
#                     A roads, such as A1.
#                 A Roads with M (am)
#                     A roads with M after them, such as A1 (M).
#                 Motorways (motor)
#                     Motorways, such as M1.
#     The second item is a list. It contains junctions, roundabouts and other things such as level crossings. These must be in order, but can start from either end of the road.
#         Each item in this list has another list inside it.
#             The first item of the list is a list which contains all the streets it is connected to, in the order highlighted in the diagrams below.
#             The second item is what type of object this is. They can be:
#                 Street name switches (streetswitch)
#
#                     Street 1 ---O--- Street 2
#
#                 T - Junctions (tjunction)
#
#                     Street 1 ---O--- Street 2
#                                 |
#                              Street 3
#
#                 X - Junctions (xjunction)
#
#                              Street 1
#                                 |
#                     Street 2 ---O--- Street 3
#                                 |
#                              Street 4
#
#                 Roundabouts (roundabout)
#
#                     These depend on the number of streets. The streets are listed in clockwise order, starting anywhere around the roundabout.
#
#                 Motorway junctions (motorjunction)
#
#                     Street 1   |
#                         \      |
#                          \     |
#                           \    |
#                            \   |
#                             \  |
#                              \ |
#                               \|
#                                |
#                             Street 2
#
#                     Also, the junction number is the third value.
#
#                 Level crossings (traincrossing)
#
#                     Street 1 --|-|-- Street 2

class navamap:
    def __init__(self, file):
        self.file = file
        if os.path.exists(file):
            self.data = getdata(self.file)
        else:
            self.data = [dict(), list()]
    def addroad(self, name, roadtype, connected=list()):
        "Creates a street entry."
        self.data[0][name] = [connected, roadtype]
        savedata(self.file, self.data)
    def addobject(self, connected, objecttype):
        "Creates a junction or feature entry."
        self.data[1].append([connected, objecttype])
        savedata(self.file, self.data)
