from sklearn.preprocessing import LabelEncoder as LabelEncoderOperation

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class LabelEncoderSchema(BaseSchema):
    pass


class LabelEncoder(SklearnLikeConverter, LabelEncoderOperation):
    """Scikit-learn's LabelEncoder wrapper for DashAI."""

    SCHEMA = LabelEncoderSchema
    DESCRIPTION = "Encode target labels with value between 0 and n_classes-1."
