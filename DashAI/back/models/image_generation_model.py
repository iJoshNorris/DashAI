from typing import Any

import diffusers
import torch
from diffusers import DiffusionPipeline

from DashAI.back.core.schema_fields import (
    BaseSchema,
    enum_field,
    float_field,
    int_field,
    schema_field,
)
from DashAI.back.models.base_generative_model import BaseGenerativeModel


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


class ImageGenerationModel(BaseGenerativeModel):
    """Class for models associated to ImageGenerationProcess."""

    SCHEMA = ImageGenerationSchema

    def __init__(self, **kwargs):
        kwargs = self.validate_and_transform(kwargs)
        self.model_id = "stabilityai/stable-diffusion-2-1"
        self.num_inference_steps = kwargs.pop("num_inference_steps")
        self.guidance_scale = kwargs.pop("guidance_scale")
        self.device = kwargs.pop("device")

        self.pipeline = DiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
        ).to(self.device)

    def generate(self, input: Any) -> Any:
        """Generate output from a generative model.

        input (Any): Input to the generative model.
        """
        image = self.pipeline(
            input,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=self.guidance_scale,
        ).images[0]
        return image

    def process_output(self, out: Any, file_name: str, path: str) -> str:
        """Process the output of a generative model.

        file_name (Str): Indicates the name of the file.
        path (Str): Indicates the path where the output will be stored.
        """
        # TODO: SANITIZE THE IMAGE FILE
        save_dir = path / "stable-diffusion-images"
        if not save_dir.exists():
            save_dir.mkdir(parents=True)

        image_path = save_dir / f"{file_name}.png"

        # Save the image
        out.save(image_path, format="PNG")

        return image_path
