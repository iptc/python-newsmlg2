# NewsML-G2 - Python implementation of the NewsML-G2 standard

NewsML-G2 is an open standard created by the International Press
Telecommunications Council to share news content. See http://www.newsml-g2.org/

This module is a part-implementation of the standard in Python.  Currently it
reads itemMeta and contentMeta blocks, catalogs and metadata objects from
NewsML-G2 XML files and outputs Python objects.

Work in progress.

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
    standardversion="2.29"
    conformance="power"
    version="1"
    xml:lang="en-GB">
    <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_36.xml" />
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
assert newsitem.standardversion == '2.29'
assert newsitem.conformance == 'power'

itemmeta = newsitem.itemmeta
# you can choose whether to use qcodes or URIs, we do the conversion for you
# using the catalog declared in the NewsML-G2 file
assert itemmeta.itemclass == 'ninat:text'
assert resolve_qcode(itemmeta.itemclass) == 'http://cv.iptc.org/newscodes/ninature/text'
assert itemmeta.provider == 'nprov:IPTC'
assert resolve_qcode(itemmeta.provider) == 'http://cv.iptc.org/newscodes/newsprovider/IPTC'
# Elements that contain a simple text string can be read with str(class)
assert str(itemmeta.versioncreated) == '2020-06-22T12:00:00+03:00'

etc...
```

## Creating NewsML-G2 files from code

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
        g2doc.set_item(newsitem)

        output_newsitem = g2doc.get_item()
        assert newsitem.guid == 'test-guid'
        assert newsitem.standard == 'NewsML-G2'
        assert newsitem.standardversion == '2.29'
        assert newsitem.conformance == 'power'
        assert newsitem.version == '1'
        assert newsitem.xml_lang == 'en-GB'

        output_xml = g2doc.to_xml()
        assert output_xml == (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            '<newsItem xmlns="http://iptc.org/std/nar/2006-10-01/" xmlns:nitf="http://iptc.org/std/NITF/2006-10-18/" xml:lang="en-GB" standard="NewsML-G2" standardversion="2.29" conformance="power" guid="test-guid" version="1">\n'
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
