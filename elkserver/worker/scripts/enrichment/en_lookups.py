import csv
import re

class Lookups:
    def __init__(self, path='../lookups'):
        self.path = path
        self.lookups = {
            'customer': self.read_customer,
            'redteam': self.read_redteam,
            'unknown': self.read_unknown,
            'sandboxes': self.read_sandboxes,
            'testsystems':self.read_testsystems,
            'exitnodes': self.read_exitnodes
        }

    def parse_multi(self, file_path, result=[]):
        csv_object = csv.DictReader(open(file_path), delimiter=';')
        for row in csv_object:
            result.append({
                'query_mode':row['query_mode'],
                'target_ipint':re.compile(row['target_ipint']),
                'target_hostname':re.compile(row['target_hostname']),
                'target_user':re.compile(row['target_user'])
            })

        return result

    def parse_single(self, file_path):
        csv_object = csv.DictReader(open(file_path), delimiter=';')
        primary_field = csv_object.fieldnames[0]
        result = {primary_field: {row[primary_field] for row in csv_object}}
        return result

    def read_sandboxes(self, lookup='known_sandboxes.csv'):
        file_path = '{}/{}'.format(self.path, lookup)
        sandboxes = self.parse_multi(file_path)
        return sandboxes

    def read_testsystems(self, lookup='known_testsystems.csv'):
        file_path = '{}/{}'.format(self.path, lookup)
        testsystems = self.parse_multi(file_path)
        return testsystems

    def read_exitnodes(self, lookup='iplist_exitnodes.csv'):
        file_path = '{}/{}'.format(self.path, lookup)
        exitnodes = self.parse_single(file_path)
        return exitnodes

    def read_customer(self, lookup='iplist_customer.csv'):
        file_path = '{}/{}'.format(self.path, lookup)
        customer = self.parse_single(file_path)
        return customer
            
    def read_redteam(self, lookup='iplist_redteam.csv'):
        file_path = '{}/{}'.format(self.path, lookup)
        redteam = self.parse_single(file_path)
        return redteam
            
    def read_unknown(self, lookup='iplist_unknown.csv'):
        file_path = '{}/{}'.format(self.path, lookup)
        unknown = self.parse_single(file_path)
        return unknown

    def load(self, result={}):
        for key, value in self.lookups.items():
            result[key] = value()
        return result