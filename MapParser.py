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
#                 Right T - Junctions (rtjunction)
#
#                     Street 1 ---O--- Street 2
#                                 |
#                              Street 3
#
#                 Left T - Junctions (ltjunction)
#
#                              Street 1
#                                 |
#                     Street 2 ---O--- Street 3
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

class object:
    "A junction or feature."
    def __init__(self, type, connected):
        self.type = type
        self.connect = connected
    def getinstruction(self, inroad, outroad):
        if self.type == "streetswitch":
            return "Continue onto renamed road " + outroad
        elif self.type == "rtjunction":
            if inroad == self.connect[0]:
                if outroad == self.connect[1]:
                    return "Continue ahead onto " + outroad
                else:
                    return "Turn right onto " + outroad
            elif inroad == self.connect[1]:
                if outroad == self.connect[0]:
                    return "Continue ahead onto " + outroad
                else:
                    return "Turn left onto " + outroad
            else:
                if outroad == self.connect[0]:
                    return "Turn left onto " + outroad
                else:
                    return "Turn right onto " + outroad
        elif self.type == "ltjunction":
            if inroad == self.connect[0]:
                if outroad == self.connect[1]:
                    return "Turn right onto " + outroad
                else:
                    return "Turn left onto " + outroad
            elif inroad == self.connect[1]:
                if outroad == self.connect[0]:
                    return "Turn left onto " + outroad
                else:
                    return "Continue ahead onto " + outroad
            else:
                if outroad == self.connect[0]:
                    return "Turn right onto " + outroad
                else:
                    return "Continue ahead onto " + outroad
        elif self.type == "xjunction":
            if inroad == self.connect[0]:
                if outroad == self.connect[1]:
                    return "Turn right onto " + outroad
                elif outroad == self.connect[2]:
                    return "Turn left onto " + outroad
                else:
                    return "Continue ahead onto " + outroad
            elif inroad == self.connect[1]:
                if outroad == self.connect[0]:
                    return "Turn left onto " + outroad
                elif outroad == self.connect[2]:
                    return "Continue ahead onto " + outroad
                else:
                    return "Turn right onto " + outroad
            elif inroad == self.connect[2]:
                if outroad == self.connect[0]:
                    return "Turn right onto " + outroad
                elif outroad == self.connect[1]:
                    return "Continue ahead onto " + outroad
                else:
                    return "Turn left onto " + outroad
            else:
                if outroad == self.connect[0]:
                    return "Continue ahead onto " + outroad
                elif outroad == self.connect[1]:
                    return "Turn left onto " + outroad
                else:
                    return "Turn right onto " + outroad
        elif self.type == "roundabout":
            i = self.connect.index(inroad)
            e = 0
            while not self.connect[i] == outroad:
                e += 1
                i += 1
                if i == len(self.connect):
                    i = 0
            return "Enter roundabout and take exit " + e
        elif self.type == "motorjunction":
            return "Exit left onto " + outroad
        else:
            return "Cross the level crossing onto " + outroad

class road:
    "A single road."
    def __init__(self, name, type, objects):
        self.name = name
        self.type = type
        self.objects = objects

class navamap:
    "An entire map."
    def __init__(self, file):
        self.file = file
        if os.path.exists(file):
            self.data = getdata(self.file)
        else:
            self.data = [dict(), list()]
    def addroad(self, name, roadtype, connected):
        "Creates a street entry."
        self.data[0][name] = [connected, roadtype]
        savedata(self.file, self.data)
    def addobject(self, connected, objecttype):
        "Creates a junction or feature entry."
        self.data[1].append([connected, objecttype])
        savedata(self.file, self.data)
    def getroaddata(self, name):
        "Returns a road instance of the name specified."
        objects = list()
        for id in self.data[0][name][0]:
            objects += self.getobjectdata(id)
        return road(name, self.data[0][name][1], objects)
    def getobjectdata(self, id):
        "Returns an object instance of the id specified."
        return object(self.data[1][id][0], self.data[1][id][1])
