from sklearn.decomposition import SparseCoder as SparseCoderOperation

from DashAI.back.core.schema_fields import (
    schema_field,
    int_field,
    float_field,
    enum_field,
    none_type,
    bool_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class SparseCoderSchema(BaseSchema):
    # dictionary: schema_field(
    #     none_type(),  # ndarray of shape (n_components, n_features)
    #     None,
    #     "The dictionary atoms used for sparse coding. Lines are assumed to be normalized to unit norm.",
    # )  # type: ignore
    transform_algorithm: schema_field(
        enum_field(["lasso_lars", "lasso_cd", "lars", "omp", "threshold"]),
        "omp",
        "Algorithm used to transform the data.",
    )  # type: ignore
    transform_n_nonzero_coefs: schema_field(
        none_type(int_field()),
        None,
        "Number of non-zero coefficients to target in the coding.",
    )  # type: ignore
    transform_alpha: schema_field(
        none_type(float_field()), None, "Sparsity controlling parameter."
    )  # type: ignore
    split_sign: schema_field(
        bool_field(),
        False,
        "Whether to split the sparse coefficients into negative and positive parts.",
    )  # type: ignore
    n_jobs: schema_field(
        none_type(int_field()), None, "Number of parallel jobs to run."
    )  # type: ignore
    positive_code: schema_field(
        bool_field(),
        False,
        "Whether to enforce positivity on the sparse code.",
    )  # type: ignore
    transform_max_iter: schema_field(
        int_field(gt=0),
        1000,
        "Maximum number of iterations to perform.",
    )  # type: ignore


class SparseCoder(SklearnLikeConverter, SparseCoderOperation):
    """Scikit-learn's SparseCoder wrapper for DashAI."""

    SCHEMA = SparseCoderSchema
    DESCRIPTION = (
        "Finds a sparse representation of data against a fixed, precomputed dictionary."
    )
