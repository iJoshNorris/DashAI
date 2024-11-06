from sklearn.impute import MissingIndicator as MissingIndicatorOperation

from DashAI.back.core.schema_fields import (
    schema_field,
    bool_field,
    none_type,
    int_field,
    float_field,
    string_field,
    union_type,
    enum_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class MissingIndicatorSchema(BaseSchema):
    missing_values: schema_field(
        none_type(
            union_type(int_field(), union_type(float_field(), string_field()))
        ),  # int, float, str, np.nan or None
        None,  # np.nan,
        "The placeholder for the missing values.",
    )  # type: ignore
    features: schema_field(
        enum_field(["missing-only", "all"]),
        None,
        "The features to consider for missing values.",
    )  # type: ignore
    sparse: schema_field(
        union_type(bool_field(), enum_field(["auto"])),
        "auto",
        "Whether the output should be a sparse matrix.",
    )  # type: ignore
    error_on_new: schema_field(
        bool_field(),
        True,
        "Whether to raise an error on new missing values.",
    )  # type: ignore


class MissingIndicator(SklearnLikeConverter, MissingIndicatorOperation):
    """Scikit-learn's MissingIndicator wrapper for DashAI."""

    SCHEMA = MissingIndicatorSchema
    DESCRIPTION = "Binary indicators for missing values."
