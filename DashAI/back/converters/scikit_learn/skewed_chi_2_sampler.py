from sklearn.kernel_approximation import SkewedChi2Sampler as SkewedChi2SamplerOperation

from DashAI.back.converters.sklearn_wrapper import SklearnWrapper
from DashAI.back.core.schema_fields import (
    float_field,
    int_field,
    none_type,
    schema_field,
)
from DashAI.back.core.schema_fields.base_schema import BaseSchema


class SkewedChi2SamplerSchema(BaseSchema):
    skewedness: schema_field(
        float_field(gt=0),
        1.0,
        "The skewedness parameter of the chi-squared kernel.",
    )  # type: ignore
    n_components: schema_field(
        int_field(ge=1),
        100,
        "Number of Monte Carlo samples per original feature. Equals the dimensionality of the computed feature space.",
    )  # type: ignore
    random_state: schema_field(
        none_type(int_field()),  # int, RandomState instance or None
        None,
        "Pseudo-random number generator to control the generation of the random weights and random offset when fitting the training data. Pass an int for reproducible output across multiple function calls.",
    )  # type: ignore


class SkewedChi2Sampler(SklearnWrapper, SkewedChi2SamplerOperation):
    """Scikit-learn's SkewedChi2Sampler wrapper for DashAI."""

    SCHEMA = SkewedChi2SamplerSchema
    DESCRIPTION = "Approximates the feature map of a chi-squared kernel by Monte Carlo approximation of its Fourier transform."
