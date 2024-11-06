from sklearn.feature_selection import (
    GenericUnivariateSelect as GenericUnivariateSelectOperation,
)

from DashAI.back.core.schema_fields import (
    schema_field,
    float_field,
    int_field,
    none_type,
    union_type,
    enum_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class GenericUnivariateSelectSchema(BaseSchema):
    # score_func: schema_field(
    #     string_field(), # callable
    #     "f_classif",
    #     "The scoring function to use.",
    # )  # type: ignore
    mode: schema_field(
        enum_field(["percentile", "k_best", "fpr", "fdr", "fwe"]),
        "percentile",
        "Select features according to a percentile of the highest scores.",
    )  # type: ignore
    param: schema_field(
        none_type(
            union_type(enum_field(["all"]), union_type(float_field(), int_field()))
        ),
        1e-5,
        "Parameter of the mode.",
    )  # type: ignore


class GenericUnivariateSelect(SklearnLikeConverter, GenericUnivariateSelectOperation):
    """SciKit-Learn's GenericUnivariateSelect wrapper for DashAI."""

    SCHEMA = GenericUnivariateSelectSchema
    DESCRIPTION = "Univariate feature selector with configurable strategy."
