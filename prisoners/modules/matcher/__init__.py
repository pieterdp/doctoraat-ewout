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
            try:
                same_birth_place = self.get_same_place_of_birth(prisoner)
            except AttributeError as e:
                print(e)
                continue
            year_of_birth = self.make_year_of_birth(prisoner)
            in_pc = PrisonersCompare.query.filter(PrisonersCompare.id_gedetineerde == prisoner.Id_gedetineerde).first()
            if not in_pc:
                print('Matching {0}.'.format(prisoner))
                for pr_same_birth in same_birth_place:
                    # Try to reduce the pool of candidates by only selecting prisoners for which the difference
                    # between their years of births is less than 5
                    same_birth_yofb = self.make_year_of_birth(pr_same_birth)
                    yofb_diff = year_of_birth - same_birth_yofb
                    if abs(yofb_diff) <= 5:
                        if not self.check(prisoner.Id_gedetineerde, pr_same_birth.Id_gedetineerde):
                            try:
                                p_compare = PrisonersCompare(prisoner.Id_gedetineerde, prisoner.Voornaam, prisoner.Naam,
                                                             prisoner.Verblijf.first().Geboorteplaats.first().Plaatsnaam_vertaling,
                                                             pr_same_birth.Id_gedetineerde,
                                                             pr_same_birth.Voornaam, pr_same_birth.Naam,
                                                             pr_same_birth.Verblijf.first().Geboorteplaats.first().Plaatsnaam_vertaling,
                                                             self.make_year_of_birth(prisoner),
                                                             prisoner.Geboortemaand,
                                                             prisoner.Geboortedag, self.make_year_of_birth(pr_same_birth),
                                                             pr_same_birth.Geboortemaand,
                                                             pr_same_birth.Geboortedag)
                                p_compare.c_l_score()
                                db.session.add(p_compare)
                                db.session.commit()
                            except AttributeError as e:
                                print(e)
                                continue
            else:
                print('{0} already in database.'.format(prisoner))

    def check(self, id_master, id_slave):
        exists = PrisonersCompare.query.filter(and_(PrisonersCompare.id_gedetineerde == id_master,
                                                    PrisonersCompare.c_id_gedetineerde == id_slave)).first()
        if exists:
            return True
        else:
            return False

    def get_same_place_of_birth(self, or_prisoner):
        same_birth = Gedetineerde.query.filter(and_(
            Geboorteplaats.Plaatsnaam_vertaling == or_prisoner.Verblijf.first().Geboorteplaats.first().
            Plaatsnaam_vertaling,
            Geboorteplaats.Id_verbl == Verblijf.Id_verblijf,
            Verblijf.Id_ged == Gedetineerde.Id_gedetineerde,
            Gedetineerde.Id_gedetineerde != or_prisoner.Id_gedetineerde)).all()
        return same_birth

    def make_year_of_birth(self, prisoner):
        o_verblijf = prisoner.Verblijf.first()
        year_of_birth = o_verblijf.Inschrijvingsdatum_j - o_verblijf.Leeftijd
        return year_of_birth
