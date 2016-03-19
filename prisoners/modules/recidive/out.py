import csv


class RecidiveOut:
    """
    Convert the list of masters from RecidiveGet to a CSV file:
    {
        id_master,
        master_naam,
        master_voornaam,
        master_geboorteplaats,
        master_inschrijvingsjaar,
        master_leeftijd,
        master_lengte,
        slaves: [
            {
                slave_id,
                slave_inschrijvingsjaar,
                slave_leeftijd,
                slave_lengte
            }
        ]
    }
    For every master, create a line like this:
    id;naam;voornaam;geboorteplaats;inschrijvingsjaar;leeftijd;lengte
    And then append to that line for every slave:
        slave_id;slave_inschrijvingsjaar;slave_leeftijd;slave_lengte
    """

    def __init__(self, recidivists, csv_file):
        self.recidivists = recidivists
        self.slave_count = 1
        rows = self.convert_to_rows()
        header = self.create_header()
        fh = open(csv_file, 'w')
        csvwriter = csv.writer(fh, delimiter=',', quotechar='"')
        csvwriter.writerow(header)
        for row in rows:
            csvwriter.writerow(row)
        fh.close()

    def convert_to_rows(self):
        rows = []
        for recidivist in self.recidivists:
            row = [
                recidivist['master_naam'],
                recidivist['master_voornaam'],
                recidivist['master_geboorteplaats'],
                recidivist['master_id'],
                recidivist['master_inschrijvingsjaar'],
                recidivist['master_leeftijd'],
                recidivist['master_lengte']
            ]
            i = 0
            for slave in recidivist['slaves']:
                i += 1
                if i > self.slave_count:
                    self.slave_count = i
                if slave is None:
                    continue
                row = row + [
                    slave['slave_id'],
                    slave['slave_inschrijvingsjaar'],
                    slave['slave_leeftijd'],
                    slave['slave_lengte']
                ]
            rows.append(row)
        return rows

    def create_header(self):
        """
        Create the CSV header
        id_master;master_naam;master_voornaam;master_geboorteplaats;master_inschrijvingsjaar;master_leeftijd;master_lengte
            slave[n]_id;slave[n]_inschrijvingsjaar;slave[n]_leeftijd;slave[n]_lengte
            for n > 0 and n <= slave_count
        :return:
        """
        header = [
            'naam',
            'voornaam',
            'geboorteplaats',
            'gedetineerde0_id_ged',
            'gedetineerde0_inschrijvingsjaar',
            'gedetineerde0_leeftijd',
            'gedetineerde0_lengte'
        ]
        for n in range(1, self.slave_count):
            header = header + [
                'gedetineerde{0}_id_ged'.format(str(n)),
                'gedetineerde{0}_inschrijvingsjaar'.format(str(n)),
                'gedetineerde{0}_leeftijd'.format(str(n)),
                'gedetineerde{0}_lengte'.format(str(n))
            ]
        return header

