"""
### STARSTUFF INIT ###

To Galahir950 / Ryan, a creator
# MEMENTO MORI ERGO FABRICATO #

"""
#print("  Loading StarStuff...")
from . import celestial, vehicle, weaponry, world

__all__ = ["generate"]

def genSol():
    sol = celestial.System("Sol")
    s = celestial.Star("the Sun", sol, radius=695700)
    s.color = "#fc8"
    #s = celestial.BlackHole("Gargantua", sol, mass=1, radius=695700)
    #s.color = "#111111"

    p = celestial.Planet("Mercury", sol, orbit=87.969, radius=2439.7)
    p.color = "#aaaaaa"

    p = celestial.Planet("Venus", sol, orbit=224.701, radius=6051.8)
    p.color = "#efefe8"

    p = celestial.Planet("Earth", sol, orbit=365, radius=6371)
    p.color = "#6ad"
    m = celestial.DwarfPlanet("Luna", p, orbit=28, radius=1737.1)
    m.color = "#aaa"

    p = celestial.Planet("Mars", sol, orbit=686.971, radius=3389.5)
    p.color = "#cc734c"

    #m = celestial.Belt("Inner Belt", sol, composition={"rock":50.0,"dust":50.0})
    #c = celestial.DwarfPlanet("Ceres", m)
    #c = celestial.Minor("Vesta", m)
    #c = celestial.Minor("Pallas", m)

    p = celestial.GiantPlanet("Jupiter", sol, orbit=4332.59, radius=69911)
    p.composition = "Gas"
    p.color = "#b89776"

    p = celestial.GiantPlanet("Saturn", sol, orbit=10759.22, radius=58232)
    p.composition = "Gas"
    p.color = "#f2dea9"
    #m = celestial.Belt("Rings of Saturn", p, composition={"ice":95.0,"rock":5.0})

    p = celestial.GiantPlanet("Caelus", sol, orbit=30688.5, radius=25362)
    p.composition = "Ice"
    p.color = "#9fb0c6"

    p = celestial.GiantPlanet("Neptune", sol, orbit=60182, radius=24622)
    p.composition = "Ice"
    p.color = "#5279cc"

    #m = celestial.Belt("Kuiper Belt", sol, composition={"ice":80.0,"rock":20.0})
    #p = celestial.DwarfPlanet("Pluto", m)
    #p.composition = "Ice"

    return sol

def genBC():
    bc = celestial.System("Beta Cygni")
    s1 = celestial.Star("Albireo A")
    s2 = celestial.Star("Albireo B")

    g = celestial.GiantPlanet("Beta Cygni I", bc)
    g.composition = "Ice"

    g = celestial.GiantPlanet("Beta Cygni II", bc)
    g.composition = "Gas"
    p = celestial.Planet("Beta Cygni IIa", g)
    p = celestial.DwarfPlanet("Beta Cygni IIb", g)
    p.composition = "Ice"

    return bc

def generate():
    mw = celestial.Galaxy("Milky Way")
    mw.subAssign(genSol())
    #mw.subAssign(genBC())
    return mw.orbitals[0]

#class Generator:



#print("   StarStuff Initialized")
