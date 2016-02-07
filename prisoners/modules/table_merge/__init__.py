from sqlalchemy import and_
from prisoners.models.compare import PrisonersCompare, prisonersmatch
from prisoners.models.merge import PrisonersMerged
from prisoners.models.original import Gedetineerde, Verblijf
from prisoners import db


class TableMerge:
    def __init__(self):
        self.age_to = 35
        for id_gedetineerde in self.get_all_ids():
            # Check whether it is in PrisonersCompare
            in_compare = db.session.query(prisonersmatch).filter(
                prisonersmatch.c.mast_id_ged == id_gedetineerde).first()
            # in_compare = PrisonersCompare.query.filter(PrisonersCompare.id_gedetineerde == id_gedetineerde).first()
            if in_compare:
                # It is
                db_pris_compare = PrisonersCompare.query. \
                    filter(PrisonersCompare.id_gedetineerde == in_compare.c.mast_id_ged).first()
                db_gedetineerde = db_pris_compare.Gedetineerde.first()
                db_verblijf = db_gedetineerde.Verblijf.first()
                db_geboorteplaats = db_verblijf.Geboorteplaats.first()
                db_misdrijf = db_verblijf.Misdrijf.first()
                db_woonplaats = db_verblijf.Woonplaats.first()
                db_prisoner = PrisonersMerged()
                db_prisoner.id_gedetineerde = db_gedetineerde.Id_gedetineerde
                db_prisoner.naam = db_gedetineerde.Naam
                db_prisoner.voornaam = db_gedetineerde.Voornaam
                db_prisoner.geboorteplaats = db_geboorteplaats.Plaatsnaam_vertaling
                db_prisoner.geboorteplaats_nis = db_geboorteplaats.Plaatsnaam_NIS
                db_prisoner.geslacht = db_gedetineerde.Geslacht
                db_prisoner.misdrijf = db_misdrijf.Misdrijf_vertaling
                db_prisoner.woonplaats = db_woonplaats.Plaatsnaam_vertaling
                db_prisoner.woonplaats_nis = db_woonplaats.Plaatsnaam_NIS
                db_prisoner.beroep = self.get_occupation_closest_to(db_pris_compare, self.age_to)
                # db_prisoner.leeftijd = db_pris_compare.Gedetineerde.first().Verblijf.first().Leeftijd
                db_prisoner.leeftijd = self.get_height_closest_to(db_pris_compare, self.age_to)
                db_prisoner.geboortejaar = self.make_year_of_birth(db_pris_compare.Gedetineerde.first())
                db_prisoner.lichaamslengte = db_verblijf.Lichaamslengte_m
                db.session.add(db_prisoner)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
            else:
                # It isn't
                # Check whether it has been matched (we skip those as well)
                has_been_checked = db.session.query(prisonersmatch).filter(
                    prisonersmatch.c.slave_id_ged == id_gedetineerde).first()
                if not has_been_checked:
                    db_gedetineerde = Gedetineerde.query.filter(Gedetineerde.Id_gedetineerde == id_gedetineerde).first()
                    db_verblijf = db_gedetineerde.Verblijf.first()
                    db_geboorteplaats = db_verblijf.Geboorteplaats.first()
                    db_misdrijf = db_verblijf.Misdrijf.first()
                    db_woonplaats = db_verblijf.Woonplaats.first()
                    db_beroep = db_verblijf.Beroep.first()
                    db_prisoner = PrisonersMerged()
                    db_prisoner.id_gedetineerde = db_gedetineerde.Id_gedetineerde
                    db_prisoner.naam = db_gedetineerde.Naam
                    db_prisoner.voornaam = db_gedetineerde.Voornaam
                    db_prisoner.geboorteplaats = db_geboorteplaats.Plaatsnaam_vertaling
                    db_prisoner.geboorteplaats_nis = db_geboorteplaats.Plaatsnaam_NIS
                    db_prisoner.geslacht = db_gedetineerde.Geslacht
                    db_prisoner.misdrijf = db_misdrijf.Misdrijf_vertaling
                    db_prisoner.woonplaats = db_woonplaats.Plaatsnaam_vertaling
                    db_prisoner.woonplaats_nis = db_woonplaats.Plaatsnaam_NIS
                    db_prisoner.beroep = db_beroep.Beroep_vertaling
                    db_prisoner.leeftijd = db_verblijf.Leeftijd
                    db_prisoner.geboortejaar = self.make_year_of_birth(db_gedetineerde)
                    db_prisoner.lichaamslengte = db_verblijf.Lichaamslengte_m
                    db.session.add(db_prisoner)
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(e)

    def get_all_ids(self):
        return db.session.query(Gedetineerde.Id_gedetineerde).filter(and_(Gedetineerde.Id_gedetineerde == Verblijf.Id_ged,
                                                                          Verblijf.Leeftijd >= 20,
                                                                          Verblijf.Leeftijd <= 50)).all()

    def make_year_of_birth(self, input_gedetineerde):
        year_of_inscr = input_gedetineerde.Verblijf.first().Inschrijvingsdatum_j
        age_at_inscr = input_gedetineerde.Verblijf.first().Leeftijd
        return year_of_inscr - age_at_inscr

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
        # Add the information from o_c_prisoner as well
        l_to_compare.append({
            'age_diff': abs(to_age - o_c_prisoner.Gedetineerde.first().Verblijf.first().Leeftijd),
            'height': o_c_prisoner.Gedetineerde.first().Verblijf.first().Lichaamslengte_m
        })
        # Sort
        if len(l_to_compare) > 0:
            l_dist = sorted(l_to_compare, key=lambda prisoner: prisoner['age_diff'])
            return l_dist[0]['height']
        else:
            print('No matches.')
            return o_c_prisoner.Gedetineerde.first().Verblijf.first().Lichaamslengte_m

    def get_occupation_closest_to(self, o_c_prisoner, to_age):
        l_to_compare = []
        for match in o_c_prisoner.matches:
            l_to_compare.append({
                'age_diff': abs(to_age - match.Gedetineerde.first().Verblijf.first().Leeftijd),
                'occupation': match.Gedetineerde.first().Verblijf.first().Beroep.first().Beroep_vertaling
            })
        # Add o_c_prisoner
        l_to_compare.append({
            'age_diff': abs(to_age - o_c_prisoner.Gedetineerde.first().Verblijf.first().Leeftijd),
            'occupation': o_c_prisoner.Gedetineerde.first().Verblijf.first().Beroep.first().Beroep_vertaling
        })
        # Sort
        if len(l_to_compare) > 0:
            l_dist = sorted(l_to_compare, key=lambda prisoner: prisoner['age_diff'])
            return l_dist[0]['occupation']
        else:
            print('No matches.')
            return o_c_prisoner.Gedetineerde.first().Verblijf.first().Beroep.first().Beroep_vertaling
