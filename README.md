# NewsML-G2 - Python implementation of the NewsML-G2 standard

NewsML-G2 is an open standard created by the International Press
Telecommunications Council to share news content. See http://www.newsml-g2.org/

This module is a part-implementation of the standard in Python.  Currently it
reads itemMeta and contentMeta blocks, catalogs and metadata objects from
NewsML-G2 XML files and outputs Python objects.

Currently built for Python 3 only - please let us know if you require Python 2
support.

## Installation

Installing from PyPI:

    pip install newsmlg2

## Reading NewsML-G2 files

Example:

```
import NewsMLG2

# load NewsML-G2 from a file and print the parsed version
g2doc = NewsMLG2.NewsMLG2Document(filename="test-newsmlg2-file.xml")
print(g2doc.get_item())

# load NewsML-G2 from a string
g2doc = NewsMLG2.NewsMLG2Document(
b"""<?xml version="1.0" encoding="UTF-8"?>
<newsItem
    xmlns="http://iptc.org/std/nar/2006-10-01/"
    guid="simplest-test"
    standard="NewsML-G2"
    standardversion="2.34"
    conformance="power"
    version="1"
    xml:lang="en-GB">
    <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_38.xml" />
    <itemMeta>
        <itemClass qcode="ninat:text" />
        <provider qcode="nprov:IPTC" />
        <versionCreated>2020-06-22T12:00:00+03:00</versionCreated>
    </itemMeta>
    <contentSet>
        <inlineXML contenttype="application/nitf+xml">
        </inlineXML>
    </contentSet>
</newsItem>
""")

# get the newsItem from the parsed object
newsitem = g2doc.getNewsItem()
# test various elements and attributes using our shortcut dot syntax
assert newsitem.guid == 'simplest-test'
assert newsitem.standard == 'NewsML-G2'
assert newsitem.standardversion == '2.34'
assert newsitem.conformance == 'power'

itemmeta = newsitem.itemmeta
# you can choose whether to use qcodes or URIs, we do the conversion for you
# using the catalog declared in the NewsML-G2 file
assert itemmeta.itemclass.qcode == 'ninat:text'
assert NewsMLG2.qcode_to_uri(itemmeta.itemclass.qcode) == 'http://cv.iptc.org/newscodes/ninature/text'
assert itemmeta.provider.qcode == 'nprov:IPTC'
assert NewsMLG2.qcode_to_uri(itemmeta.provider.qcode) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
# Elements that contain a simple text string can be read with str(class)
assert str(itemmeta.versioncreated) == '2020-06-22T12:00:00+03:00'

etc...
```

## Creating NewsML-G2 files in Python

There are a few points to note when creating NewsML-G2 directly in Python code (as opposed to
parsing a string containing XML).

* Elements with multiple values (such as multiple <broader> elements) must be created
individually and then added to their parent through array assignment. So you should create

Example:
```
g2doc = NewsMLG2.NewsMLG2Document()
newsitem = NewsMLG2.NewsItem()
newsitem.guid = 'test-guid'
newsitem.xml_lang = 'en-GB'
itemmeta = NewsMLG2.ItemMeta()
itemmeta.itemclass.qcode = "ninat:text"
itemmeta.provider.qcode = "nprov:IPTC"
itemmeta.versioncreated = "2020-06-22T12:00:00+03:00"
newsitem.itemmeta = itemmeta
contentmeta = NewsMLG2.NewsItemContentMeta()
contentmeta.contentcreated = '2008-11-05T19:04:00-08:00'
located = NewsMLG2.Located()
located.type = 'cptype:city'
located.qcode = 'city:345678'
located.name = 'Berlin'
contentmeta.located = located
located = NewsMLG2.Located()
located.type = 'cptype:city'
located.qcode = 'city:345678'
located.name = 'Berlin'
contentmeta.located = located
digsrctype = NewsMLG2.DigitalSourceType()
digsrctype.uri = 'http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia'
contentmeta.digitalsourcetype = digsrctype
broader1 = NewsMLG2.Broader()
broader1.type = 'cptype:statprov'
broader1.qcode = 'state:2365'
broader1.name = 'Berlin'
broader2 = NewsMLG2.Broader()
broader2.type = 'cptype:country'
broader2.qcode = 'iso3166-1a2:DE'
broader2.name = 'Germany'
contentmeta.located.broader = [broader1, broader2]
creator = NewsMLG2.Creator()
creator.qcode = 'codesource:DEZDF'
creator.name = 'Zweites Deutsches Fernsehen'
# This implements
# contentmeta.creator.organisationdetails.location.name = 'MAINZ'
# we have to make each item separately.
orgdetails = NewsMLG2.OrganisationDetails()
orglocation = NewsMLG2.OrganisationLocation()
orglocation.name = 'MAINZ'
orgdetails.location = orglocation
creator.organisationdetails = orgdetails
contentmeta.creator = creator
newsitem.contentmeta = contentmeta
g2doc.set_item(newsitem)

output_newsitem = g2doc.get_item()
assert newsitem.guid == 'test-guid'
assert newsitem.standard == 'NewsML-G2'
assert newsitem.standardversion == '2.34'
assert newsitem.conformance == 'power'
assert newsitem.version == '1'
assert newsitem.xml_lang == 'en-GB'

output_xml = g2doc.to_xml()
assert output_xml == (
    "<?xml version='1.0' encoding='utf-8'?>\n"
    '<newsItem xmlns="http://iptc.org/std/nar/2006-10-01/" xmlns:nitf="http://iptc.org/std/NITF/2006-10-18/" xml:lang="en-GB" standard="NewsML-G2" standardversion="2.34" conformance="power" guid="test-guid" version="1">\n'
    '  <itemMeta>\n'
    '    <itemClass qcode="ninat:text"/>\n'
    '    <provider qcode="nprov:IPTC"/>\n'
    '    <versionCreated>2020-06-22T12:00:00+03:00</versionCreated>\n'
    '  </itemMeta>\n'
    '</newsItem>\n')
```

## Testing

A unit test library is included.

Run it with:

    pytest

Test coverage can be measured with the `coverage.py` package:

    pip install coverage
    coverage run --source NewsMLG2 -m pytest 
    coverage report

## Release notes

* 0.1 - First release, pinned to Python 3 only (use pip >9.0 to ensure pip's
Python version requirement works properly)
* 0.2 - Can now read and write NewsML-G2 from code - NewsMessage and PlanningItem
not yet implemented. Probably quite a few bugs.
* 0.3 - Changed from automatically converting between URIs and QCodes to providing
helper functions `uri_to_qcode()` and `qcode_to_uri()`
* 0.4 - Added catalog v37 and v38. Added PlanningItem support. Fixed bugs. Improved
magic function support to help hasattr() and more on NewsML-G2 objects.
* 0.5 - Now has 100% unit test coverage. Fixed more bugs. Implemented changes up to
NewsML-G2 schema version v2.32.
* 0.6 - Implemented NewsMessage and Events (EventsML-G2). Adding arrays using code
(as opposed to parsing an XML string/file) now works. Almost ready to go to 1.0.
