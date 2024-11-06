from DashAI.back.models.generative_model import GenerativeModel


class ImageGenerationModel(GenerativeModel):
    """Class for models associated to ImageGenerationProcess."""

    COMPATIBLE_COMPONENTS = ["ImageGenerationProcess"]
