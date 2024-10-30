from sklearn.cross_decomposition import PLSCanonical as PLSCanonicalOperation

from DashAI.back.core.schema_fields import (
    schema_field,
    int_field,
    enum_field,
    float_field,
    bool_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class PLSCanonicalSchema(BaseSchema):
    n_components: schema_field(
        int_field(ge=1),
        2,
        "Number of components to keep.",
    )  # type: ignore
    scale: schema_field(
        bool_field(),
        True,
        "Whether to scale the data.",
    )  # type: ignore
    algorithm: schema_field(
        enum_field(["nipals", "svd"]),
        "nipals",
        "Algorithm to use.",
    )  # type: ignore
    max_iter: schema_field(
        int_field(ge=1),
        500,
        "Maximum number of iterations to perform.",
    )  # type: ignore
    tol: schema_field(
        float_field(ge=0.0),
        1e-6,
        "Tolerance for the stopping condition.",
    )  # type: ignore
    copy: schema_field(
        bool_field(),
        True,
        "Whether to copy X and Y in fit before applying centering, and potentially scaling.",
    )  # type: ignore


class PLSCanonical(SklearnLikeConverter, PLSCanonicalOperation):
    """Scikit-learn"s PLSCanonical wrapper for DashAI."""

    SCHEMA = PLSCanonicalSchema
    DESCRIPTION = "Partial Least Squares transformer and regressor."
