from prisoners.models.compare import PrisonersCompare
from prisoners.models.merge import PrisonersMerged
from prisoners.models.original import Gedetineerde
from prisoners import db


class TableMerge:
    def __init__(self):
        for id_gedetineerde in self.get_all_ids():
            # Check whether it is in PrisonersCompare
            in_compare = PrisonersCompare.query.filter(PrisonersCompare.id_gedetineerde == id_gedetineerde).first()
            if in_compare:
                # It is
                pass
            else:
                # It isn't
                #             id_gedetineerde = db.Column(db.Integer, db.ForeignKey(Gedetineerde.Id_gedetineerde))
                # naam = db.Column(db.String(255), index=True)
                # voornaam = db.Column(db.String(255), index=True)
                # geboorteplaats = db.Column(db.String(255), index=True)
                # geboorteplaats_nis = db.Column(db.String(255), index=True)
                # geslacht = db.Column(db.String(32))
                # misdrijf = db.Column(db.String(255))
                # woonplaats = db.Column(db.String(255))
                # woonplaats_nis = db.Column(db.String(255))
                # beroep = db.Column(db.String(255))
                # leeftijd = db.Column(db.String(255))
                # geboortejaar = db.Column(db.String(255))
                # lichaamslengte = db.Column(db.String(255))
                # flag = db.Column(db.Boolean, default=False)
                db_gedetineerde = Gedetineerde.query.filter(Gedetineerde.Id_gedetineerde == id_gedetineerde).first()
                db_prisoner = PrisonersMerged()
                db_prisoner.id_gedetineerde = db_gedetineerde.Id_gedetineerde
                db_prisoner.naam = db_gedetineerde.Naam
                db_prisoner.voornaam = db_gedetineerde.Voornaam
                db_prisoner.geboorteplaats = db_gedetineerde.Verblijf.first().Geboorteplaats.first().Plaatsnaam_vertaling
                db_prisoner.geboorteplaats_nis = db_gedetineerde.Verblijf.first().Geboorteplaats.first().Plaatsnaam_NIS
                db_prisoner.geslacht = db_gedetineerde.Geslacht
                db_prisoner.misdrijf = db_gedetineerde.Verblijf.first().Misdrijf.first().Misdrijf_vertaling
                db_prisoner.woonplaats = db_gedetineerde.Verblijf.first().Woonplaats.first().Plaatsnaam_vertaling
                db_prisoner.woonplaats_nis = db_gedetineerde.Verblijf.first().Woonplaats.first().Plaatsnaam_NIS
                db_prisoner.beroep = db_gedetineerde.Verblijf.first().Beroep.first().Beroep_vertaling
                db_prisoner.leeftijd = db_gedetineerde.Verblijf.first().Leeftijd
                db_prisoner.geboortejaar = self.make_year_of_birth(db_gedetineerde)
                db_prisoner.lichaamslengte = db_gedetineerde.Verblijf.first().Lichaamslengte_m
                db.session.add(db_prisoner)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    def get_all_ids(self):
        return db.session.query(Gedetineerde.Id_gedetineerde).all()
    
    def make_year_of_birth(self, input_gedetineerde):
        year_of_inscr = input_gedetineerde.Verblijf.first().Inschrijvingsdatum_j
        age_at_inscr = input_gedetineerde.Verblijf.first().Leeftijd
        return year_of_inscr - age_at_inscr

    #20 & 50

    def get_height_closest_to(self, o_c_prisoner, to_age):
        """
        Get the height closes to to_age (e.g. 35) from a prisoners that originally
        came from PrisonerCompare and has matches
        :param o_c_prisoner:
        :param to_age:
        :return:
        """
        l_to_compare = []
        # Get "gedetineerde" object we need to get Leeftijd
        for match in o_c_prisoner.matches:
            l_to_compare.append({
                'age_diff': abs(to_age - match.Gedetineerde.first().Verblijf.first().Leeftijd),
                'height': match.Gedetineerde.first().Verblijf.first().Lichaamslengte_m
            })
        # Sort
        if len(l_to_compare) > 0:
            l_dist = sorted(l_to_compare, key=lambda prisoner: prisoner['age_diff'])
            return l_dist[0]['height']
        else:
            print('No matches.')
            return o_c_prisoner.Gedetineerde.first().Verblijf.first().Lichaamslengte_m
