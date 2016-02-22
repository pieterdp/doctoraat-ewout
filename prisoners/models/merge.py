from prisoners import db
from prisoners.models.original import Gedetineerde


class PrisonersMerged(db.Model):
    __tablename__ = 'PrisonersMerged'
    id = db.Column(db.Integer, primary_key=True)
    id_gedetineerde_wrong = db.Column(db.Integer, index=True)
    id_gedetineerde = db.Column(db.Integer, db.ForeignKey(Gedetineerde.Id_gedetineerde))
    naam = db.Column(db.String(255), index=True)
    voornaam = db.Column(db.String(255), index=True)
    geboorteplaats = db.Column(db.String(255), index=True)
    geboorteplaats_nis = db.Column(db.String(255), index=True)
    geslacht = db.Column(db.String(32))
    misdrijf = db.Column(db.String(255))
    woonplaats = db.Column(db.String(255))
    woonplaats_nis = db.Column(db.String(255))
    beroep = db.Column(db.String(255))
    leeftijd = db.Column(db.String(255))
    geboortejaar = db.Column(db.String(255))
    lichaamslengte = db.Column(db.String(255))
    flag = db.Column(db.Boolean, default=False)
    control_leeftijd = db.Column(db.String(255))
    control_lichaamslengte = db.Column(db.String(255))


class PrisonersCorrected(db.Model):
    __tablename__ = 'PrisonersCorrected'
    id = db.Column(db.Integer, primary_key=True)
    id_gedetineerde_old = db.Column(db.Integer, index=True)
    id_gedetineerde_new = db.Column(db.Integer, index=True)
    leeftijd = db.Column(db.String(255))
    beroep = db.Column(db.String(255))
    lichaamslengte = db.Column(db.String(255))


class PrisonersIds(db.Model):
    __tablename__ = 'PrisonersIds'
    id = db.Column(db.Integer, primary_key=True)
    id_gedetineerde = db.Column(db.Integer, index=True)


class PrisonersMergedBrugge(db.Model):
    __tablename__ = 'PrisonersMergedBrugge'
    id = db.Column(db.Integer, primary_key=True)
    id_gedetineerde = db.Column(db.Integer, index=True)
    naam = db.Column(db.String(255))
    voornaam = db.Column(db.String(255))
    geboorteplaats = db.Column(db.String(255))
    geboorteplaats_nis = db.Column(db.String(255))
    geslacht = db.Column(db.String(255))
    misdrijf = db.Column(db.String(255))
    woonplaats = db.Column(db.String(255))
    woonplaats_nis = db.Column(db.String(255))
    beroep = db.Column(db.String(255))
    geboortejaar = db.Column(db.String(255))
    lichaamslengte = db.Column(db.String(255))
    flag = db.Column(db.Boolean)
    leeftijd = db.Column(db.String(255))
