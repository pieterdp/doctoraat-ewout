from sqlalchemy import and_
from prisoners.models.original import Gedetineerde
from prisoners.models.original import Verblijf, Geboorteplaats
from prisoners.models.compare import PrisonersCompare
from prisoners import db


class Matcher:
    """
    For every item a in db.Gedetineerde; do the following:
    Get all Gedetineerde g for which g.Geboorteplaats = a.Geboorteplaats
    For all g, do:
        c = new PrisonersCompare(a, g)
        c.l_score()
    """

    def __init__(self):
        prisoners = Gedetineerde.query.all()
        for prisoner in prisoners:
            same_birth_place = self.get_same_place_of_birth(prisoner)
            for pr_same_birth in same_birth_place:
                p_compare = PrisonersCompare(prisoner.Id_gedetineerde, prisoner.Voornaam, prisoner.Naam,
                                             prisoner.Verblijf.first().Geboorteplaats.first().Plaatsnaam_vertaling,
                                             pr_same_birth.Id_gedetineerde,
                                             pr_same_birth.Voornaam, pr_same_birth.Naam,
                                             pr_same_birth.Verblijf.first().Geboorteplaats.first().Plaatsnaam_vertaling,
                                             prisoner.Geboortejaar,
                                             prisoner.Geboortemaand,
                                             prisoner.Geboortedag, pr_same_birth.Geboortejaar,
                                             pr_same_birth.Geboortemaand,
                                             pr_same_birth.Geboortedag)
                p_compare.c_l_score()
                db.session.add(p_compare)
                db.session.commit()

    def get_same_place_of_birth(self, or_prisoner):
        same_birth = Gedetineerde.query.filter(and_(
            Geboorteplaats.Plaatsnaam_vertaling == or_prisoner.Verblijf.first().Geboorteplaats.first().Plaatsnaam_vertaling,
            Geboorteplaats.Id_verbl == Verblijf.Id_verblijf,
            Verblijf.Id_ged == Gedetineerde.Id_gedetineerde,
            Gedetineerde.Id_gedetineerde != or_prisoner.Id_gedetineerde)).all()
        return same_birth
