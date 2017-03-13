import couchdb


class Cache:
    @property
    def server(self):
        return couchdb.Server('http://nas.nidavellir.be:5984')


class RecidivistsCache(Cache):
    def __init__(self):
        try:
            self.db = self.server['recidivists']
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create('recidivists')

    def set(self, recidivists):
        doc = {'data': recidivists, '_id': 'recidivists_data'}
        self.db.save(doc)
        return doc['data']

    def get(self):
        try:
            result = self.db['recidivists_data']['data']
        except couchdb.http.ResourceNotFound:
            result = None
        return result


class AllWithDataCache(Cache):
    def __init__(self):
        try:
            self.db = self.server['all_with_data']
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create('all_with_data')

    def set(self, recidivists):
        doc = {'data': recidivists, '_id': 'all_with_data'}
        self.db.save(doc)
        return doc['data']

    def get(self):
        try:
            result = self.db['all_with_data']['data']
        except couchdb.http.ResourceNotFound:
            result = None
        return result


class NonRecidivistsCache(Cache):
    def __init__(self):
        try:
            self.db = self.server['non_recidivists']
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create('non_recidivists')

    def set(self, recidivists):
        doc = {'data': recidivists, '_id': 'non_recidivists_data'}
        self.db.save(doc)
        return doc['data']

    def get(self):
        try:
            result = self.db['non_recidivists_data']['data']
        except couchdb.http.ResourceNotFound:
            result = None
        return result


class AllCache(Cache):
    def __init__(self):
        try:
            self.db = self.server['all']
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create('all')

    def set(self, all_p):
        doc = {'data': all_p, '_id': 'all_data'}
        self.db.save(doc)
        return doc['data']

    def get(self):
        try:
            result = self.db['all_data']['data']
        except couchdb.http.ResourceNotFound:
            result = None
        return result


class BruggeCache(Cache):
    def __init__(self):
        try:
            self.db = self.server['all_brugge']
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create('all_brugge')

    def set(self, all_p):
        doc = {'data': all_p, '_id': 'all_data'}
        self.db.save(doc)
        return doc['data']

    def get(self):
        try:
            result = self.db['all_data']['data']
        except couchdb.http.ResourceNotFound:
            result = None
        return result


class GentCache(Cache):
    def __init__(self):
        try:
            self.db = self.server['all_gent']
        except couchdb.http.ResourceNotFound:
            self.db = self.server.create('all_gent')

    def set(self, all_p):
        doc = {'data': all_p, '_id': 'all_data'}
        self.db.save(doc)
        return doc['data']

    def get(self):
        try:
            result = self.db['all_data']['data']
        except couchdb.http.ResourceNotFound:
            result = None
        return result
