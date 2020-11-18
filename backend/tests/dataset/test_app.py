from tests.context import dataset
import pandas as pd


def test_app(capsys, example_fixture):
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
