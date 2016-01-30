from prisoners import db


class Archiefbestanden(db.Model):
    __tablename__ = 'Archiefbestanden'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_archief = db.Column(db.Integer, index=True)
    Archiefbewaarplaats = db.Column(db.String(255), nullable=True)
    Toegang = db.Column(db.String(255), nullable=True)
    Archiefbestand = db.Column(db.String(255), nullable=True)
    Gevangenis = db.Column(db.String(255), nullable=True)
    Afdeling = db.Column(db.String(255), nullable=True)
    Opmerkingen = db.Column(db.String(255), nullable=True)
    Uitgebreide_beschrijving = db.Column(db.String(512), nullable=True)
    Verblijf = db.relationship('Verblijf', backref='Archief', lazy='dynamic')


class Gedetineerde(db.Model):
    __tablename__ = 'Gedetineerde'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_gedetineerde = db.Column(db.Integer, index=True)
    Voornaam = db.Column(db.String(255), index=True, nullable=True)
    Naam = db.Column(db.String(255), index=True, nullable=True)
    Geslacht = db.Column(db.String(32), nullable=True, index=True)
    Geboortedag = db.Column(db.Integer, nullable=True)
    Geboortemaand = db.Column(db.Integer, nullable=True)
    Geboortejaar = db.Column(db.Integer, nullable=True, index=True)
    Opmerkingen = db.Column(db.String(512), nullable=True)
    Verblijf = db.relationship('Verblijf', backref='Gedetineerde', lazy='dynamic')


class Verblijf(db.Model):
    __tablename__ = 'Verblijf'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_verblijf = db.Column(db.Integer, index=True)
    Id_ged = db.Column(db.Integer, db.ForeignKey(Gedetineerde.Id_gedetineerde))
    Id_archief = db.Column(db.Integer, db.ForeignKey(Archiefbestanden.Id_archief))
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
    Beroep = db.relationship('Beroep', backref='Verblijf', lazy='dynamic')
    Geboorteplaats = db.relationship('Geboorteplaats', backref='Verblijf', lazy='dynamic')
    Woonplaats = db.relationship('Woonplaats', backref='Verblijf', lazy='dynamic')
    Misdrijf = db.relationship('Misdrijf', backref='Verblijf', lazy='dynamic')
    Rechtbank = db.relationship('Rechtbank', backref='Verblijf', lazy='dynamic')
    Strafmaat = db.relationship('Strafmaat', backref='Verblijf', lazy='dynamic')


class Beroep(db.Model):
    __tablename__ = 'Beroep'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_beroep = db.Column(db.Integer, index=True)
    Id_verb = db.Column(db.Integer, db.ForeignKey(Verblijf.Id_verblijf))
    Beroep_letterlijk = db.Column(db.String(255), nullable=True)
    Beroep_vertaling = db.Column(db.String(255), nullable=True, index=True)
    Beroep_cat = db.Column(db.String(255), nullable=True, index=True)
    HISCO = db.Column(db.Integer, index=True, nullable=True)


class Geboorteplaats(db.Model):
    __tablename__ = 'Geboorteplaats'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_geboorteplaats = db.Column(db.Integer, index=True)
    Id_verbl = db.Column(db.Integer, db.ForeignKey(Verblijf.Id_verblijf))
    Plaatsnaam_letterlijk = db.Column(db.String(255), nullable=True)
    Plaatsnaam_vertaling = db.Column(db.String(255), index=True, nullable=True)
    Plaatsnaam_NIS = db.Column(db.String(64), index=True, nullable=True)
    NIS_CODE = db.Column(db.String(64), index=True, nullable=True)
    Jaar_VIII = db.Column(db.Integer, nullable=True, index=True)
    Jaar_1846 = db.Column(db.Integer, nullable=True, index=True)
    Jaar_1876 = db.Column(db.Integer, nullable=True, index=True)


class Woonplaats(db.Model):
    __tablename__ = 'Woonplaats'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_woonplaats = db.Column(db.Integer, index=True)
    Id_verbl = db.Column(db.Integer, db.ForeignKey(Verblijf.Id_verblijf))
    Plaatsnaam_letterlijk = db.Column(db.String(255), nullable=True)
    Plaatsnaam_vertaling = db.Column(db.String(255), index=True, nullable=True)
    Plaatsnaam_NIS = db.Column(db.String(64), index=True, nullable=True)


class Misdrijf(db.Model):
    __tablename__ = 'Misdrijf'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_misdrijf = db.Column(db.Integer, index=True)
    Id_verbl = db.Column(db.Integer, db.ForeignKey(Verblijf.Id_verblijf))
    Misdrijf_letterlijk = db.Column(db.String(255), nullable=True)
    Misdrijf_vertaling = db.Column(db.String(255), nullable=True, index=True)
    Misdrijf_cat = db.Column(db.String(255), nullable=True, index=True)


class Rechtbank(db.Model):
    __tablename__ = 'Rechtbank'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_rechtbank = db.Column(db.Integer, index=True)
    Id_verb = db.Column(db.Integer, db.ForeignKey(Verblijf.Id_verblijf))
    Plaats = db.Column(db.String(255), nullable=True)
    Soort = db.Column(db.String(255), nullable=True, index=True)


class Strafmaat(db.Model):
    __tablename__ = 'Strafmaat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Id_strafmaat = db.Column(db.Integer, index=True)
    Id_verb = db.Column(db.Integer, db.ForeignKey(Verblijf.Id_verblijf))
    Straf_d = db.Column(db.Integer, nullable=True)
    Straf_m = db.Column(db.Integer, nullable=True)
    Straf_j = db.Column(db.Integer, nullable=True)
    Levenslang = db.Column(db.Integer, nullable=True)
    Doodstraf = db.Column(db.Integer, nullable=True)
    Strafvermindering = db.Column(db.String(255), nullable=True)
    Andere = db.Column(db.String(255), nullable=True)
