from prisoners.models.brugge import PrisonersMatchBrugge, GedetineerdeBrugge, GeboorteplaatsBrugge, VerblijfBrugge
from prisoners.models.compare import PrisonersMatch
from prisoners.models.original import Gedetineerde, Geboorteplaats, Verblijf


class RecidiveGet:
    """
    From both the *Brugge and the *Gent PrisonersMatch tables, get the list
    of matched prisoners. Those prisoners have been repeatedly incarcerated
    and are thus recidivists. We need the following information (both from the
    master and the slave): naam, voornaam, geboorteplaats, inschrijvingsjaar,
    leeftijd bij inschrijven, lengte bij inschrijven.
    We return a dictionary:
    {
        id_master,
        master_naam,
        master_voornaam,
        master_geboorteplaats,
        master_inschrijvingsjaar,
        master_leeftijd,
        master_lengte,
        slaves: [
            {
                slave_id,
                slave_inschrijvingsjaar,
                slave_leeftijd,
                slave_lengte
            }
        ]
    }
    We repeat slave for every slave.
    Linking is by id_gedetineerde
    """
    def __init__(self):
        pass
