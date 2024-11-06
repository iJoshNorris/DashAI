from sklearn.kernel_approximation import (
    PolynomialCountSketch as PolynomialCountSketchOperation,
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
    gamma: schema_field(
        float_field(gt=0),
        1.0,
        "Parameter of the polynomial kernel whose feature map will be approximated.",
    )  # type: ignore
    degree: schema_field(
        int_field(ge=1),
        2,
        "Degree of the polynomial kernel whose feature map will be approximated.",
    )  # type: ignore
    coef0: schema_field(
        int_field(),
        0,
        "Constant term of the polynomial kernel whose feature map will be approximated.",
    )  # type: ignore
    n_components: schema_field(
        int_field(ge=1),
        100,
        "The number of features to construct.",
    )  # type: ignore
    random_state: schema_field(
        none_type(int_field()),  # int, RandomState instance or None
        None,
        "Determines random number generation for indexHash and bitHash initialization. Pass an int for reproducible results across multiple function calls.",
    )  # type: ignore


class PolynomialCountSketch(SklearnLikeConverter, PolynomialCountSketchOperation):
    """Scikit-learn's PolynomialCountSketch wrapper for DashAI."""

    SCHEMA = AdditiveChi2SamplerSchema
    DESCRIPTION = "Polynomial kernel approximation via Tensor Sketch."
