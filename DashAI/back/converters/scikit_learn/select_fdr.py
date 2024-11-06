from sklearn.feature_selection import (
    SelectFdr as SelectFdrOperation,
)

from DashAI.back.core.schema_fields import (
    schema_field,
    float_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class SelectFdrSchema(BaseSchema):
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


class SelectFdr(SklearnLikeConverter, SelectFdrOperation):
    """SciKit-Learn's SelectFdr wrapper for DashAI."""

    SCHEMA = SelectFdrSchema
    DESCRIPTION = "Filter: Select features according to a false discovery rate test."
