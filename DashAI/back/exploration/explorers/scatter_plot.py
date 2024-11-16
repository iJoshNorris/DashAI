import os
import pathlib
import pickle

import plotly.express as px
from beartype.typing import Any, Dict, List
from plotly.graph_objs import Figure

from DashAI.back.core.schema_fields import (
    enum_field,
    int_field,
    none_type,
    schema_field,
    string_field,
    union_type,
)
from DashAI.back.dataloaders.classes.dashai_dataset import (  # ClassLabel, Value,
    DashAIDataset,
    DatasetDict,
)
from DashAI.back.dependencies.database.models import Exploration, Explorer
from DashAI.back.exploration.base_explorer import BaseExplorer, BaseExplorerSchema


class ScatterPlotSchema(BaseExplorerSchema):
    color_group: schema_field(
        none_type(union_type(string_field(), int_field(ge=0))),
        None,
        ("The columnName or columnIndex to take for grouping colored points."),
    )  # type: ignore
    simbol_group: schema_field(
        none_type(union_type(string_field(), int_field(ge=0))),
        None,
        ("The columnName or columnIndex to take for grouping simbol of the points."),
    )  # type: ignore
    point_size_from: schema_field(
        enum_field(["column values", "fixed value"]),
        "column values",
        ("The source of the point size."),
    )  # type: ignore
    point_size: schema_field(
        none_type(union_type(string_field(), int_field(ge=0))),
        None,
        ("The columnName, columnIndex or value to take for the size of the points."),
    )  # type: ignore


class ScatterPlotExplorer(BaseExplorer):
    """
    ScatterPlotExplorer is an explorer that returns a scatter plot
    of selected columns of a dataset.
    """

    DISPLAY_NAME = "Scatter Plot"
    DESCRIPTION = (
        "ScatterPlotExplorer is an explorer that returns a scatter plot "
        "of selected columns of a dataset."
    )

    SCHEMA = ScatterPlotSchema
    metadata: Dict[str, Any] = {
        "allowed_dtypes": ["*"],
        "restricted_dtypes": [],
        "input_cardinality": {"exact": 2},
    }

    def __init__(self, **kwargs) -> None:
        self.color_column = kwargs.get("color_group")
        self.simbol_column = kwargs.get("simbol_group")
        self.point_size_from = kwargs.get("point_size_from")
        self.point_size = kwargs.get("point_size")
        super().__init__(**kwargs)

    def prepare_dataset(
        self, dataset_dict: DatasetDict, columns: List[Dict[str, Any]]
    ) -> DashAIDataset:
        split = list(dataset_dict.keys())[0]
        explorer_columns = [col["columnName"] for col in columns]
        dataset_columns = dataset_dict[split].column_names

        if self.color_column is not None:
            if isinstance(self.color_column, int):
                idx = self.color_column
                col = dataset_columns[idx]
                if col not in explorer_columns:
                    columns.append({"id": idx, "columnName": col})
            else:
                col = self.color_column
                if col not in explorer_columns:
                    columns.append({"columnName": col})
            self.color_column = col

        if self.simbol_column is not None:
            if isinstance(self.simbol_column, int):
                idx = self.simbol_column
                col = dataset_columns[idx]
                if col not in explorer_columns:
                    columns.append({"id": idx, "columnName": col})
            else:
                col = self.simbol_column
                if col not in explorer_columns:
                    columns.append({"columnName": col})
            self.simbol_column = col

        if self.point_size is not None:
            if self.point_size_from == "column values":
                if isinstance(self.point_size, (int, float)):
                    idx = self.point_size
                    col = dataset_columns[idx]
                    if col not in explorer_columns:
                        columns.append({"id": idx, "columnName": col})
                else:
                    col = self.point_size
                    if col not in explorer_columns:
                        columns.append({"columnName": col})
                self.point_size = col
            elif self.point_size_from == "fixed value":
                self.point_size = int(self.point_size)

        return super().prepare_dataset(dataset_dict, columns)

    def launch_exploration(self, dataset: DashAIDataset, explorer_info: Explorer):
        _df = dataset.to_pandas()
        cols = [col["columnName"] for col in explorer_info.columns]

        colorColumn = self.color_column if self.color_column in _df.columns else None
        simbolColumn = self.simbol_column if self.simbol_column in _df.columns else None
        if self.point_size_from == "column values" and self.point_size is not None:
            pointSize = self.point_size if self.point_size in _df.columns else None
        else:
            pointSize = None

        fig = px.scatter(
            _df,
            x=cols[0],
            y=cols[1],
            color=colorColumn,
            symbol=simbolColumn,
            size=pointSize,
            title=f"Scatter Plot of {cols[0]} vs {cols[1]}",
        )

        if self.point_size_from == "fixed value" and self.point_size is not None:
            fig.update_traces(marker={"size": self.point_size})

        if explorer_info.name is not None and explorer_info.name != "":
            fig.update_layout(title=f"{explorer_info.name}")

        return fig

    def save_exploration(
        self,
        __exploration_info__: Exploration,
        explorer_info: Explorer,
        save_path: str,
        result: Figure,
    ) -> str:
        if explorer_info.name is None or explorer_info.name == "":
            filename = f"{explorer_info.id}.pickle"
        else:
            filename = f"{explorer_info.id}_{explorer_info.name}.pickle"
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
