from prisoners.modules.data_import import DataImporter


files = ['Gent_beroep.txt', 'Gent_geboorteplaats.txt', 'Gent_gedetineerde.txt', 'Gent_verblijf.txt']
#input_types = ['gedetineerde', 'verblijf', 'beroep', 'geboorteplaats']
input_types = ['beroep', 'geboorteplaats']

for input_type in input_types:
    print('Importing Gent_{0}.txt ...'.format(input_type))
    o_import = DataImporter(input_file='source_data/Gent_{0}.txt'.format(input_type))
    f_input = getattr(o_import, 'import_{0}'.format(input_type))
    received = f_input()
    print('Done')
