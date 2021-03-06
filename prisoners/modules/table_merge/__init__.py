from sqlalchemy import and_
from prisoners.models.compare import PrisonersCompare, PrisonersMatch
from prisoners.models.merge import PrisonersMerged
from prisoners.models.original import Gedetineerde, Verblijf
from prisoners import db


class TableMerge:

    def original_merge(self):
        """
        As the function worked originally
        :return:
        """
        for ged_result in self.get_all_ids():
            id_gedetineerde = ged_result[0]
            # Check whether it is in PrisonersCompare
            already_merged = PrisonersMerged.query.filter(PrisonersMerged.id_gedetineerde == id_gedetineerde).first()
            if already_merged:
                continue
            print(id_gedetineerde)
            #in_compare = db.session.query(prisonersmatch).filter(
            #    prisonersmatch.c.master_id_ged == id_gedetineerde).first()
            in_compare = PrisonersMatch.query.filter(PrisonersMatch.master_id_ged == id_gedetineerde).first()
            # in_compare = PrisonersCompare.query.filter(PrisonersCompare.id_gedetineerde == id_gedetineerde).first()
            if in_compare:
                print('Has some matches')
                db_pris_compare = PrisonersCompare.query. \
                    filter(PrisonersCompare.id_gedetineerde == id_gedetineerde).first()
                # Get the matches using a join (using .matches does not work)
                matches = self.get_matches(db_pris_compare)
                for match in matches:
                    print('idmatch:' + str(match.id_gedetineerde))
                # It is
                db_gedetineerde = db_pris_compare.Gedetineerde
                db_verblijf = db_gedetineerde.Verblijf.first()
                db_geboorteplaats = db_verblijf.Geboorteplaats.first()
                db_misdrijf = db_verblijf.Misdrijf.first()
                db_woonplaats = db_verblijf.Woonplaats.first()
                db_prisoner = PrisonersMerged()
                db_prisoner.id_gedetineerde = db_gedetineerde.Id_gedetineerde
                db_prisoner.naam = db_gedetineerde.Naam
                db_prisoner.voornaam = db_gedetineerde.Voornaam
                db_prisoner.geslacht = db_gedetineerde.Geslacht
                if db_geboorteplaats:
                    db_prisoner.geboorteplaats = db_geboorteplaats.Plaatsnaam_vertaling
                    db_prisoner.geboorteplaats_nis = db_geboorteplaats.Plaatsnaam_NIS
                if db_misdrijf:
                    db_prisoner.misdrijf = db_misdrijf.Misdrijf_vertaling
                if db_woonplaats:
                    db_prisoner.woonplaats = db_woonplaats.Plaatsnaam_vertaling
                    db_prisoner.woonplaats_nis = db_woonplaats.Plaatsnaam_NIS
                db_prisoner.beroep = self.get_occupation_closest_to(db_pris_compare, self.age_to, matches)
                # db_prisoner.leeftijd = db_pris_compare.Gedetineerde.first().Verblijf.first().Leeftijd
                db_prisoner.lichaamslengte = self.get_height_closest_to(db_pris_compare, self.age_to, matches)
                db_prisoner.geboortejaar = self.make_year_of_birth(db_pris_compare.Gedetineerde)
                db_prisoner.flag = True
                db_prisoner.control_leeftijd = self.make_control_leeftijd(db_pris_compare, matches)
                db_prisoner.control_lichaamslengte = self.make_control_lichaamslengte(db_pris_compare, matches)
                db.session.add(db_prisoner)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
            else:
                # It isn't
                # Check whether it has been matched (we skip those as well)
                #has_been_checked = db.session.query(prisonersmatch).filter(
                #    prisonersmatch.c.slave_id_ged == id_gedetineerde).first()
                has_been_checked = PrisonersMatch.query.filter(PrisonersMatch.slave_id_ged == id_gedetineerde).first()
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
                    db_prisoner.geslacht = db_gedetineerde.Geslacht
                    if db_geboorteplaats:
                        db_prisoner.geboorteplaats = db_geboorteplaats.Plaatsnaam_vertaling
                        db_prisoner.geboorteplaats_nis = db_geboorteplaats.Plaatsnaam_NIS
                    if db_misdrijf:
                        db_prisoner.misdrijf = db_misdrijf.Misdrijf_vertaling
                    if db_woonplaats:
                        db_prisoner.woonplaats = db_woonplaats.Plaatsnaam_vertaling
                        db_prisoner.woonplaats_nis = db_woonplaats.Plaatsnaam_NIS
                    if db_beroep:
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

    def new_merge(self):
        """
        Function that merges and returns the correct id_gedetineerde + fill in the age
        :return:
        """
        for ged_result in self.get_all_ids():
            id_gedetineerde = ged_result[0]
            # Check whether it is in PrisonersCompare
            already_merged = PrisonersMerged.query.filter(PrisonersMerged.id_gedetineerde == id_gedetineerde).first()
            if already_merged:
                continue
            print(id_gedetineerde)
            #in_compare = db.session.query(prisonersmatch).filter(
            #    prisonersmatch.c.master_id_ged == id_gedetineerde).first()
            in_compare = PrisonersMatch.query.filter(PrisonersMatch.master_id_ged == id_gedetineerde).first()
            # in_compare = PrisonersCompare.query.filter(PrisonersCompare.id_gedetineerde == id_gedetineerde).first()
            if in_compare:
                print('Has some matches')
                db_pris_compare = PrisonersCompare.query. \
                    filter(PrisonersCompare.id_gedetineerde == id_gedetineerde).first()
                # Get the matches using a join (using .matches does not work)
                matches = self.get_matches(db_pris_compare)
                for match in matches:
                    print('idmatch:' + str(match.id_gedetineerde))
                # It is
                # Now get all information from the one that's closest to our self.age_to
                db_prisoner_to_age = self.get_pris_closest_to(db_pris_compare, self.age_to, matches)

                print('pris closest to {0}: {1}'.format(str(self.age_to), str(db_prisoner_to_age.id_gedetineerde)))
                print('check:{0}'.format(db_pris_compare.id_gedetineerde))

                db_gedetineerde = db_prisoner_to_age.Gedetineerde
                db_verblijf = db_gedetineerde.Verblijf.first()
                db_geboorteplaats = db_verblijf.Geboorteplaats.first()
                db_misdrijf = db_verblijf.Misdrijf.first()
                db_woonplaats = db_verblijf.Woonplaats.first()
                db_beroep = db_verblijf.Beroep.first()

                db_prisoner = PrisonersMerged()
                db_prisoner.id_gedetineerde = db_gedetineerde.Id_gedetineerde
                db_prisoner.id_gedetineerde_wrong = db_pris_compare.id_gedetineerde
                db_prisoner.naam = db_gedetineerde.Naam
                db_prisoner.voornaam = db_gedetineerde.Voornaam
                db_prisoner.geslacht = db_gedetineerde.Geslacht
                if db_geboorteplaats:
                    db_prisoner.geboorteplaats = db_geboorteplaats.Plaatsnaam_vertaling
                    db_prisoner.geboorteplaats_nis = db_geboorteplaats.Plaatsnaam_NIS
                if db_misdrijf:
                    db_prisoner.misdrijf = db_misdrijf.Misdrijf_vertaling
                if db_woonplaats:
                    db_prisoner.woonplaats = db_woonplaats.Plaatsnaam_vertaling
                    db_prisoner.woonplaats_nis = db_woonplaats.Plaatsnaam_NIS
                if db_beroep:
                    db_prisoner.beroep = db_beroep.Beroep_vertaling
                db_prisoner.leeftijd = db_verblijf.Leeftijd
                db_prisoner.geboortejaar = self.make_year_of_birth(db_gedetineerde)
                db_prisoner.lichaamslengte = db_verblijf.Lichaamslengte_m
                db_prisoner.flag = False
                db_prisoner.control_leeftijd = self.make_control_leeftijd(db_pris_compare, matches)
                db_prisoner.control_lichaamslengte = self.make_control_lichaamslengte(db_pris_compare, matches)
                db.session.add(db_prisoner)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
            else:
                # It isn't
                # Check whether it has been matched (we skip those as well)
                #has_been_checked = db.session.query(prisonersmatch).filter(
                #    prisonersmatch.c.slave_id_ged == id_gedetineerde).first()
                has_been_checked = PrisonersMatch.query.filter(PrisonersMatch.slave_id_ged == id_gedetineerde).first()
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
                    db_prisoner.geslacht = db_gedetineerde.Geslacht
                    if db_geboorteplaats:
                        db_prisoner.geboorteplaats = db_geboorteplaats.Plaatsnaam_vertaling
                        db_prisoner.geboorteplaats_nis = db_geboorteplaats.Plaatsnaam_NIS
                    if db_misdrijf:
                        db_prisoner.misdrijf = db_misdrijf.Misdrijf_vertaling
                    if db_woonplaats:
                        db_prisoner.woonplaats = db_woonplaats.Plaatsnaam_vertaling
                        db_prisoner.woonplaats_nis = db_woonplaats.Plaatsnaam_NIS
                    if db_beroep:
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

    def __init__(self, use_original=True):
        self.age_to = 35
        if use_original is True:
            self.original_merge()

    def get_all_ids(self):
        return db.session.query(Gedetineerde.Id_gedetineerde).filter(and_(Gedetineerde.Id_gedetineerde == Verblijf.Id_ged,
                                                                          Verblijf.Leeftijd >= 20,
                                                                          Verblijf.Leeftijd <= 50)).all()

    def clear_matches(self, input_matches):
        t_matches = []
        cleared_matches = []
        for input_match in input_matches:
            if (input_match.id_gedetineerde, input_match.c_id_gedetineerde) not in t_matches:
                t_matches.append((input_match.id_gedetineerde, input_match.c_id_gedetineerde))
                cleared_matches.append(input_match)
        return cleared_matches

    def get_matches(self, master_prisoner):
        matches = []
        # Get all matches from PrisonersMatch
        all_matches = PrisonersMatch.query.filter(PrisonersMatch.master_id_ged == master_prisoner.id_gedetineerde).all()
        for p_match in all_matches:
            # Get the prisoner from PrisonersCompare
            pc_match = PrisonersCompare.query.filter(PrisonersCompare.id_gedetineerde == p_match.slave_id_ged).first()
            matches.append(pc_match)
        return matches

    def make_year_of_birth(self, input_gedetineerde):
        year_of_inscr = input_gedetineerde.Verblijf.first().Inschrijvingsdatum_j
        age_at_inscr = input_gedetineerde.Verblijf.first().Leeftijd
        return year_of_inscr - age_at_inscr

    def get_height_closest_to(self, o_c_prisoner, to_age, matches):
        """
        Get the height closes to to_age (e.g. 35) from a prisoners that originally
        came from PrisonerCompare and has matches
        :param o_c_prisoner:
        :param to_age:
        :param matches: cleared matches (self.clear_matches)
        :return:
        """
        l_to_compare = []
        # Get "gedetineerde" object we need to get Leeftijd
        for match in matches:
            l_to_compare.append({
                'age_diff': abs(to_age - match.Gedetineerde.Verblijf.first().Leeftijd),
                'height': match.Gedetineerde.Verblijf.first().Lichaamslengte_m
            })
        # Add the information from o_c_prisoner as well
        # EDIT: this is not necessary, it's already in matches
        # EDIT: now it is
        l_to_compare.append({
            'age_diff': abs(to_age - o_c_prisoner.Gedetineerde.Verblijf.first().Leeftijd),
            'height': o_c_prisoner.Gedetineerde.Verblijf.first().Lichaamslengte_m
        })
        # Sort
        if len(l_to_compare) > 0:
            l_dist = sorted(l_to_compare, key=lambda prisoner: prisoner['age_diff'])
            return l_dist[0]['height']
        else:
            print('No matches.')
            return o_c_prisoner.Gedetineerde.Verblijf.first().Lichaamslengte_m

    def get_pris_closest_to(self, o_c_prisoner, to_age, matches):
        l_to_compare = []
        # Get "gedetineerde" object we need to get Leeftijd
        for match in matches:
            l_to_compare.append({
                'age_diff': abs(to_age - match.Gedetineerde.Verblijf.first().Leeftijd),
                'prisoner': match
            })
        # Add the information from o_c_prisoner as well
        # EDIT: this is not necessary, it's already in matches
        # EDIT: now it is
        l_to_compare.append({
            'age_diff': abs(to_age - o_c_prisoner.Gedetineerde.Verblijf.first().Leeftijd),
            'prisoner': o_c_prisoner
        })
        # Sort
        if len(l_to_compare) > 0:
            l_dist = sorted(l_to_compare, key=lambda prisoner: prisoner['age_diff'])
            return l_dist[0]['prisoner']
        else:
            print('No matches.')
            return o_c_prisoner.Gedetineerde.Verblijf.first().Lichaamslengte_m

    def make_control_leeftijd(self, oc_prisoner, matches):
        control_list = []
        for match in matches:
            control_list.append(str(match.Gedetineerde.Verblijf.first().Leeftijd))
        control_list.append(str(oc_prisoner.Gedetineerde.Verblijf.first().Leeftijd))
        return ';'.join(control_list)

    def make_control_lichaamslengte(self, oc_prisoner, matches):
        control_list = []
        for match in matches:
            control_list.append(str(match.Gedetineerde.Verblijf.first().Lichaamslengte_m))
        control_list.append(str(oc_prisoner.Gedetineerde.Verblijf.first().Lichaamslengte_m))
        return ';'.join(control_list)

    def get_occupation_closest_to(self, o_c_prisoner, to_age, matches):
        l_to_compare = []
        for match in matches:
            db_beroep = match.Gedetineerde.Verblijf.first().Beroep.first()
            if db_beroep:
                l_to_compare.append({
                    'age_diff': abs(to_age - match.Gedetineerde.Verblijf.first().Leeftijd),
                    'occupation': db_beroep.Beroep_vertaling
                })
        # Add o_c_prisoner
        # EDIT: this is not necessary, it's already in matches
        # EDIT: now it is
        db_beroep = o_c_prisoner.Gedetineerde.Verblijf.first().Beroep.first()
        if db_beroep:
            l_to_compare.append({
                'age_diff': abs(to_age - o_c_prisoner.Gedetineerde.Verblijf.first().Leeftijd),
                'occupation': db_beroep.Beroep_vertaling
            })
        # Sort
        if len(l_to_compare) > 0:
            l_dist = sorted(l_to_compare, key=lambda prisoner: prisoner['age_diff'])
            return l_dist[0]['occupation']
        else:
            print('No matches.')
            if db_beroep:
                return db_beroep.Beroep_vertaling
            else:
                return None
