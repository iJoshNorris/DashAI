from typing import Any
from llama_cpp import Llama

from DashAI.back.core.schema_fields import (
    BaseSchema,
    int_field,
    schema_field,
)
from DashAI.back.models.base_generative_model import BaseGenerativeModel


class LlamaSchema(BaseSchema):
    """Schema for Llama text generation model."""

    max_tokens: schema_field(
        int_field(ge=1),
        placeholder=100,
        description="Maximum number of tokens to generate.",
    )  # type: ignore


class LLMGenerationModel(BaseGenerativeModel):
    """Llama model for text generation using llama.cpp library."""

    SCHEMA = LlamaSchema

    def __init__(self, **kwargs):
        kwargs = self.validate_and_transform(kwargs)
        self.model_id = "Qwen/Qwen2-0.5B-Instruct-GGUF"  # Repositorio de Hugging Face
        self.filename = "*q8_0.gguf"  # Archivo del modelo
        self.max_tokens = kwargs.pop("max_tokens", 100)

        # Descargar y cargar el modelo desde Hugging Face
        self.model = Llama.from_pretrained(
            repo_id=self.model_id, filename=self.filename, verbose=True
        )

    def generate(self, prompt: str) -> str:
        """Generate text based on prompts."""
        output = self.model(
            f"Q: {prompt} A:", max_tokens=self.max_tokens, stop=["\n", "Q:"], echo=True
        )
        return output["choices"][0]["text"]

    def process_output(self, out: Any, file_name: str, path: str) -> str:
        """Process the output of a generative model.

        file_name (Str): Indicates the name of the file.
        path (Str): Indicates the path where the output will be stored.
        """
        save_dir = path / "llm-models"
        if not save_dir.exists():
            save_dir.mkdir(parents=True)

        text_path = save_dir / f"{file_name}.txt"

        # Save the output to a text file
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(str(out))

        return text_path

    @classmethod
    def load(cls, filename: str) -> "LLMGenerationModel":
        # Load the model from a given path
        return cls(model_path=filename)
