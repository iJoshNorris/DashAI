import json

from sklearn.svm import SVC as _SVC

from DashAI.back.models.scikit_learn.sklearn_like_model import SklearnLikeModel
from DashAI.back.models.tabular_classification_model import TabularClassificationModel


class SVC(TabularClassificationModel, SklearnLikeModel, _SVC):
    """
    Support vector machine. Supervised learning algorithm that separates
    two classes in two spaces by means of a hyperplane. This hyperplane is
    defined as a vector called support vector.
    """

    MODEL = "SVC"

    @classmethod
    def get_schema(cls):
        with open(
            f"DashAI/back/models/parameters/models_schemas/{cls.MODEL}.json"
        ) as f:
            cls.SCHEMA = json.load(f)
