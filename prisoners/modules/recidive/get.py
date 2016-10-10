import re
from prisoners.models.brugge import PrisonersMatchBrugge, GedetineerdeBrugge, GeboorteplaatsBrugge, VerblijfBrugge
from prisoners.models.compare import PrisonersMatch, UnmatchedBrugge, UnmatchedGent
from prisoners.models.original import Gedetineerde, Geboorteplaats, Verblijf
from prisoners.modules.cache import RecidivistsCache, NonRecidivistsCache
from prisoners.modules.all import All

INVALIDATE_CACHE = False


class RecidiveGet:
    """
    From both the *Brugge and the *Gent PrisonersMatch tables, get the list
    of matched prisoners. Those prisoners have been repeatedly incarcerated
    and are thus recidivists. We need the following information (both from the
    master and the slave): naam, voornaam, geboorteplaats, inschrijvingsjaar,
    leeftijd bij inschrijven, lengte bij inschrijven.
    We return a list of dictionaries:
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
        self.recidivists = self.__r_cache()
        self.not_recidivists = self.__n_cache()

    def __r_cache(self):
        c = RecidivistsCache()
        if c.get() is None or INVALIDATE_CACHE == True:
            c.set(self.get_all_recidivists())
        return c.get()

    def __n_cache(self):
        c = NonRecidivistsCache()
        if c.get() is None or INVALIDATE_CACHE == True:
            c.set(self.get_not_recidivists())
        return c.get()

    def get_not_recidivists(self):
        # Get all those unmatched
        unmatched_gent = UnmatchedGent.query.all()
        unmatched_brugge = UnmatchedBrugge.query.all()
        info_gent = []
        info_brugge = []
        print('Gent')
        for unmatched in unmatched_gent:
            info_gent.append(self.add_master_information(unmatched.id_gedetineerde))
        print('Brugge')
        for unmatched in unmatched_brugge:
            info_brugge.append(self.add_master_information_brugge(unmatched.id_gedetineerde))
        return info_gent + info_brugge

    def get_all_recidivists(self):
        # Get all master - slave combinations
        # Brugge
        masters_brugge = PrisonersMatchBrugge.query.all()
        masters_ghent = PrisonersMatch.query.all()
        recidivists = []
        masters = self.get_masters_and_slaves(masters_brugge, masters_ghent)
        # print(masters) #19300
        for master_id, slave_ids in masters.items():
            slaves = []
            # print(slave_ids)
            for slave_id in slave_ids:
                slaves.append(self.add_slave_information(slave_id))
            recidivist = self.add_master_information(master_id)
            recidivist['slaves'] = slaves
            recidivists.append(recidivist)
        return recidivists

    def get_all_recidivists_below_21(self):
        # id_master,
        # master_naam,
        # master_voornaam,
        # master_geboorteplaats,
        # master_inschrijvingsjaar,
        # master_leeftijd,
        # master_lengte,
        # slave_id,
        # slave_inschrijvingsjaar,
        # slave_leeftijd,
        # slave_lengte
        recidivists = self.__r_cache()
        below_21 = []
        for r in recidivists:
            person_data_points = []
            if r['master_leeftijd'] <= 21:
                person_data_points.append({
                    'id_ged': r['master_id'],
                    'leeftijd': r['master_leeftijd'],
                    'lengte': r['master_lengte'],
                    'inschrijving': [r['master_inschrijvingsjaar'], r['master_inschrijvingsmaand'], r['master_inschrijvingsdag']]
                })
            for s in r['slaves']:
                if s['slave_leeftijd'] is not None and s['slave_leeftijd'] <= 21:
                    person_data_points.append({
                        'id_ged': s['slave_id'],
                        'leeftijd': s['slave_leeftijd'],
                        'lengte': s['slave_lengte'],
                        'inschrijving': [s['slave_inschrijvingsjaar'], s['slave_inschrijvingsmaand'],
                                         s['slave_inschrijvingsdag']]
                    })
            if len(person_data_points) > 0:
                below_21.append(person_data_points)
        return below_21

    def get_coupled_data_below_21(self):
        below_21 = self.get_all_recidivists_below_21()
        below_coupled = []
        for row in below_21:
            coupled_row = []
            # Sort the row based on the ''.join(inschrijvingdatum)
            sorted_row = sorted(row, key=lambda item: (int(item['leeftijd']), self.mk_sortable_date(item['inschrijving'])))
            #if len(sorted_row) >= 2:
            i = 0
            while i < len(sorted_row):
                try:
                    next_item = sorted_row[i + 1]
                except IndexError:
                    # We're at the last item, so break
                    if len(coupled_row) == 0:
                        coupled_row = [[sorted_row[i]]]
                    break
                else:
                    coupled_row.append([sorted_row[i], sorted_row[i+1]])
                i += 1
            below_coupled.append(coupled_row)
        return below_coupled

    def mk_sortable_date(self, inschrijvingsdatum):
        j = inschrijvingsdatum[0]
        m = inschrijvingsdatum[1]
        d = inschrijvingsdatum[2]
        if len(str(m)) < 2:
            m = '0{0}'.format(m)
        if len(str(d)) < 2:
            d = '0{0}'.format(d)
        as_str = ''.join([str(j), str(m), str(d)])
        return int(as_str)

    def get_all_recidivists_above_eq_21(self):
        recidivists = self.__r_cache()
        above_21 = []
        return above_21

    def get_masters_and_slaves(self, brugge, gent):
        masters = {}
        for m_slave in brugge:
            # master.id, slave.id
            if m_slave.id_gedetineerde_master in masters:
                # Append the id_gedetineerde_slave to the list in masters[id_gedetineerde_master]
                masters[m_slave.id_gedetineerde_master].append(m_slave.id_gedetineerde_slave)
            else:
                masters[m_slave.id_gedetineerde_master] = [m_slave.id_gedetineerde_slave]
        for m_slave in gent:
            if m_slave.master_id_ged in masters:
                masters[m_slave.master_id_ged].append(m_slave.slave_id_ged)
            else:
                masters[m_slave.master_id_ged] = [m_slave.slave_id_ged]
        return masters

    def add_slave_information(self, slave_id):
        db_gedetineerde = Gedetineerde.query.filter(Gedetineerde.Id_gedetineerde == slave_id).first()
        if db_gedetineerde is None:
            # The prisoner is from the *Brugge table
            return self.add_slave_information_brugge(slave_id)
        additional_info = self.get_verblijf_geboorteplaats(db_gedetineerde)  # Get information from Verblijf and
        # Geboorteplaats
        return {
            'slave_id': slave_id,
            'slave_inschrijvingsjaar': additional_info['inschrijvingsjaar'],
            'slave_inschrijvingsmaand': additional_info['inschrijvingsmaand'],
            'slave_inschrijvingsdag': additional_info['inschrijvingsdag'],
            'slave_geslacht': db_gedetineerde.Geslacht,
            'slave_leeftijd': additional_info['leeftijd'],
            'slave_lengte': additional_info['lengte']
        }

    def add_slave_information_brugge(self, slave_id):
        db_gedetineerde = GedetineerdeBrugge.query.filter(GedetineerdeBrugge.Id_gedetineerde == slave_id).first()
        if db_gedetineerde is None:
            return None
        additional_info = self.get_verblijf_geboorteplaats(db_gedetineerde)  # Get information from Verblijf and
        # Geboorteplaats
        return {
            'slave_id': slave_id,
            'slave_inschrijvingsjaar': additional_info['inschrijvingsjaar'],
            'slave_inschrijvingsmaand': additional_info['inschrijvingsmaand'],
            'slave_inschrijvingsdag': additional_info['inschrijvingsdag'],
            'slave_geslacht': db_gedetineerde.Geslacht,
            'slave_leeftijd': additional_info['leeftijd'],
            'slave_lengte': additional_info['lengte']
        }

    def add_master_information(self, master_id):
        db_gedetineerde = Gedetineerde.query.filter(Gedetineerde.Id_gedetineerde == master_id).first()
        if db_gedetineerde is None:
            # The prisoner is from the *Brugge table
            return self.add_master_information_brugge(master_id)
        additional_info = self.get_verblijf_geboorteplaats(db_gedetineerde)  # Get information from Verblijf and
        # Geboorteplaats
        return {
            'master_id': master_id,
            'master_naam': db_gedetineerde.Naam,
            'master_voornaam': db_gedetineerde.Voornaam,
            'master_geboorteplaats': additional_info['geboorteplaats'],
            'master_inschrijvingsjaar': additional_info['inschrijvingsjaar'],
            'master_inschrijvingsmaand': additional_info['inschrijvingsmaand'],
            'master_inschrijvingsdag': additional_info['inschrijvingsdag'],
            'master_geslacht': db_gedetineerde.Geslacht,
            'master_leeftijd': additional_info['leeftijd'],
            'master_lengte': additional_info['lengte']
        }

    def add_master_information_brugge(self, master_id):
        db_gedetineerde = GedetineerdeBrugge.query.filter(GedetineerdeBrugge.Id_gedetineerde == master_id).first()
        if db_gedetineerde is None:
            return None
        additional_info = self.get_verblijf_geboorteplaats(db_gedetineerde)  # Get information from Verblijf and
        # Geboorteplaats
        return {
            'master_id': master_id,
            'master_naam': db_gedetineerde.Naam,
            'master_voornaam': db_gedetineerde.Voornaam,
            'master_geboorteplaats': additional_info['geboorteplaats'],
            'master_inschrijvingsjaar': additional_info['inschrijvingsjaar'],
            'master_inschrijvingsmaand': additional_info['inschrijvingsmaand'],
            'master_inschrijvingsdag': additional_info['inschrijvingsdag'],
            'master_geslacht': db_gedetineerde.Geslacht,
            'master_leeftijd': additional_info['leeftijd'],
            'master_lengte': additional_info['lengte']
        }

    def get_verblijf_geboorteplaats(self, db_gedetineerde):
        db_verblijf = db_gedetineerde.Verblijf.first()
        if not db_verblijf:
            print('Geen verblijf: {0}'.format(db_gedetineerde.Id_gedetineerde))
            return {
                'geboorteplaats': '',
                'inschrijvingsjaar': 0,
                'inschrijvingsmaand': 0,
                'inschrijvingsdag': 0,
                'leeftijd': 0,
                'lengte': 'ERROR_NO_LENGTH'
            }
        db_geboorteplaats = db_verblijf.Geboorteplaats.first()
        if not db_geboorteplaats:
            print('Geen geboorteplaats: {0}'.format(db_gedetineerde.Id_gedetineerde))
            return {
                'geboorteplaats': '',
                'inschrijvingsjaar': db_verblijf.Inschrijvingsdatum_j,
                'inschrijvingsmaand': db_verblijf.Inschrijvingsdatum_m,
                'inschrijvingsdag': db_verblijf.Inschrijvingsdatum_d,
                'leeftijd': db_verblijf.Leeftijd,
                'lengte': self.convert_length(db_verblijf.Lichaamslengte_m)
            }
        return {
            'geboorteplaats': db_geboorteplaats.Plaatsnaam_vertaling,
            'inschrijvingsjaar': db_verblijf.Inschrijvingsdatum_j,
            'inschrijvingsmaand': db_verblijf.Inschrijvingsdatum_m,
            'inschrijvingsdag': db_verblijf.Inschrijvingsdatum_d,
            'leeftijd': db_verblijf.Leeftijd,
            'lengte': self.convert_length(db_verblijf.Lichaamslengte_m)
        }

    def convert_length(self, original):
        """
        Convert the length from a string to a float. Multiply it by 10
        To get rid of all the comma's.
        :param original:
        :return:
        """
        if original is None or original == '':
            return 'ERROR_NO_LENGTH'
        comma = re.compile(',')
        converted_height = comma.sub('.', original)
        dec_h = float(converted_height)
        return round(dec_h * 10)
