from prisoners import db
from prisoners.models.original import Gedetineerde


class PrisonersMerged(db.Model):
    __tablename__ = 'PrisonersMerged'
    id = db.Column(db.Integer, primary_key=True)
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
