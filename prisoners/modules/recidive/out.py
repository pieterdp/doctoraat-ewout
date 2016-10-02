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
                recidivist['master_geslacht'],
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
                    slave['slave_geslacht'],
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
            'gedetineerde0_geslacht',
            'gedetineerde0_lengte'
        ]
        for n in range(1, self.slave_count):
            header = header + [
                'gedetineerde{0}_id_ged'.format(str(n)),
                'gedetineerde{0}_inschrijvingsjaar'.format(str(n)),
                'gedetineerde{0}_leeftijd'.format(str(n)),
                'gedetineerde{0}_geslacht'.format(str(n)),
                'gedetineerde{0}_lengte'.format(str(n))
            ]
        return header


class GenericOut:
    def make_age_catalog(self, data_list, min_age, max_age):
        header = [
            'id_gedetineerde'
        ] + [
            'lengte_at_{0}'.format(age) for age in range(min_age, max_age + 1, 1)
        ]
        rows = [header]
        for data_item in data_list:
            # 1 + (age - min_age) = position in row
            #item0 = id_gedetineerde
            row = [[]]*((max_age + 1 - min_age) + 1)
            row[0] = data_item[0]['id_ged']
            for data_point in data_item:
                orig = row[1 + (data_point['leeftijd'] - min_age)]
                new_point = data_point['inschrijving'], data_point['leeftijd'], data_point['lengte']
                if len(orig) == 0:
                    row[1 + (data_point['leeftijd'] - min_age)] = [new_point]
                else:
                    row[1 + (data_point['leeftijd'] - min_age)].append(new_point)
            string_row = []
            # Loop over the row
            for r in row[1:]:
                if len(r) == 0:
                    string_item = 0
                elif len(r) == 1:
                    # We have one data point
                    item = r[0]
                    string_item = '{0}:{1}'.format(item[1], item[2])
                else:
                    # Sort based on ''.join(inschrijving)
                    sortable = []
                    for item in r:
                        sortable_item = [self.mk_sortable_date(item[0]), '{0}:{1}'.format(item[1], item[2])]
                        sortable.append(sortable_item)
                    sorted_items = sorted(sortable, key=lambda s_item: s_item[0])
                    string_item = ','.join([s[1] for s in sorted_items])
                string_row.append(string_item)
            if self.non_zero(string_row) >= 1:
                rows.append(string_row)
        return rows

    def make_coupled_catalog(self, data_list):
        rows = []
        for data_item in data_list:
            row = [data_item[0][0]['id_ged']]
            for data_couple in data_item:
                row.append('{0}:{1}|{2}:{3}'.format(
                    data_couple[0]['leeftijd'],
                    data_couple[0]['lengte'],
                    data_couple[1]['leeftijd'],
                    data_couple[1]['lengte']
                ))
            rows.append(row)
        return rows

    def non_zero(self, row):
        count = 0
        for i in row:
            if i != 0:
                count += 1
        return count

    def mk_sortable_date(self, inschrijvingsdatum):
        j = inschrijvingsdatum[0]
        m = inschrijvingsdatum[1]
        d = inschrijvingsdatum[2]
        if len(str(m)) < 2:
            m = '0{0}'.format(m)
        if len(str(d)) < 2:
            d = '0{0}'.format(d)
        as_str = ''.join([str(j), str(m), str(d)])
        return int(as_str)
