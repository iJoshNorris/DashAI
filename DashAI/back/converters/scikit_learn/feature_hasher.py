from sklearn.feature_extraction import FeatureHasher as FeatureHasherOperation

from DashAI.back.core.schema_fields import (
    schema_field,
    int_field,
    bool_field,
    enum_field,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class FeatureHasherSchema(BaseSchema):
    n_features: schema_field(
        int_field(ge=1),
        2**20,
        "The number of features (columns) in the output matrix.",
    )  # type: ignore
    input_type: schema_field(
        enum_field(["dict", "pair", "string"]),
        "dict",
        "The input type. 'dict' means that the input will be a list of mappings (dict-like objects) of feature names to feature values. 'pair' means that the input will be a list of pairs of feature names and feature values.",
    )  # type: ignore
    # dtype: schema_field(
    #     none_type(enum_field(["np.float32", "np.float64"])), # numpy dtype
    #     np.float64,
    #     "The type of feature values.",
    # )  # type: ignore
    alternate_sign: schema_field(
        bool_field(),
        True,
        "Whether to alternate the sign of the hash value for each feature.",
    )  # type: ignore


class FeatureHasher(SklearnLikeConverter, FeatureHasherOperation):
    """Scikit-learn's FeatureHasher wrapper for DashAI."""

    SCHEMA = FeatureHasherSchema
    DESCRIPTION = (
        "This class turns sequences of symbolic feature names (strings) into scipy.sparse matrices, "
        "using a hash function to compute the matrix column corresponding to a name. The hash function "
        "employed is the signed 32-bit version of Murmurhash3."
    )
