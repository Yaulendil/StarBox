import collections
import astropy
from astropy import constants as c
from astropy import units as u

#__all__ = ["Planet","Star","System"]

"""
/starbox/celestial.py

Class module for:
    Celestial bodies: Stars, black holes, planets, etc.
    Locations on and around bodies: Settlements, elevators, stations, etc.
    Celestial structures composed of bodies: Star systems, sectors, galaxies, etc.


bodyRank: Hierarchy of mass of celestials
    0: Universal center (Great Attractor)
    1: Galactic center (SMBH, quasar)
    2: Galactic child (BH, star, IS vessel)
    3: Stellar child (Planet, belt, IP vessel)
    4: Planetary child (Moon, belt, orbital vessel)
    5: Planetary grandchild (Orbital vessel around a moon)

"""

# Lookup tables for scale conversions
mInUnit = {"mm":0.001,"m":1,"km":1000}
gInUnit = {"mg":0.001,"g":1,"kg":1000,
           "massEarth":5.9722e27,
           "massJovian":1.89813e30,
           "massSolar":1.98847e33}

def convertMass(q1, u1, u2):
    if u1 == u2:
        return q1
    else:
        q0 = q1*gInUnit[u1]
        q2 = q0/gInUnit[u2]
        return q2

def findLargestProportion(din,flavor=False):
    dsort = [(k, din[k]) for k in sorted(din, key=din.get, reverse=True)]
    return dsort[0][0]


class Body:
    """
    Superclass for all natural celestial objects
    """
    def __init__(self, name, # Identity information
                 mass=1, # Physical information
                 ruler=None, space=None): # Social information
        self.name = name
        self.orbitals = [] # Natural bodies orbiting this body; Moons, rings, etc.
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station

        # Physical characteristics
        self.mass = mass # Mass of the planet

        # Positional characteristics
        self.posPhi = None # Position of the body relative to its parent
        self.posRho = None # Distance from the body to its parent body

        self.ruler = ruler
        self.sites = [] # Locations on the surface of the world, synthetic or geographical
        self.nations = [] # Entities controlling territory on this world (typically subservient to the ruler)

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def subAssign(self, childNew):
        try:
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
            if self.system() != None:
                self.system().subAssign(childNew)
        except AttributeError:
            return




class Planet(Body):
    """
    Planet: Most ubiquitous celestial body
    name, str: Common designation
    parent, obj: The object around which this body orbits; If None, planet is Rogue
    composition, str: Type of planet (Rock, ice, gas).
    ruler, obj: The governing entity, if any, with total control over this body
    """
    bodyType = "Planet"
    bodySubtype = "Planet"
    massUnit = "massEarth"

    def __init__(self, name, parent=None, # Identity information
                 composition="Rock", # Physical information
                 ruler=None, space=None, dayLength=24): # Social information
        super().__init__(name, ruler, space)
        #self.name = name
        self.parent = parent
        self.composition = composition
        self.orbitals = [] # Natural bodies orbiting this body; Typically another planet
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station

        # Physical characteristics
        self.radius = None # Distance from the center to the surface
        self.Gravity = 1 # Strength of surface gravity, relative to Earth

        # Temporal characteristics
        self.periodRotation = dayLength # Number of hours taken to rotate
        self.periodOrbital = None # Number of hours in a year

        self.bodyRank = 3
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def __str__(self):
        oput = '"{}": {} {}'.format(self.name, self.composition, self.bodySubtype.lower())
        system = self.system()
        if system != None:
            oput = oput + " in the {} system".format(system.name)
        if self.ruler != self.parent.ruler:
            oput = oput + ", under the control of {}".format(self.ruler)
        if self.orbitals != []:
            oput = oput + "\n -Has the following moons:"
            for moon in self.orbitals:
                oput = oput + "\n -- " + moon.__str__()
        return oput


class GiantPlanet(Planet):
    bodySubtype = "Giant"
    massUnit = "massJovian"


class DwarfPlanet(Planet):
    bodySubtype = "Dwarf"


class Star:
    """
    Star: Standard, very bright, celestial body; Core of most Systems
    """
    bodyType = "Star"
    bodySubtype = "Star"
    massUnit = "massSolar"

    def __init__(self, name, parent=None, # Identity information
                 mass=1, stellarClass="D", subtype="Main Sequence", # Physical information
                 ruler=None, space=None): # Social information
        self.name = name # STR: Common designation
        self.parent = parent # OBJ: Object around which this body orbits
        self.mass = mass # FLOAT: Mass of the star, given in Solar Masses
        self.stellarClass = stellarClass
        self.stellarSubtype = subtype
        self.ruler = ruler
        self.orbitals = [] # Natural bodies orbiting this body; Typically planets and belts
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station
        self.bodyRank = 2
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def subsList(self):
        oput = "{}: {}".format(self.bodySubtype, self.name)
        n = 0
        try:
            oput = oput + "\nParent: [{}] {} ({})".format(n, self.parent.name, self.parent.bodySubtype)
            n += 1
        except AttributeError:
            pass
        oput = oput + "\n    Orbitals:"
        for subloc in self.orbitals:
            oput = oput + "\n   :[\033[96m{}\033[0m]: {} ({})".format(n, subloc.name, subloc.bodySubtype)
            n += 1
        oput = oput + "\n    Satellites:"
        for subloc in self.satellites:
            oput = oput + "\n   :[{}]: {} ({})".format(n, subloc.name, subloc.bodySubtype)
            n += 1
        return oput

    def subAssign(self, childNew):
        try:
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
            if self.parent.bodyType == "System":
                self.parent.subAssign(childNew)
        except AttributeError:
            return


