from prisoners import db


class PrisonersMatchBrugge(db.Model):
    __tablename__ = 'PrisonersMatchBrugge'
    id = db.Column(db.Integer, primary_key=True)
    id_gedetineerde_master = db.Column(db.Integer, index=True)
    id_gedetineerde_slave = db.Column(db.Integer, index=True)


class GedetineerdeBrugge(db.Model):
    __tablename__ = 'GedetineerdeBrugge'
    Id_gedetineerde = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Voornaam = db.Column(db.String(255), index=True, nullable=True)
    Naam = db.Column(db.String(255), index=True, nullable=True)
    Geslacht = db.Column(db.String(32), nullable=True, index=True)
    Geboortedag = db.Column(db.Integer, nullable=True)
    Geboortemaand = db.Column(db.Integer, nullable=True)
    Geboortejaar = db.Column(db.Integer, nullable=True, index=True)
    Opmerkingen = db.Column(db.String(512), nullable=True)
    Verblijf = db.relationship('VerblijfBrugge', backref='Gedetineerde', lazy='dynamic')


class VerblijfBrugge(db.Model):
    __tablename__ = 'VerblijfBrugge'
    Id_verblijf = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_ged = db.Column(db.Integer, db.ForeignKey(GedetineerdeBrugge.Id_gedetineerde))
    Id_archief = db.Column(db.Integer)
    Rolnummer = db.Column(db.String(64), index=True)
    Inschrijvingsdatum_d = db.Column(db.Integer, index=True, nullable=True)
    Inschrijvingsdatum_m = db.Column(db.Integer, index=True, nullable=True)
    Inschrijvingsdatum_j = db.Column(db.Integer, index=True, nullable=True)
    Leeftijd = db.Column(db.Integer, index=True, nullable=True)
    Lichaamslengte_m = db.Column(db.String(255), index=True, nullable=True)
    Lichaamslengte_andere = db.Column(db.String(255), nullable=True)
    Lichaamsgewicht_opname = db.Column(db.String(255), nullable=True)
    Lichaamsgewicht_ontslag = db.Column(db.String(255), nullable=True)
    Ontslagdatum_d = db.Column(db.Integer, nullable=True)
    Ontslagdatum_m = db.Column(db.Integer, nullable=True)
    Ontslagdatum_j = db.Column(db.Integer, nullable=True)
    Burgerlijke_staat = db.Column(db.String(64), nullable=True, index=True)
    Geletterdheid = db.Column(db.String(255), nullable=True)
    Pokkenletsels = db.Column(db.Integer, nullable=True, index=True)
    Verminkingen = db.Column(db.String(255), nullable=True)
    Opmerkingen = db.Column(db.String(255), nullable=True)
    Geboorteplaats = db.relationship('GeboorteplaatsBrugge', backref='Verblijf', lazy='dynamic')


class GeboorteplaatsBrugge(db.Model):
    __tablename__ = 'GeboorteplaatsBrugge'
    Id_geboorteplaats = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_verbl = db.Column(db.Integer, db.ForeignKey(VerblijfBrugge.Id_verblijf))
    Plaatsnaam_letterlijk = db.Column(db.String(255), nullable=True)
    Plaatsnaam_vertaling = db.Column(db.String(255), index=True, nullable=True)
    Plaatsnaam_NIS = db.Column(db.String(64), index=True, nullable=True)
    NIS_CODE = db.Column(db.String(64), index=True, nullable=True)
    Jaar_VIII = db.Column(db.Integer, nullable=True, index=True)
    Jaar_1846 = db.Column(db.Integer, nullable=True, index=True)
    Jaar_1876 = db.Column(db.Integer, nullable=True, index=True)
