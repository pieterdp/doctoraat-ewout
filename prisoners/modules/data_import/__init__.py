# -*- coding: utf-8 -*-
import codecs
import csv
from os.path import isfile

from sqlalchemy.exc import IntegrityError

from prisoners import db
from prisoners.models.original import Beroep, Geboorteplaats, Gedetineerde, Verblijf


class DataImporter:
    def __init__(self, input_file):
        if not isfile(input_file):
            raise FileNotFoundError('File {0} does not exit.'.format(input_file))
        f_input = codecs.open(input_file, 'r', encoding='cp1252')
        self.r_csv = csv.DictReader(f_input, delimiter=';', quotechar='"')

    def check(self, c_db, id_column, check_id):
        existing_object = c_db.query.filter(getattr(c_db, id_column) == check_id).first()
        if existing_object:
            return True
        else:
            return False

    def import_beroep(self):
        l_beroep = []
        for row in self.r_csv:
            if not self.check(Beroep, 'Id_beroep', row['Id_beroep']):
                db_beroep = Beroep()
                db_beroep.Id_beroep = row['Id_beroep']
                db_beroep.Id_verb = row['Id_verb']
                db_beroep.Beroep_letterlijk = row['Beroep_letterlijk']
                db_beroep.Beroep_vertaling = row['Beroep_vertaling']
                db_beroep.Beroep_cat = row['Beroep_cat']
                try:
                    db.session.add(db_beroep)
                    db.session.commit()
                    l_beroep.append(db_beroep)
                    print(db_beroep)
                except IntegrityError as e:
                    db.session.rollback()
                    print('Integrity Error: {0}'.format(e))
        return l_beroep

    def import_geboorteplaats(self):
        l_geboorteplaats = []
        for row in self.r_csv:
            db_geboorteplaats = Geboorteplaats()
            db_geboorteplaats.Id_geboorteplaats = row['Id_geboorteplaats']
            db_geboorteplaats.Id_verbl = row['Id_verbl']
            db_geboorteplaats.Plaatsnaam_letterlijk = row['Plaatsnaam_letterlijk']
            db_geboorteplaats.Plaatsnaam_vertaling = row['Plaatsnaam_vertaling']
            try:
                db.session.add(db_geboorteplaats)
                db.session.commit()
                l_geboorteplaats.append(db_geboorteplaats)
                print(db_geboorteplaats)
            except IntegrityError as e:
                db.session.rollback()
                print('Integrity Error: {0}'.format(e))
        return l_geboorteplaats

    def import_gedetineerde(self):
        l_gedetineerde = []
        for row in self.r_csv:
            db_gedetineerde = Gedetineerde()
            db_gedetineerde.Id_gedetineerde = row['Id_gedetineerde']
            db_gedetineerde.Voornaam = row['Voornaam']
            db_gedetineerde.Naam = row['Naam']
            db_gedetineerde.Geslacht = row['Geslacht']
            db.session.add(db_gedetineerde)
            db.session.commit()
            l_gedetineerde.append(db_gedetineerde)
            print(db_gedetineerde)
        return l_gedetineerde

    def import_verblijf(self):
        l_verblijf = []
        for row in self.r_csv:
            if row['Id_ged'] and row['Id_verblijf']:
                db_verblijf = Verblijf()
                db_verblijf.Id_verblijf = row['Id_verblijf']
                db_verblijf.Id_ged = row['Id_ged']
                db_verblijf.Rolnummer = row['Rolnummer']
                db_verblijf.Inschrijvingsdatum_d = row['Inschrijvingsdatum_d']
                db_verblijf.Inschrijvingsdatum_m = row['Inschrijvingsdatum_m']
                db_verblijf.Inschrijvingsdatum_j = row['Inschrijvingsdatum_j']
                db_verblijf.Leeftijd = row['Leeftijd']
                db_verblijf.Lichaamslengte_m = row['Lichaamslengte_m']
                db.session.add(db_verblijf)
                db.session.commit()
                print(db_verblijf)
                l_verblijf.append(db_verblijf)
        return l_verblijf
