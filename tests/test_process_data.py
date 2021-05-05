import pytest
from utils.process_data import *

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

@pytest.mark.parametrize('variables, constraints, expect', [
                         (['M*MeV'], ['OnlyD'], ['M*MeV', 'OnlyD#M*MeV']), 
                         (['M*MeV', 'P*MeV'], ['OnlyD', 'BandDs'], ['M*MeV', 'OnlyD#M*MeV', 'BandDs#M*MeV','P*MeV', 'OnlyD#P*MeV', 'BandDs#P*MeV'])])
def test_extract_constraints(variables, constraints, expect):
    output = extract_constraints(variables, constraints)
    assert output == expect

@pytest.mark.parametrize('df, exclude, expect', [
                         (pd.DataFrame({'_foo_': range(5), '_bar_':range(5, 10)}), ['bar'], pd.DataFrame({'_foo_': range(5)})),
                         ((pd.DataFrame({'_foo_': range(5), '_bar_':range(5, 10)}), ['foo'], pd.DataFrame({'_bar_': range(5, 10)})))])
def test_exclude_constraints(df, exclude, expect):
    output = exclude_constraints(df, exclude)
    assert output.values.all() == expect.values.all()
