#!/usr/bin/python
#
# Copyright 2014 Justin Rummel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, print_function

import gzip
from distutils.version import LooseVersion
from StringIO import StringIO
from xml.etree import ElementTree

try:
    from urllib.request import urlopen  # For Python 3
    from urllib.error import URLError
except ImportError:
    from urllib2 import urlopen  # For Python 2
    from urllib2 import URLError

# variables
base_url = 'https://softwareupdate.vmware.com/cds/vmw-desktop/'
fusion = 'fusion.xml'

# functions
def core_metadata(base_url, fusion):
    print(base_url)

    try:
        vsus = urlopen(base_url + fusion)
    except URLError as e:
        print(e.reason)

    data = vsus.read()
    # print(data)

    try:
        metaList = ElementTree.fromstring(data)
    except ExpatData:
        print("Unable to parse XML data from string")

    versions = []
    for metadata in metaList:
        version = metadata.find("version")
        versions.append(version.text)

    versions.sort(key=LooseVersion)
    latest = versions[-1]
    # print(latest)

    urls = []
    for metadata in metaList:
        url = metadata.find("url")
        urls.append(url.text)

    matching = [s for s in urls if latest in s]
    core = [s for s in matching if "core" in s]
    print(core[0])

    vsus.close()

    try:
        vLatest = urlopen(base_url + core[0])
    except URLError as e:
        print(e.reason)

    buf = StringIO( vLatest.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()
    # print(data)

    try:
        metadataResponse = ElementTree.fromstring(data)
    except ExpatData:
        print("Unable to parse XML data from string")

    relativePath = metadataResponse.find("bulletin/componentList/component/relativePath")
    print(core[0].replace("metadata.xml.gz", relativePath.text))
    print(base_url+core[0].replace("metadata.xml.gz", relativePath.text))

core_metadata(base_url, fusion)
