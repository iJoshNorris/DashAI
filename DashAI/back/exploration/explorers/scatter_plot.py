import os
import pathlib
import pickle

import plotly.express as px
from beartype.typing import Any, Dict, List
from plotly.graph_objs import Figure

from DashAI.back.core.schema_fields import none_type, schema_field, string_field
from DashAI.back.dataloaders.classes.dashai_dataset import (  # ClassLabel, Value,
    DashAIDataset,
    DatasetDict,
)
from DashAI.back.dependencies.database.models import Exploration, Explorer
from DashAI.back.exploration.base_explorer import BaseExplorer, BaseExplorerSchema


class ScatterPlotSchema(BaseExplorerSchema):
    """
    ScatterPlotSchema is an explorer that returns a scatter plot \
    of selected columns of a dataset.
    """

    color: schema_field(
        none_type(string_field()),
        None,
        ("The columnName to take for Class coloring."),
    )  # type: ignore
    simbol: schema_field(
        none_type(string_field()),
        None,
        ("The columnName to take for symbol grouping."),
    )  # type: ignore
    size: schema_field(
        none_type(string_field()),
        None,
        ("The columnName to take for size of the points."),
    )  # type: ignore


class ScatterPlotExplorer(BaseExplorer):
    SCHEMA = ScatterPlotSchema

    metadata: Dict[str, Any] = {
        "allowed_dtypes": ["*"],
        "restricted_dtypes": [],
        "input_cardinality": {"exact": 2},
    }

    def __init__(self, **kwargs) -> None:
        self.color = kwargs.get("color")
        self.simbol = kwargs.get("simbol")
        self.size = kwargs.get("size")
        super().__init__(**kwargs)

    def prepare_dataset(
        self, dataset_dict: DatasetDict, columns: List[str]
    ) -> DashAIDataset:
        split = list(dataset_dict.keys())[0]
        dataset_columns = dataset_dict[split].column_names

        colorColumn = self.kwargs.get("color")
        if colorColumn and colorColumn in dataset_columns:
            columns.append(colorColumn)
        simbolColumn = self.kwargs.get("simbol")
        if simbolColumn and simbolColumn in dataset_columns:
            columns.append(simbolColumn)
        sizeColumn = self.kwargs.get("size")
        if sizeColumn and sizeColumn in dataset_columns:
            columns.append(sizeColumn)

        columns = list(set(columns))
        print(columns)
        return super().prepare_dataset(dataset_dict, columns)

    def launch_exploration(self, dataset: DashAIDataset, explorer_info: Explorer):
        _df = dataset.to_pandas()
        cols = [col["columnName"] for col in explorer_info.columns]

        colorColumn = self.color if self.color in _df.columns else None
        simbolColumn = self.simbol if self.simbol in _df.columns else None
        sizeColumn = self.size if self.size in _df.columns else None

        fig = px.scatter(
            _df,
            x=cols[0],
            y=cols[1],
            color=colorColumn,
            symbol=simbolColumn,
            size=sizeColumn,
            title=f"Scatter Plot of {cols[0]} vs {cols[1]}",
        )

        return fig

    def save_exploration(
        self,
        exploration_info: Exploration,
        explorer_info: Explorer,
        save_path: str,
        result: Figure,
    ) -> str:
        if explorer_info.name is None or explorer_info.name == "":
            filename = f"{exploration_info.id}_{explorer_info.id}.pickle"
        else:
            filename = f"{explorer_info.name}_{explorer_info.id}.pickle"
        path = pathlib.Path(os.path.join(save_path, filename))

        with open(path, "wb") as f:
            pickle.dump(result, f)

        return path.as_posix()

    def get_results(
        self, exploration_path: str, options: Dict[str, Any]
    ) -> Dict[str, Any]:
        resultType = "plotly_json"
        config = {}

        with open(exploration_path, "rb") as f:
            result = pickle.load(f)

        result: Figure = result
        result = result.to_json()

        return {"data": result, "type": resultType, "config": config}
