from sklearn.feature_selection import (
    SelectKBest as SelectKBestOperation,
)

from DashAI.back.core.schema_fields import (
    schema_field,
    union_type,
    enum_field,
    int_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class SelectKBestSchema(BaseSchema):
    # score_func: schema_field(
    #     string_field(),  # callable
    #     "f_classif",
    #     "The scoring function to use.",
    # )  # type: ignore
    k: schema_field(
        union_type(enum_field(["all"]), int_field(ge=1)),
        10,
        "Number of top features to select.",
    )  # type: ignore


class SelectKBest(SklearnLikeConverter, SelectKBestOperation):
    """SciKit-Learn's SelectKBest wrapper for DashAI."""

    SCHEMA = SelectKBestSchema
    DESCRIPTION = "Select features according to the k highest scores."
