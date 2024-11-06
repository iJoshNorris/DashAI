from sklearn.feature_extraction.text import (
    TfidfTransformer as TfidfTransformerOperation,
)

from DashAI.back.core.schema_fields import (
    schema_field,
    bool_field,
    enum_field,
    none_type,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class TfidfTransformerSchema(BaseSchema):
    norm: schema_field(
        none_type(enum_field(["l1", "l2"])),
        "l2",
        "Norm used to normalize term vectors.",
    )  # type: ignore
    use_idf: schema_field(
        bool_field(),
        True,
        "Enable inverse-document-frequency reweighting.",
    )  # type: ignore
    smooth_idf: schema_field(
        bool_field(),
        True,
        "Smooth idf weights by adding one to document frequencies, as if an extra document was seen containing every term in the collection exactly once.",
    )  # type: ignore
    sublinear_tf: schema_field(
        bool_field(),
        False,
        "Apply sublinear tf scaling, i.e., replace tf with 1 + log(tf).",
    )  # type: ignore


class TfidfTransformer(SklearnLikeConverter, TfidfTransformerOperation):
    """Scikit-learn's TfidfTransformer wrapper for DashAI."""

    SCHEMA = TfidfTransformerSchema
    DESCRIPTION = (
        "Transform a count matrix to a normalized tf or tf-idf representation."
    )
