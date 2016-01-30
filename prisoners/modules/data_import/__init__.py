import csv
from os.path import isfile
from prisoners.models.original import Beroep
from prisoners import db


class DataImporter:
    def __init__(self, input_file):
        if not isfile(input_file):
            raise FileNotFoundError('File {0} does not exit.'.format(input_file))
        f_input = open(input_file, 'r')
        self.r_csv = csv.DictReader(f_input)

    def import_beroep(self):
        for row in self.r_csv:
            db_beroep = Beroep()
            db_beroep.Id_beroep = row['Id_beroep']
            db_beroep.Id_verb = row['Id_verb']
            db_beroep.Beroep_letterlijk = row['Beroep_letterlijk']
            db_beroep.Beroep_vertaling = row['Beroep_vertaling']
            db_beroep.Beroep_cat = row['Beroep_cat']
            db_beroep.HISCO = row['HISCO']
            db.session.add(db_beroep)
            db.session.commit()
