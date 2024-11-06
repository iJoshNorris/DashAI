from sklearn.kernel_approximation import (
    AdditiveChi2Sampler as AdditiveChi2SamplerOperation,
)

from DashAI.back.core.schema_fields import (
    schema_field,
    int_field,
    float_field,
    none_type,
)

from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.converters.scikit_learn.sklearn_like_converter import (
    SklearnLikeConverter,
)


class AdditiveChi2SamplerSchema(BaseSchema):
    sample_steps: schema_field(
        int_field(ge=1),
        2,
        "The number of sample steps (shuffling) to perform.",
    )  # type: ignore
    sample_interval: schema_field(
        none_type(float_field(ge=1.0)),
        None,
        "The number of samples to generate between each original sample.",
    )  # type: ignore


class AdditiveChi2Sampler(SklearnLikeConverter, AdditiveChi2SamplerOperation):
    """Scikit-learn's AdditiveChi2Sampler wrapper for DashAI."""

    SCHEMA = AdditiveChi2SamplerSchema
    DESCRIPTION = "Uses sampling the fourier transform of the kernel characteristic at regular intervals."
