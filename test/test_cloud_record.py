import unittest
from datetime import datetime

from apel.db.records import CloudRecord


class CloudRecordTest(unittest.TestCase):
    '''
    Test case for CloudRecord
    '''

    def setUp(self):
        self._msg1 = '''
VMUUID: 2012-12-04 09:15:01+00:00 CESNET vm-0
SiteName: CESNET
CloudComputeService: OpenNebula Service A
MachineName: 'one-0'
LocalUserId: 5
LocalGroupId: 1
GlobalUserName: NULL
FQAN: NULL
Status: completed
StartTime: 1318840264
EndTime: 1318848076
SuspendDuration: NULL
WallDuration: NULL
CpuDuration: NULL
CpuCount: 1
NetworkType: NULL
NetworkInbound: 0
NetworkOutbound: 0
PublicIPCount: 5
Memory: 512
Disk: NULL
BenchmarkType: Hepspec
Benchmark: 1006.3
StorageRecordId: NULL
ImageId: 'scilin6'
CloudType: OpenNebula
'''
        self._values1 = {'SiteName': 'CESNET',
                        'CloudComputeService': 'OpenNebula Service A',
                        'MachineName': '\'one-0\'',
                        'LocalUserId': '5',
                        'Status': 'completed',
                        'CpuCount': 1,
                        'PublicIPCount': 5,
                        'Memory': 512,
                        'BenchmarkType': 'Hepspec',
                        'Benchmark': 1006.3,
                        'ImageId': '\'scilin6\'',
                        'CloudType': 'OpenNebula'
                        }

        self._msg2 = '''
VMUUID: 2012-08-14 14:00:01+0200 FZJ Accounting Test
SiteName: FZJ
CloudComputeService: OpenStack Service A
MachineName: Accounting Test
LocalUserId: 1189105086dc4959bc9889383afc43b5
LocalGroupId: EGI FCTF
GlobalUserName: /DC=es/DC=irisgrid/O=cesga/CN=javier-lopez
FQAN: /ops/Role=NULL/Capability=NULL
Status: started
StartTime: 1343362725
EndTime: NULL
SuspendDuration: NULL
WallDuration: 1582876
CpuDuration: 437
CpuCount: 1
NetworkType: NULL
NetworkInbound: NULL
NetworkOutbound: NULL
PublicIPCount: 1
Memory: 512
Disk: 0
BenchmarkType: Si2k
Benchmark: 200
StorageRecordId: NULL
ImageId: Debian Testing (Wheezy)
CloudType: Openstack
'''

        self._values2 = {'SiteName': 'FZJ',
                        'CloudComputeService': 'OpenStack Service A',
                        'MachineName': 'Accounting Test',
                        'LocalUserId': '1189105086dc4959bc9889383afc43b5',
                        'GlobalUserName': '/DC=es/DC=irisgrid/O=cesga/CN=javier-lopez',
                        'FQAN': '/ops/Role=NULL/Capability=NULL',
                        'VO': 'ops',
                        'VOGroup': '/ops',
                        'VORole': 'Role=NULL',
                        'Status': 'started',
                        'CpuCount': 1,
                        'PublicIPCount': 1,
                        'Memory': 512,
                        'BenchmarkType': 'Si2k',
                        'Benchmark': 200,
                        'ImageId': 'Debian Testing (Wheezy)',
                        'CloudType': 'Openstack'
                         }

        # A v0.2 style message, used to check we can still
        # support a v0.2 cloud message
        self._msg3 = '''
VMUUID: 2013-11-14 19:15:21+00:00 CESNET vm-1
SiteName: CESNET
MachineName: 'one-1'
LocalUserId: 5
LocalGroupId: 1
GlobalUserName: NULL
FQAN: NULL
Status: completed
StartTime: 1318842264
EndTime: 1318849976
SuspendDuration: NULL
WallDuration: NULL
CpuDuration: NULL
CpuCount: 1
NetworkType: NULL
NetworkInbound: 0
NetworkOutbound: 0
Memory: 512
Disk: NULL
StorageRecordId: NULL
ImageId: 'scilin6'
CloudType: OpenNebula
'''

        self._values3 = {'SiteName': 'CESNET',
                         'CloudComputeService': 'None',
                         'MachineName': '\'one-1\'',
                         'LocalUserId': '5',
                         'Status': 'completed',
                         'CpuCount': 1,
                         'PublicIPCount': None,
                         'Memory': 512,
                         'BenchmarkType': 'None',
                         'Benchmark': 0.0,
                         'ImageId': '\'scilin6\'',
                         'CloudType': 'OpenNebula'}

        self._msg4 = '''
BenchmarkType: HEPSPEC06
Status: completed
SiteName: Test Site
MachineName: Test Machine
ImageId: Test Image ID
LocalUserId: Test Local User ID
FQAN: NULL
LocalGroupId: Test Local Group ID
VMUUID: Test VM ID
CloudType: caso/0.3.4 (OpenStack)
GlobalUserName: Test User
CloudComputeService: Test Service'''

        self._values4 = {'VMUUID': 'Test VM ID',
                         'SiteName': 'Test Site',
                         'CloudComputeService': 'Test Service',
                         'MachineName': 'Test Machine',
                         'LocalUserId': 'Test Local User ID',
                         'LocalGroupId': 'Test Local Group ID',
                         'GlobalUserName': 'Test User',
                         'FQAN': 'None',
                         'Status': 'completed',
                         'StartTime': None,
                         'EndTime': None,
                         'SuspendDuration': None,
                         'WallDuration': None,
                         'CpuDuration': None,
                         'CpuCount': 0,
                         'NetworkType': 'None',
                         'NetworkInbound': None,
                         'NetworkOutbound': None,
                         'Memory': None,
                         'Disk': None,
                         'StorageRecordId': 'None',
                         'ImageId': 'Test Image ID',
                         'CloudType': 'caso/0.3.4 (OpenStack)'}

        self.cases = {}
        self.cases[self._msg1] = self._values1
        self.cases[self._msg2] = self._values2
        self.cases[self._msg3] = self._values3
        self.cases[self._msg4] = self._values4

    def test_load_from_msg_value_check(self):
        """Check for correct values in CloudRecords generated from messages."""
        for msg in self.cases.keys():

            cr = CloudRecord()
            cr.load_from_msg(msg)

            cont = cr._record_content

            for key in self.cases[msg].keys():
                self.assertEqual(cont[key], self.cases[msg][key], "%s != %s for key %s" % (cont[key], self.cases[msg][key], key))

    def test_load_from_msg_type_check(self):
        """Check the fields of a parsed message are of the correct type."""
        for msg in self.cases.keys():

            cr = CloudRecord()
            cr.load_from_msg(msg)

            for key in cr._int_fields:
                value = cr._record_content[key]
                # Check the value we are going to be passing to MySQL
                # is an integer or None. MySQL 5.6.x rejects the value
                # otherwise, whereas 5.1.x interprets it as integer 0.
                valid_value = isinstance(value, int) or value is None
                # Use 'repr' to show quote marks if value is a string.
                self.assertTrue(valid_value, 'Integer %s with value: %s\n%s' %
                                (key, repr(value), msg))

            for key in cr._float_fields:
                value = cr._record_content[key]
                # Check the value we are going to be passing to MySQL
                # is a float or None. MySQL 5.6.x rejects the value
                # otherwise, whereas 5.1.x interprets it as 0.00.
                valid_value = isinstance(value, float) or value is None
                # Use 'repr' to show quote marks if value is a string.
                self.assertTrue(valid_value, 'Decimal %s with value: %s\n%s' %
                                (key, repr(value), msg))

            for key in cr._datetime_fields:
                value = cr._record_content[key]
                # Check the value we are going to be passing to MySQL
                # is a datetime or None. MySQL 5.6.x rejects the value
                # otherwise, whereas 5.1.x interprets it as a zero timestamp.
                valid_value = isinstance(value, datetime) or value is None
                # Use 'repr' to show quote marks if value is a string.
                self.assertTrue(valid_value, 'Datetime %s with value: %s\n%s' %
                                (key, repr(value), msg))

    def test_mandatory_fields(self):
        record = CloudRecord()
        record.set_field('VMUUID', 'host.example.org/cr/87912469269276')
        record.set_field('SiteName', 'MySite')
        record.set_field('MachineName', 'MyMachine')

        try:
            record._check_fields()
        except Exception as error:
            self.fail(
                '_check_fields method failed: %s [%s]' %
                (str(error), str(type(error)))
            )

if __name__ == '__main__':
    unittest.main()
