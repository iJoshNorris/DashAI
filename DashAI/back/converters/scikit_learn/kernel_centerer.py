from sklearn.preprocessing import KernelCenterer as KernelCentererOperation

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class KernelCentererSchema(BaseSchema):
    pass


class KernelCenterer(SklearnLikeConverter, KernelCentererOperation):
    """Scikit-learn's KernelCenterer wrapper for DashAI."""

    SCHEMA = KernelCentererSchema
    DESCRIPTION = "Center a kernel matrix."
