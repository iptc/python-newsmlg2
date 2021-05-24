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

Installing from PyPI (after we release it to PyPI...):

    pip install newsml-g2

## Usage

Example:

```
    import NewsMLG2

    parser = NewsMLG2.NewsMLG2Parser(filename="test-newsmlg2-file.xml")
    print(parser.getNewsItem())

    parser = NewsMLG2.NewsMLG2Parser(b"""<?xml version="1.0" encoding="UTF-8"?>
<newsItem
    xmlns="http://iptc.org/std/nar/2006-10-01/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    guid="simplest-test"
    standard="NewsML-G2"
    standardversion="2.29"
    conformance="power"
    version="1"
    xml:lang="en-GB">
    <catalogRef href="http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_35.xml" />
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
    newsitem = parser.getNewsItem()
    assert newsitem.get_attr('guid') == 'simplest-test'
    assert newsitem.get_attr('standard') == 'NewsML-G2'
    assert newsitem.get_attr('standardversion') == '2.29'
    assert newsitem.get_attr('conformance') == 'power'
```

## Testing

A very small unit test library is included.

Run it with:

    python setup.py test

## Release notes

* 0.1 - First release, pinned to Python 3 only (use pip >9.0 to ensure pip's
Python version requirement works properly)
