import re
from prisoners.modules.cache import AllCache, BruggeCache, GentCache
from prisoners.models.brugge import GeboorteplaatsBrugge, VerblijfBrugge, GedetineerdeBrugge
from prisoners.models.original import Geboorteplaats, Gedetineerde, Verblijf

INVALIDATE_CACHE = False


class All:
    def __init__(self):
        pass

    def __a_cache(self):
        c = AllCache()
        if c.get() is None or INVALIDATE_CACHE == True:
            c.set(self.get_all())
        return c.get()

    def __b_cache(self):
        c = BruggeCache()
        if c.get() is None or INVALIDATE_CACHE == True:
            c.set(self.get_all_brugge())
        return c.get()

    def __g_cache(self):
        c = GentCache()
        if c.get() is None or INVALIDATE_CACHE == True:
            c.set(self.get_all_gent())
        return c.get()

    def get(self):
        return self.__a_cache()

    def get_all(self):
        gent = self.get_all_gent()
        brugge = self.get_all_brugge()
        all = {**gent, **brugge}
        return all

    def get_all_brugge(self):
        all_ged = GedetineerdeBrugge.query.all()
        with_info = {}
        for s_ged in all_ged:
            extra_info = self.add_info(s_ged)
            with_info[s_ged.Id_gedetineerde] = {
                'id': s_ged.Id_gedetineerde,
                'naam': s_ged.Naam,
                'voornaam': s_ged.Voornaam,
                'geslacht': s_ged.Geslacht,
                'geboorteplaats': extra_info['geboorteplaats'],
                'inschrijvingsjaar': extra_info['inschrijvingsjaar'],
                'leeftijd': extra_info['leeftijd'],
                'lengte': extra_info['lengte']
            }
        return with_info

    def get_all_gent(self):
        all_ged = Gedetineerde.query.all()
        with_info = {}
        for s_ged in all_ged:
            extra_info = self.add_info(s_ged)
            with_info[s_ged.Id_gedetineerde] = {
                'id': s_ged.Id_gedetineerde,
                'naam': s_ged.Naam,
                'voornaam': s_ged.Voornaam,
                'geslacht': s_ged.Geslacht,
                'geboorteplaats': extra_info['geboorteplaats'],
                'inschrijvingsjaar': extra_info['inschrijvingsjaar'],
                'leeftijd': extra_info['leeftijd'],
                'lengte': extra_info['lengte']
            }
        return with_info

    def add_info(self, db_ged):
        db_verbl = db_ged.Verblijf.first()
        if not db_verbl:
            print('Geen verblijf: {0}'.format(db_ged.Id_gedetineerde))
            return {
                'geboorteplaats': 'NOV_RECORD',
                'inschrijvingsjaar': 0,
                'leeftijd': 0,
                'lengte': 0
            }
        db_geb = db_verbl.Geboorteplaats.first()
        if not db_geb:
            print('Geen geboorteplaats: {0}'.format(db_ged.Id_gedetineerde))
            return {
                'geboorteplaats': 'NOG_RECORD',
                'inschrijvingsjaar': db_verbl.Inschrijvingsdatum_j,
                'leeftijd': db_verbl.Leeftijd,
                'lengte': self.convert_length(db_verbl.Lichaamslengte_m)
            }
        return {
            'geboorteplaats': db_geb.Plaatsnaam_vertaling,
            'inschrijvingsjaar': db_verbl.Inschrijvingsdatum_j,
            'leeftijd': db_verbl.Leeftijd,
            'lengte': self.convert_length(db_verbl.Lichaamslengte_m)
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
