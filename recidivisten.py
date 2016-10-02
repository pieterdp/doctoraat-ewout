import csv
from prisoners.modules.recidive.get import RecidiveGet
from prisoners.modules.recidive.out import RecidiveOut, GenericOut
from prisoners.modules.all import All

param = 'GET_BELOW_21'

rg = RecidiveGet()

if param == 'GET_NON_REC':
    header = [
        'naam',
        'voornaam',
        'geboorteplaats',
        'gedetineerde0_id_ged',
        'gedetineerde0_inschrijvingsjaar',
        'gedetineerde0_leeftijd',
        'gedetineerde0_geslacht',
        'gedetineerde0_lengte'
    ]
    fh = open('output/geen_recidivisten.csv', 'w')
    csvwriter = csv.writer(fh, delimiter=',', quotechar='"')
    csvwriter.writerow(header)

    for not_recidivist in rg.not_recidivists:
        row = [
            not_recidivist['master_naam'],
            not_recidivist['master_voornaam'],
            not_recidivist['master_geboorteplaats'],
            not_recidivist['master_id'],
            not_recidivist['master_inschrijvingsjaar'],
            not_recidivist['master_leeftijd'],
            not_recidivist['master_geslacht'],
            not_recidivist['master_lengte']
        ]
        csvwriter.writerow(row)
    fh.close()

if param == 'GET_REC':
    output_file = 'output/recidivisten_met_geslacht.csv'
    ro = RecidiveOut(recidivists=rg.recidivists, csv_file=output_file)

if param == 'GET_BELOW_21':
    r_21 = rg.get_all_recidivists_below_21()
    age_catalog = GenericOut().make_age_catalog(r_21, 0, 21)
    fh = open('output/recidivisten_onder_21.csv', 'w')
    csvwriter = csv.writer(fh, delimiter=',', quotechar='"')
    for r in age_catalog:
        csvwriter.writerow(r)
    fh.close()

