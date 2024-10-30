from sklearn.cross_decomposition import CCA as CCAOperation

from DashAI.back.core.schema_fields import (
    schema_field,
    int_field,
    float_field,
    bool_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class CCASchema(BaseSchema):
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
        "Whether to copy X and Y or perform in-place normalization.",
    )  # type: ignore


class CCA(SklearnLikeConverter, CCAOperation):
    """Scikit-learn's CCA wrapper for DashAI."""

    SCHEMA = CCASchema
    DESCRIPTION = "Canonical Correlation Analysis, also known as 'Mode B' PLS."
