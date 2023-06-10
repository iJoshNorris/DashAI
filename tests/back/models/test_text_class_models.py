import io
import shutil

import pytest
from datasets import DatasetDict
from sklearn.exceptions import NotFittedError
from starlette.datastructures import UploadFile

from DashAI.back.dataloaders.classes.dataloader import to_dashai_dataset
from DashAI.back.dataloaders.classes.json_dataloader import JSONDataLoader
from DashAI.back.models.hugging_face.distilbert_transformer import DistilBertTransformer
from DashAI.back.tasks.text_classification_task import TextClassificationTask


@pytest.fixture(scope="module", name="load_dashaidataset")
def fixture_load_dashaidataset():
    test_dataset_path = "tests/back/models/ImdbSentimentDataset.json"
    dataloader_test = JSONDataLoader()
    params = {"data_key": "data"}
    with open(test_dataset_path, "r", encoding="utf8") as file:
        json_data = file.read()
        json_binary = io.BytesIO(bytes(json_data, encoding="utf8"))
        file = UploadFile(json_binary)

    datasetdict = dataloader_test.load_data("tests/back/models", params, file=file)
    datasetdict["train"] = datasetdict["train"].select(range(100))
    inputs_columns = ["text"]
    outputs_columns = ["class"]
    datasetdict = to_dashai_dataset(datasetdict, inputs_columns, outputs_columns)
    outputs_columns = datasetdict["train"].outputs_columns
    separate_datasetdict = dataloader_test.split_dataset(
        datasetdict, 0.7, 0.1, 0.2, class_column=outputs_columns[0]
    )

    text_task = TextClassificationTask.create()
    separate_datasetdict = text_task.prepare_for_task(separate_datasetdict)
    text_task.validate_dataset_for_task(separate_datasetdict, "IMDBDataset")
    yield separate_datasetdict


def test_fit_text_class_model(load_dashaidataset: DatasetDict):
    distilbert = DistilBertTransformer()
    distilbert.fit(load_dashaidataset)
    assert distilbert.fitted is True


def test_predict_text_class_model(load_dashaidataset: DatasetDict):
    distilbert = DistilBertTransformer()
    distilbert.fit(load_dashaidataset)
    pred_distilbert = distilbert.predict(load_dashaidataset)
    assert load_dashaidataset["test"].num_rows == len(pred_distilbert)


def test_not_fitted_text_class_model(load_dashaidataset: DatasetDict):
    distilbert = DistilBertTransformer()

    with pytest.raises(NotFittedError):
        distilbert.predict(load_dashaidataset)


def test_save_and_load_model(load_dashaidataset: DatasetDict):
    distilbert = DistilBertTransformer()
    distilbert.fit(load_dashaidataset)
    distilbert.save("tests/back/models/distilbert_model")
    saved_model_distilbert = DistilBertTransformer.load(
        "tests/back/models/distilbert_model"
    )
    assert saved_model_distilbert.fitted is True
    pred_distilbert = saved_model_distilbert.predict(load_dashaidataset)
    assert load_dashaidataset["test"].num_rows == len(pred_distilbert)
    shutil.rmtree("tests/back/models/distilbert_model", ignore_errors=True)


def test_get_schema_from_model():
    model_schema = DistilBertTransformer.get_schema()
    assert type(model_schema) is dict
    assert "type" in model_schema.keys()
    assert model_schema["type"] == "object"
    assert "properties" in model_schema.keys()
    assert type(model_schema["properties"]) is dict
