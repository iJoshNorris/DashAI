// DatasetSummaryTable.js
import React, { useEffect, useMemo, useState } from "react";
import { useSnackbar } from "notistack";
import PropTypes from "prop-types";
import { DataGrid, useGridApiRef } from "@mui/x-data-grid";
import {
  getDatasetSample as getDatasetSampleRequest,
  getDatasetTypes as getDatasetTypesRequest,
} from "../../api/datasets";
import { dataTypesList, columnTypesList, imageTypesList } from "../../utils/typesLists";
import SelectTypeCell from "../custom/SelectTypeCell";

function DatasetSummaryTable({
  datasetId,
  isEditable,
  columnsSpec,
  setColumnsSpec,
  newDataset,
  setNewDataset,
  selectedDataloader,
  setSelectedDataloader,
}) {
  const [loading, setLoading] = useState(true);
  const { enqueueSnackbar } = useSnackbar();
  const [rows, setRows] = useState([]);
  const apiRef = useGridApiRef();

  const getDatasetInfo = async () => {
    setLoading(true);
    try {
      const dataset = await getDatasetSampleRequest(datasetId);
      const types = await getDatasetTypesRequest(datasetId);//revisareeeeee
      console.log(types);
      let datatype = null;
      const rowsArray = Object.keys(dataset).map((name, idx) => {
        if (types[name].type === "Value" || types[name].type === "ClassLabel") {
          datatype = types[name].dtype
        }
        else {
          datatype = "Seleccionar tipo de input de imagen"
        }
        return {
          id: idx,
          columnName: name,
          example: dataset[name][0],
          columnType: types[name].type,
          dataType: datatype,
        };
      });
      setRows(rowsArray);
      if (isEditable) {
        setColumnsSpec(types);
      }
    } catch (error) {
      enqueueSnackbar("Error while trying to obtain the dataset.");
      if (error.response) {
        console.error("Response error:", error.message);
      } else if (error.request) {
        console.error("Request error", error.request);
      } else {
        console.error("Unknown Error", error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const updateCellValue = async (id, field, newValue) => {
    await apiRef.current.setEditCellValue({ id, field, value: newValue });
    apiRef.current.stopCellEditMode({ id, field });
    setRows((prevRows) =>
      prevRows.map((row) =>
        row.id === id ? { ...row, [field]: newValue } : row,
      ),
    );

    const columnName = rows.find((row) => row.id === id)?.columnName;
    const updateColumns = { ...columnsSpec };

    if (field === "dataType") {
      updateColumns[columnName].dtype = newValue;
    } else if (field === "columnType") {
      updateColumns[columnName].type = newValue;

      if (newValue === "Image") {
        setNewDataset({ ...newDataset, dataloader: selectedDataloader.name })
      }
      
    }

    setColumnsSpec(updateColumns);
  };

  const renderSelectCell = (params, options) => {
    return (
      <SelectTypeCell
        id={params.id}
        value={params.value}
        field={params.field}
        options={options}
        updateValue={(id, field, newValue) =>
          updateCellValue(id, field, newValue)
        }
      />
    );
  };

  const columns = useMemo(() => [
    {
      field: "columnName",
      headerName: "Column name",
      minWidth: 200,
      editable: false,
    },
    {
      field: "example",
      headerName: "Example",
      minWidth: 200,
      editable: false,
    },
    {
      field: "columnType",
      headerName: "Column type",
      renderEditCell: (params) =>
        isEditable && renderSelectCell(params, columnTypesList),
      minWidth: 200,
      editable: isEditable,
    },
    {
      field: "dataType",
      headerName: "Data type",
      renderEditCell: (params) => {
        const datatypes = params.row.columnType === "Value" ? dataTypesList : imageTypesList;
        return isEditable && renderSelectCell(params, datatypes);
      },
      minWidth: 200,
      editable: isEditable,
    },
  ]);

  useEffect(() => {
    getDatasetInfo();
  }, []);

  return (
    <DataGrid
      rows={rows}
      columns={columns}
      initialState={{
        pagination: {
          paginationModel: {
            pageSize: 4,
          },
        },
      }}
      pageSize={4}
      pageSizeOptions={[4, 5, 10]}
      loading={loading}
      apiRef={apiRef}
      autoHeight
    />
  );
}

DatasetSummaryTable.propTypes = {
  datasetId: PropTypes.number,
  isEditable: PropTypes.bool,
  columnsSpec: PropTypes.object,
  setColumnsSpec: PropTypes.func,
};

export default DatasetSummaryTable;
