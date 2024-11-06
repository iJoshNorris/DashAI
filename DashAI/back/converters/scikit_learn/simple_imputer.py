from sklearn.impute import SimpleImputer as SimpleImputerOperation

from DashAI.back.core.schema_fields import (
    schema_field,
    string_field,
    union_type,
    enum_field,
    int_field,
    float_field,
    string_field,
    none_type,
    bool_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class SimpleImputerSchema(BaseSchema):
    missing_values: schema_field(
        none_type(
            union_type(int_field(), union_type(float_field(), string_field()))
        ),  # int, float, str, np.nan, None or pandas.NA
        None,  # np.nan,
        "The placeholder for the missing values.",
    )  # type: ignore
    strategy: schema_field(
        enum_field(["mean", "median", "most_frequent", "constant"]),
        "mean",
        "The imputation strategy.",
    )  # type: ignore
    fill_value: schema_field(
        none_type(union_type(int_field(), union_type(float_field(), string_field()))),
        None,
        "The value to replace missing values with.",
    )  # type: ignore
    # Deprecated since version 1.1
    verbose: schema_field(
        int_field(),
        0,
        "Controls the verbosity of the imputer.",
    )  # type: ignore
    copy: schema_field(
        bool_field(),
        True,
        "If True, a copy of X will be created.",
    )  # type: ignore
    add_indicator: schema_field(
        bool_field(),
        False,
        "If True, a MissingIndicator transform will stack onto output.",
    )  # type: ignore
    keep_empty_features: schema_field(
        bool_field(),
        False,
        "If True, empty features will be kept.",
    )  # type: ignore


class SimpleImputer(SklearnLikeConverter, SimpleImputerOperation):
    """SciKit-Learn's SimpleImputer wrapper for DashAI."""

    SCHEMA = SimpleImputerSchema
    DESCRIPTION = (
        "Univariate imputer for completing missing values with simple strategies."
    )
