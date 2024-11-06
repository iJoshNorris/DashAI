from sklearn.feature_selection import (
    VarianceThreshold as VarianceThresholdOperation,
)

from DashAI.back.core.schema_fields import (
    schema_field,
    float_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class VarianceThresholdSchema(BaseSchema):
    threshold: schema_field(
        float_field(ge=0.0),
        0.0,
        "Features with a variance lower than this threshold will be removed.",
    )  # type: ignore


class VarianceThreshold(SklearnLikeConverter, VarianceThresholdOperation):
    """Scikit-learn's VarianceThreshold wrapper for DashAI."""

    SCHEMA = VarianceThresholdSchema
    DESCRIPTION = "Feature selector that removes all low-variance features."
