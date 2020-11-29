from tests.context import dataset
import pandas as pd
import lxml.etree as et


def test_metadata_processing(capsys, example_fixture):
    # pylint: disable=W0612,W0613

    df = pd.DataFrame({
        "web-scraper-order": ["aaa"],
        "web-scraper-start-url": ["bbb"],
        "article": ["ccc"],
        "article-href": ["https://example.com/file.name"],
        "title": ["      Title    123     . $$$    "],
        "authors": ["Person A and Person B"],
        "body": ['[{"body":"Abstract: first paragraph"},{"body": "Second paragraph"},' \
                '{"body":"Category / Keywords: keyword1 / keyword2, keyword3"},' \
                '{"body":"aaa"},{"body":"bbb"},{"body":"Available format(s): PDF"},{"body":""}]'],
        })

    

    main = dataset.Main()
    processed = main.process(df)

    assert len(processed.columns) == 5
    assert processed['title'][0] == 'Title 123 . $$$'
    assert processed['authors'][0] == 'Person A and Person B'
    assert processed['abstract'][0] == 'first paragraphSecond paragraph'
    assert processed['keywords'][0] == 'keyword1 / keyword2, keyword3'
    assert processed['url'][0] == 'https://example.com/file.name.pdf'


def test_citation_processing(capsys, example_fixture):
    xml_content = """ 
<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Archiving and Interchange DTD v1.0 20120330//EN" "JATS-archivearticle1.dtd">
<article xmlns:xlink="http://www.w3.org/1999/xlink">
  <front>
    <journal-meta />
    <article-meta>
      <title-group>
        <article-title>      Title   123 </article-title>
      </title-group>
    </article-meta>
    <article-title>ref1</article-title>
  </front>
  <article-title>ref2    </article-title>
</article>
"""

    main = dataset.Main()
    dep = main.process_citation(et.fromstring(xml_content))

    expected = ["Title 123", "ref1", "ref2"]
    for (got, want) in zip(dep, expected):
        assert got == want
