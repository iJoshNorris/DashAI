from sklearn.feature_selection import (
    SelectPercentile as SelectPercentileOperation,
)

from DashAI.back.core.schema_fields import (
    schema_field,
    int_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class SelectPercentileSchema(BaseSchema):
    # score_func: schema_field(
    #     string_field(),  # callable
    #     "f_classif",
    #     "The scoring function to use.",
    # )  # type: ignore
    percentile: schema_field(
        int_field(ge=1, le=100),
        10,
        "Percent of features to keep.",
    )  # type: ignore


class SelectPercentile(SklearnLikeConverter, SelectPercentileOperation):
    """SciKit-Learn's SelectPercentile wrapper for DashAI."""

    SCHEMA = SelectPercentileSchema
    DESCRIPTION = "Select features according to a percentile of the highest scores."
