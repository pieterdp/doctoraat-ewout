from prisoners.modules.recidive.get import RecidiveGet
from prisoners.modules.recidive.out import RecidiveOut

output_file = 'output/recidivisten.csv'

rg = RecidiveGet()


ro = RecidiveOut(recidivists=rg.recidivists, csv_file=output_file)
