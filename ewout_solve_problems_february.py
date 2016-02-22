import re
import csv
from prisoners import db
from prisoners.models.merge import PrisonersCorrected, PrisonersIds, PrisonersMerged, PrisonersMergedBrugge
from prisoners.modules.table_merge import TableMerge

# Import all ids using the CSV
print('Importing CSV ...')
#with open('Query1.csv', newline='') as csvfile:
#    id_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
#    for row in id_reader:
#        p_id = PrisonersIds()
#        p_id.id_gedetineerde = row[0]
#        db.session.add(p_id)
#    try:
#        db.session.commit()
#    except Exception as e:
#        db.session.rollback()
#        print(e)


print('Performing new match ...')
#tm = TableMerge(use_original=False)
#tm.new_merge()

print('Creating update table ...')
for ged_id in PrisonersIds.query.all():
    id_gedetineerde = ged_id.id_gedetineerde
    # If it is in MergedBrugge, just store it
    print('{0}'.format(str(id_gedetineerde)))
    in_brugge = PrisonersMergedBrugge.query.filter(PrisonersMergedBrugge.id_gedetineerde == id_gedetineerde).first()
    if in_brugge is not None:
        print('-> from Brugge')
        continue
        p_corr = PrisonersCorrected()
        p_corr.id_gedetineerde_old = in_brugge.id_gedetineerde
        p_corr.id_gedetineerde_new = in_brugge.id_gedetineerde
        p_corr.leeftijd = in_brugge.leeftijd
        p_corr.beroep = in_brugge.beroep
        # Convert to decimal
        dec_h = float(in_brugge.lichaamslengte)
        if dec_h == 0.0:
            print('Error converting age to decimal for {0}.'.format(in_brugge.id_gedetineerde))
            print('Original: {0}, new {1}'.format(in_brugge.lichaamslengte, dec_h))
        else:
            p_corr.lichaamslengte = dec_h * 10
        db.session.add(p_corr)
    else:
        # If not, check whether it could be a "wrong" prisoners_id
        is_wrong = PrisonersMerged.query.filter(PrisonersMerged.id_gedetineerde_wrong == id_gedetineerde).first()
        comma = re.compile(',')
        if is_wrong is not None:
            print('-> from Gent with wrong ID')
            p_corr = PrisonersCorrected()
            p_corr.id_gedetineerde_old = is_wrong.id_gedetineerde_wrong
            p_corr.id_gedetineerde_new = is_wrong.id_gedetineerde
            p_corr.leeftijd = is_wrong.leeftijd
            p_corr.beroep = is_wrong.beroep
            # Convert to decimal
            converted_height = comma.sub('.', is_wrong.lichaamslengte)
            dec_h = float(converted_height)
            if dec_h == 0.0:
                print('Error converting age to decimal for {0}.'.format(is_wrong.id_gedetineerde))
                print('Original: {0}, new {1}'.format(is_wrong.lichaamslengte, dec_h))
            else:
                p_corr.lichaamslengte = dec_h * 10
            db.session.add(p_corr)
        else:
            # Check whether it came from PrisonersMerged
            is_merged = PrisonersMerged.query.filter(PrisonersMerged.id_gedetineerde == id_gedetineerde).first()
            if is_merged:
                print('-> from Gent')
                p_corr = PrisonersCorrected()
                p_corr.id_gedetineerde_old = is_merged.id_gedetineerde
                p_corr.id_gedetineerde_new = is_merged.id_gedetineerde
                p_corr.leeftijd = is_merged.leeftijd
                p_corr.beroep = is_merged.beroep
                # Convert to decimal
                converted_height = comma.sub('.', is_merged.lichaamslengte)
                dec_h = float(converted_height)
                if dec_h == 0.0:
                    print('Error converting age to decimal for {0}.'.format(is_merged.id_gedetineerde))
                    print('Original: {0}, new {1}'.format(is_merged.lichaamslengte, dec_h))
                else:
                    p_corr.lichaamslengte = dec_h * 10
                db.session.add(p_corr)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
