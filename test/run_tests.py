#!/usr/bin/env python

#  Copyright 2008-2013 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys

from xml.etree.ElementTree import ElementTree
from subprocess import call

COMMANDS = [
    'pybot --loglevel DEBUG --log NONE --report NONE example.txt'.split(),
    'python ../robotstatuschecker.py output.xml'.split(),
    'rebot output.xml'.split()
]

class StatusCheckerChecker():

    def __init__(self):
        pass

    def check_tests(self):
        for cmd in COMMANDS:
            call(cmd)
        xml = ElementTree(file='output.xml')
        errors = self.check_and_return_errors(xml)
        if errors:
            sys.exit('\nTests for StatusChecker have failed:\n\n%s'
                     % '\n'.join(errors))
        print '\nTests for StatusChecker have completed successfully.'
        sys.exit(0)

    def check_and_return_errors(self, xml):
        errors = []
        for test_element in xml.iter('test'):
            name, status = self._get_name_and_status(test_element)
            if name.startswith('FAILURE:'):
                if status != 'FAIL':
                    errors.append('Test "%s" should have failed but passed' % name)
            elif status != 'PASS':
                errors.append('Test "%s" should have passed but failed' % name)
        return errors

    def _get_name_and_status(self, test_element):
        return (test_element.attrib['name'],
                test_element.find('status').attrib['status'])

if __name__ == '__main__':
    StatusCheckerChecker().check_tests()
