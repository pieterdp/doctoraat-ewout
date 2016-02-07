import Levenshtein
import re
from prisoners import db
from prisoners.models.original import Gedetineerde


#prisonersmatch = db.Table('PrisonersMatch',
#                          db.Column('master_id_ged', db.Integer, db.ForeignKey('PrisonersCompare.id_gedetineerde')),
#                          db.Column('slave_id_ged', db.Integer, db.ForeignKey('PrisonersCompare.c_id_gedetineerde'))
#                          )


class PrisonersMatch(db.Model):
    __tablename__ = 'PrisonersMatch'
    id = db.Column(db.Integer, primary_key=True)
    master_id_ged = db.Column(db.Integer, db.ForeignKey('PrisonersCompare.id_gedetineerde'))
    slave_id_ged = db.Column(db.Integer, db.ForeignKey('PrisonersCompare.c_id_gedetineerde'))


class PrisonersCompare(db.Model):
    __tablename__ = 'PrisonersCompare'
    id = db.Column(db.Integer, primary_key=True)
    id_gedetineerde = db.Column(db.Integer, db.ForeignKey(Gedetineerde.Id_gedetineerde))
    Voornaam = db.Column(db.String(255), nullable=False, index=True)
    Naam = db.Column(db.String(255), nullable=False, index=True)
    Geboortejaar = db.Column(db.Integer, index=True)
    Geboortemaand = db.Column(db.Integer, index=True)
    Geboortedag = db.Column(db.Integer, index=True)
    Geboorteplaats = db.Column(db.String(255), index=True, nullable=False)
    c_id_gedetineerde = db.Column(db.Integer, index=True)
    c_voornaam = db.Column(db.String(255), nullable=False, index=True)
    c_naam = db.Column(db.String(255), nullable=False, index=True)
    c_geboortejaar = db.Column(db.Integer, index=True)
    c_geboortemaand = db.Column(db.Integer, index=True)
    c_geboortedag = db.Column(db.Integer, index=True)
    c_geboorteplaats = db.Column(db.String(255), index=True, nullable=False)
    has_been_checked = db.Column(db.Boolean, nullable=False, default=False)
    l_score = db.Column(db.Numeric(10,9), index=True)
    matches = db.relationship('PrisonersCompare',
                              secondary=PrisonersMatch.__table__,
                              primaryjoin=(PrisonersMatch.master_id_ged == id_gedetineerde),
                              secondaryjoin=(PrisonersMatch.slave_id_ged == c_id_gedetineerde),
                              backref=db.backref('match_master', lazy='dynamic'),
                              lazy='dynamic'
                              )

    def __init__(self, id_gedetineerde, voornaam, naam, geboorteplaats, c_id_gedetineerde, c_voornaam, c_naam,
                 c_geboorteplaats, geboortejaar=None, geboortemaand=None, geboortedag=None, c_geboortejaar=None,
                 c_geboortemaand=None, c_geboortedag=None):
        self.id_gedetineerde = id_gedetineerde
        self.Voornaam = voornaam
        self.Naam = naam
        self.Geboortejaar = geboortejaar
        self.Geboortemaand = geboortemaand
        self.Geboortedag = geboortedag
        self.Geboorteplaats = geboorteplaats
        self.c_id_gedetineerde = c_id_gedetineerde
        self.c_voornaam = c_voornaam
        self.c_naam = c_naam
        self.c_geboortejaar = c_geboortejaar
        self.c_geboortemaand = c_geboortemaand
        self.c_geboortedag = c_geboortedag
        self.c_geboorteplaats = c_geboorteplaats

    def c_l_score(self):
        """
        Compute the levenshtein distance between naamvoornaam and c_naamc_voornaam
        :return:
        """
        master_naam = '{0}{1}'.format(self.Naam, self.Voornaam)
        master_c_naam = '{0}{1}'.format(self.c_naam, self.c_voornaam)
        non_alpha = re.compile('[^a-z]')
        # To lowercase
        master_naam.lower()
        master_c_naam.lower()
        # Remove all non alphabetical characters
        master_naam = non_alpha.sub('', master_naam)
        master_c_naam = non_alpha.sub('', master_c_naam)
        # Compute ratio
        self.l_score = Levenshtein.ratio(master_naam, master_c_naam)
