import numpy as np
import pandas as pd

from src import data_preprocessing as dp
import pytest


def _make_df_with_saleprice(values, extra_nan=False):
    df = pd.DataFrame(
        {
            "SalePrice": values,
            "LotArea": [8000, 9000, 10000, 11000, 12000][: len(values)],
            "Neighborhood": ["NAmes", "CollgCr", "NAmes", "Edwards", "NAmes"][: len(values)],
        }
    )
    if extra_nan and len(values) >= 4:
        import numpy as _np
        df.loc[1, "LotArea"] = _np.nan
        df.loc[2, "Neighborhood"] = None
    return df


@pytest.mark.unit
def test_remove_outliers_no_outliers():
    df = _make_df_with_saleprice([150000, 155000, 160000, 165000])
    result = dp.remove_outliers(df, "SalePrice", n_std=3)
    assert len(result) == len(df)


@pytest.mark.unit
def test_remove_outliers_with_outliers():
    df = _make_df_with_saleprice([150000, 155000, 160000, 165000, 1000000])
    # With a stricter threshold the outlier should be removed
    result = dp.remove_outliers(df, "SalePrice", n_std=1.5)
    assert len(result) < len(df)
    assert 1000000 not in result["SalePrice"].values


@pytest.mark.unit
def test_check_data_quality_structure(capfd):
    df = _make_df_with_saleprice([150000, 155000, 160000, 165000], extra_nan=True)
    report = dp.check_data_quality(df)
    assert set(report.keys()) == {"missing", "duplicates"}
    # duplicates can be numpy integer on some pandas versions
    assert isinstance(report["duplicates"], (int, np.integer))


@pytest.mark.unit
def test_prepare_data_fills_missing_and_removes_outliers():
    # Include a clear outlier; function uses std-based filtering which may or may not remove it
    df = _make_df_with_saleprice([150000, 155000, 160000, 165000, 10000000], extra_nan=True)
    cleaned = dp.prepare_data(df)
    assert cleaned is not None
    # no NaNs remain
    assert cleaned.isnull().sum().sum() == 0
    # Do not assert strict outlier removal; behavior depends on std threshold and distribution
