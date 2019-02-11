from config_local import api_keys
import time
import hashlib
import redis
import json
import requests


class Intel:
    def __init__(self, server='localhost', **kwargs):
        self.kwargs = kwargs
        self.rserver = redis.Redis(host=server, port=6379, db=0)
        self.cache = {
            'virustotal': 3600,
            'greynoise': 3600,
            'xforce': 3600,
            'hybridanalysis':3600,
        }

    def check_cache(self, job, value):
        job_name = '{}-{}'.format(job, value)
        job_id = hashlib.md5(job_name.encode('utf-8')).hexdigest()
        get_cache = self.rserver.get(job_id)
        records = json.loads(get_cache) if get_cache is not None else []
        return {'job_id':job_id, 'records':records}

    def greynoise(self):
        result = self.check_cache('greynoise', self.kwargs['ip'])
        if not result['records']:
            greynoise = requests.post(api_keys['greynoise']['url'], data={'ip':self.kwargs['ip']}).json()
            result['records'] = greynoise.get('records', [])
            self.rserver.set(result['job_id'], json.dumps(result['records']), ex=self.cache['greynoise'])
        return result
    
    def virustotal(self):
        result = self.check_cache('virustotal',  self.kwargs['md5'])
        if not result['records']:
            url = '{}?apikey={}&resource={}'.format(api_keys['virustotal']['url'], api_keys['virustotal']['key'], self.kwargs['md5'])
            virustotal = requests.get(url).json()
            result['records'] = [virustotal] if virustotal['response_code'] == 1 else []
            self.rserver.set(result['job_id'], json.dumps(result['records']), ex=self.cache['virustotal'])
        return result

    def xforce(self):
        result = self.check_cache('xforce',  self.kwargs['md5'])
        if not result['records']:
            url = '{}/malware/{}'.format(api_keys['xforce']['url'], self.kwargs['md5'])
            xforce = requests.get(url, auth=(api_keys['xforce']['key'], api_keys['xforce']['password'])).json()
            result['records'] = [xforce] if not 'error' in xforce else []
            self.rserver.set(result['job_id'], json.dumps(result['records']), ex=self.cache['xforce'])
        return result

    def hybridanalysis(self):
        result = self.check_cache('hybridanalysis-5',  str(self.kwargs['md5']))
        if not result['records']:
            url = '{}/hashes'.format(api_keys['hybridanalysis']['url'])
            headers = {'api-key':api_keys['hybridanalysis']['key'], 'User-Agent':'Falcon Sandbox',
                'Content-Type':'application/x-www-form-urlencoded'}
            data = ''.join(['hashes%5B%5D={}'.format(indicator) for indicator in self.kwargs['md5']])
            hybridanalysis = requests.post(url, headers=headers, data=data).json()
            result['records'] = hybridanalysis if not 'errorMessage' in hybridanalysis else []
            self.rserver.set(result['job_id'], json.dumps(result['records']), ex=self.cache['hybridanalysis'])
        return result
