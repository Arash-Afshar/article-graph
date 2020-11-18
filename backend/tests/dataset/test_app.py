from tests.context import dataset


def test_app(capsys, example_fixture):
    # pylint: disable=W0612,W0613
    dataset.Main.run()
    captured = capsys.readouterr()

    assert "Hello World..." in captured.out
