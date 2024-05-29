import logging
from typing import Dict

from kink import Container, di
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from DashAI.back.dataloaders import CSVDataLoader, ImageDataLoader, JSONDataLoader
from DashAI.back.dependencies.database.sqlite_database import setup_sqlite_db
from DashAI.back.dependencies.job_queues import BaseJobQueue, SimpleJobQueue
from DashAI.back.dependencies.registry import ComponentRegistry
from DashAI.back.job.model_job import ModelJob
from DashAI.back.metrics import F1, Accuracy, Bleu, Precision, Recall
from DashAI.back.models import (
    SVC,
    DecisionTreeClassifier,
    DistilBertTransformer,
    DummyClassifier,
    HistGradientBoostingClassifier,
    KNeighborsClassifier,
    LogisticRegression,
    OpusMtEnESTransformer,
    RandomForestClassifier,
    ViTTransformer,
)
from DashAI.back.tasks import (
    ImageClassificationTask,
    TabularClassificationTask,
    TextClassificationTask,
    TranslationTask,
)

logger = logging.getLogger(__name__)


INITIAL_COMPONENTS = [
    # Tasks
    TabularClassificationTask,
    TextClassificationTask,
    TranslationTask,
    ImageClassificationTask,
    # Models
    SVC,
    DecisionTreeClassifier,
    DummyClassifier,
    HistGradientBoostingClassifier,
    KNeighborsClassifier,
    LogisticRegression,
    RandomForestClassifier,
    DistilBertTransformer,
    ViTTransformer,
    OpusMtEnESTransformer,
    # Dataloaders
    CSVDataLoader,
    JSONDataLoader,
    ImageDataLoader,
    # Metrics
    F1,
    Accuracy,
    Precision,
    Recall,
    Bleu,
    # Jobs
    ModelJob,
]


def build_container(config: Dict[str, str]) -> Container:
    """
    Creates a dependency injection container for the application.

    Parameters
    ----------
    config : Dict[str, str]
        A dictionary containing configuration settings.

    Returns
    -------
    Container
        A dependency injection container instance populated with
        essential services. These services include:
            * 'config': The provided configuration dictionary.
            * Engine: The created SQLAlchemy engine for the SQLite database.
            * sessionmaker: A session factory for creating database sessions.
            * ComponentRegistry: The app component registry.
            * BaseJobQueue: The app job queue.
    """
    engine, session_factory = setup_sqlite_db(config)

    di["config"] = config
    di[Engine] = engine
    di[sessionmaker] = session_factory
    di[ComponentRegistry] = ComponentRegistry(initial_components=INITIAL_COMPONENTS)
    di[BaseJobQueue] = SimpleJobQueue()

    return di
