import re
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
        self.recidivists = self.get_all_recidivists()

    def get_all_recidivists(self):
        # Get all master - slave combinations
        # Brugge
        masters_brugge = PrisonersMatchBrugge.query.all()
        masters_ghent = PrisonersMatch.query.all()
        recidivists = []
        masters = self.get_masters_and_slaves(masters_brugge, masters_ghent)
        #print(masters) #19300
        for master_id, slave_ids in masters.items():
            slaves = []
            #print(slave_ids)
            for slave_id in slave_ids:
                slaves.append(self.add_slave_information(slave_id))
            recidivist = self.add_master_information(master_id)
            recidivist['slaves'] = slaves
            recidivists.append(recidivist)
        return recidivists

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
            'master_leeftijd': additional_info['leeftijd'],
            'master_lengte': additional_info['lengte']
        }

    def get_verblijf_geboorteplaats(self, db_gedetineerde):
        db_verblijf = db_gedetineerde.Verblijf.first()
        db_geboorteplaats = db_verblijf.Geboorteplaats.first()
        return {
            'geboorteplaats': db_geboorteplaats.Plaatsnaam_vertaling,
            'inschrijvingsjaar': db_verblijf.Inschrijvingsdatum_j,
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
