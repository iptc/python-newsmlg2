# Schemas used by the tests

`tests/test_schema_validation.py` validates every file in `tests/test_files`
against these schemas.

* `NewsML-G2_2.36-spec-All-Power.xsd`: from
  https://github.com/iptc/newsml-g2 (`specification/`)
* `xml.xsd`: the W3C schema for the `xml:` namespace, imported by the
  NewsML-G2 schema from the same folder

When the module moves to a new NewsML-G2 version, replace the NewsML-G2 schema
here and update `SCHEMA_FILE` in the test.
