from DashAI.back.models.generative_model import GenerativeModel


class ImageClassificationModel(GenerativeModel):
    """Class for models associated to ImageClassificationTask."""

    COMPATIBLE_COMPONENTS = ["ImageClassificationTask"]
