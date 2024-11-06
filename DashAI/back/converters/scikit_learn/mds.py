from sklearn.manifold import MDS as MDSOperation

from DashAI.back.core.schema_fields import (
    schema_field,
    int_field,
    float_field,
    none_type,
    enum_field,
    bool_field,
    union_type,
    enum_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class MDSSchema(BaseSchema):
    n_components: schema_field(
        int_field(ge=1),
        2,
        "Number of dimensions in which to immerse the dissimilarities.",
    )  # type: ignore
    metric: schema_field(
        bool_field(),
        True,
        "If True, perform metric MDS; otherwise, perform nonmetric MDS.",
    )  # type: ignore
    n_init: schema_field(
        int_field(ge=1),
        4,
        "Number of times the SMACOF algorithm will be run with different initializations.",
    )  # type: ignore
    max_iter: schema_field(
        int_field(ge=1),
        300,
        "Maximum number of iterations of the SMACOF algorithm for a single run.",
    )  # type: ignore
    verbose: schema_field(
        int_field(ge=0),
        0,
        "Level of verbosity.",
    )  # type: ignore
    eps: schema_field(
        float_field(gt=0),
        1e-3,
        "Relative tolerance with respect to stress at which to declare convergence.",
    )  # type: ignore
    n_jobs: schema_field(
        none_type(int_field()),
        None,
        "The number of jobs to use for the computation.",
    )  # type: ignore
    random_state: schema_field(
        none_type(int_field()),  # int, RandomState instance or None
        None,
        "Determines the random number generator used to initialize the centers. Pass an int for reproducible output across multiple function calls.",
    )  # type: ignore
    dissimilarity: schema_field(
        enum_field(["euclidean", "precomputed"]),
        "euclidean",
        "Dissimilarity measure to use.",
    )  # type: ignore
    normalized_stress: schema_field(
        union_type(bool_field(), enum_field(["auto"])),
        False,
        "Whether to compute normalized stress.",
    )  # type: ignore


class MDS(SklearnLikeConverter, MDSOperation):
    """Scikit-learn's MDS wrapper for DashAI."""

    SCHEMA = MDSSchema
    DESCRIPTION = "Multidimensional scaling."
