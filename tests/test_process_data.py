import pytest
from processing.process_data import *

@pytest.mark.parametrize('path, expect', [
                         ('./tests/root_file.root', pd.DataFrame({'foo': range(5), 'bar':range(5, 10)})),
                         ('./tests/pkl_file.pkl', pd.DataFrame({'foo': range(5), 'bar':range(5, 10)}))]
                         )
def test_convert_to_df(path, expect):
    output = convert_to_df(path)
    assert output.columns.all() == expect.columns.all()
    assert output.all().all() == expect.all().all()

@pytest.mark.parametrize('path, expected_error', [
                         ('./nothere.root', FileNotFoundError),
                         ('./nothere.pkl', FileNotFoundError)])
def test_convert_to_df_error(path, expected_error):
    with pytest.raises(expected_error):
        output = convert_to_df(path)
