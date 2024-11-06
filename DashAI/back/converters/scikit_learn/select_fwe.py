from sklearn.feature_selection import (
    SelectFwe as SelectFweOperation,
)

from DashAI.back.core.schema_fields import (
    schema_field,
    float_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class SelectFweSchema(BaseSchema):
    # score_func: schema_field(
    #     string_field(),  # callable
    #     "f_classif",
    #     "The scoring function to use.",
    # )  # type: ignore
    alpha: schema_field(
        float_field(ge=0.0, le=1.0),
        0.05,
        "The highest uncorrected p-value for features to be kept.",
    )  # type: ignore


class SelectFwe(SklearnLikeConverter, SelectFweOperation):
    """Scikit-learn's SelectFwe wrapper for DashAI."""

    SCHEMA = SelectFweSchema
    DESCRIPTION = "Filter: Select features according to a family-wise error rate test."
