from typing import Any

import torch
from diffusers import DiffusionPipeline

from DashAI.back.core.schema_fields import (
    enum_field,
    float_field,
    int_field,
    schema_field,
)
from DashAI.back.core.schema_fields.base_schema import BaseSchema
from DashAI.back.models.image_generation_model import ImageGenerationModel


class ImageGenerationSchema(BaseSchema):
    """Schema for image generation models."""

    num_inference_steps: schema_field(
        int_field(ge=1),
        placeholder=5,
        description="The number of denoising steps. More steps usually lead to a higher quality image at the expense of slower inference.",
    )  # type: ignore
    guidance_scale: schema_field(
        float_field(ge=0.0),
        placeholder=7.5,
        description="Higher guidance scale encourages images that are closer to the prompt, usually at the expense of lower image quality.",
    )  # type: ignore
    device: schema_field(
        enum_field(enum=["cuda", "cpu"]),
        placeholder="cuda",
        description="Device to run the model on. CUDA is recommended for faster generation if available.",
    )  # type: ignore


class StableDiffusionModel(ImageGenerationModel):
    """Class for models associated to StableDiffusionProcess."""

    SCHEMA = ImageGenerationSchema

    def __init__(self, **kwargs):
        """Initialize the model."""
        kwargs = self.validate_and_transform(kwargs)
        self.model_name = "stabilityai/stable-diffusion-2-1"
        self.num_inference_steps = kwargs.pop("num_inference_steps")
        self.guidance_scale = kwargs.pop("guidance_scale")
        self.device = kwargs.pop("device")

        self.model = DiffusionPipeline.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32 if self.device == "cuda" else torch.float16,
        ).to(self.device)

    def generate(self, input: Any) -> Any:
        """Generate output from a generative model.

        input (Any): Input to the generative model.
        """
        image = self.model(
            input,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
        ).images[0]
        return image
