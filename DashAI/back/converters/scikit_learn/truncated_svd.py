from sklearn.decomposition import TruncatedSVD as TruncatedSVDOperation

from DashAI.back.core.schema_fields import (
    schema_field,
    int_field,
    none_type,
    float_field,
    enum_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class TruncatedSVDSchema(BaseSchema):
    n_components: schema_field(
        int_field(gt=0),
        2,
        "Desired dimensionality of output data.",
    )  # type: ignore
    algorithm: schema_field(
        enum_field(["arpack", "randomized"]),
        "randomized",
        "SVD solver to use.",
    )  # type: ignore
    n_iter: schema_field(
        int_field(gt=0),
        5,
        "Number of iterations for randomized SVD solver.",
    )  # type: ignore
    n_oversamples: schema_field(
        int_field(gt=0),
        10,
        "Number of power iterations used in randomized SVD solver.",
    )  # type: ignore
    power_iteration_normalizer: schema_field(
        enum_field(["auto", "QR", "LU", "none"]),
        "auto",
        "Method to normalize the eigenvectors.",
    )  # type: ignore
    random_state: schema_field(
        none_type(int_field()),  # int, RandomState instance or None
        None,
        "Used during randomized svd. Pass an int for reproducible results across multiple function calls.",
    )  # type: ignore
    tol: schema_field(
        float_field(ge=0),
        0.0,
        "Tolerance for ARPACK.",
    )  # type: ignore


class TruncatedSVD(SklearnLikeConverter, TruncatedSVDOperation):
    """Scikit-learn's TruncatedSVD wrapper for DashAI."""

    SCHEMA = TruncatedSVDSchema
    DESCRIPTION = (
        "This transformer performs linear dimensionality reduction by means of truncated singular value decomposition (SVD). "
        "Contrary to PCA, this estimator does not center the data before computing the singular value decomposition. "
        "This means it can work with sparse matrices efficiently."
    )