class BlackHole(Star):
    bodySubtype = "Black Hole"


class System:
    """
    System: Standard designation for a grouping of bodies, typically headed by one or more stars
    """
    bodyType = "System"
    bodySubtype = "System"

    def __init__(self, name, parent=None, # Identity information
                 posPhi=0, posRho=0, mapCoords="", # Physical information
                 ruler=None, space=None, rank=2): # Social information
        self.name = name # STR: Common designation
        self.parent = parent # OBJ: Object around which this body orbits
        self.posPhi = posPhi
        self.posRho = posRho
        self.mapCoords = mapCoords
        self.heads = [] # Massive objects at the core of the system; Typically stars
        self.bodies = [] # Objects directly orbiting the system core; Typically planets

        self.ruler = ruler

        self.bodyRank = rank
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def system(self):
        return self

    def subsList(self):
        oput = "{}: {}".format(self.bodySubtype, self.name)
        oput = oput + "\n    Core:"
        for subloc in self.heads:
            oput = oput + "\n    --{} ({})".format(subloc.name, subloc.bodySubtype)
        oput = oput + "\n    Orbitals:"
        for subloc in self.bodies:
            oput = oput + "\n    --{} ({})".format(subloc.name, subloc.bodySubtype)
        return oput

    def subAssign(self, childNew):
        try:
            if childNew.bodyRank > self.bodyRank:
                self.bodies.append(childNew)
            elif childNew.bodyRank == self.bodyRank:
                self.heads.append(childNew)
        except AttributeError:
            pass

    def __dict__(self):
        return {"heads" : self.heads, "bodies" : self.bodies}

## ## ## ## ## ## ## ##
## ## MINOR TYPES ## ##
## ## ## ## ## ## ## ##

class Belt:
    """
    Belt: A region of debris in orbit around a body, forming a ring
    """
    bodyType = "Belt"

    def __init__(self, name, parent=None, # Identity information
                 posRho=0, composition={"rock":100.0}, # Physical information
                 ruler=None, space=None, rank=3): # Social information
        self.name = name # STR: Common designation
        self.parent = parent # OBJ: Object around which this body orbits
        self.posRho = posRho
        self.composition = composition
        self.orbitals = []

        self.ruler = ruler

        self.bodyRank = rank
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

        if self.parent.bodyType == "Star":
            self.bodySubtype = "Belt"
        elif self.parent.bodyType == "Planet":
            self.bodySubtype = "Ring"
        else:
            self.bodySubtype = "Cloud"

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def comp(self): # Calculate what the belt is "made of"
        return findLargestProportion(self.composition,True)

    def subAssign(self, childNew):
        try:
            self.orbitals.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
            if self.parent.bodyType == "System":
                self.parent.subAssign(childNew)
        except AttributeError:
            pass

    def __str__(self):
        oput = '"{}": A {} of {} around {}'.format(self.name, self.bodyType.lower(), self.comp().lower(), self.parent.name)
        system = self.system()
        #if system != None:
            #oput = oput + " in the {} system".format(system.name)
        if self.ruler != self.parent.ruler:
            oput = oput + ", under the control of {}".format(self.ruler)
        if self.orbitals != []:
            oput = oput + "\n -Contains the following notable bodies:"
            for moon in self.orbitals:
                oput = oput + "\n -- " + moon.__str__()
        return oput


class Minor:
    """
    Minor: An object too small to be gravitationally spherical
    Asteroids, meteors, comets, etc.
    """
    def __init__(self, name, parent=None, # Identity information
                 composition="rock", # Physical information
                 ruler=None, space=None): # Social information
        self.name = name
        self.parent = parent
        self.composition = composition
        self.satellites = [] # Synthetic structures orbiting this body; Typically a station

        # Physical characteristics
        self.mass = None # Mass of the planet
        self.massUnit = "kg"
        self.radius = None # Distance from the center to the surface

        # Positional characteristics
        self.posPhi = None # Position of the planet relative to its parent
        self.posRho = None # Distance from the planet to its parent body

        self.ruler = ruler
        self.sites = [] # Locations on the surface of the world, synthetic or geographical
        self.nations = [] # Entities controlling territory on this world (typically subservient to the ruler)

        self.bodyRank = 4
        try:
            self.parent.subAssign(self) # If the parent body has a specific method to integrate me, use it
        except AttributeError:
            pass

    def system(self):
        try:
            return self.parent.system()
        except AttributeError:
            return None

    def subAssign(self, childNew):
        try:
            self.append(childNew)
            childNew.parent = self
            childNew.bodyRank = self.bodyRank + 1
            if self.system() != None:
                self.system().subAssign(childNew)
        except AttributeError:
            return














