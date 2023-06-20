import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { DataGrid } from "@mui/x-data-grid";
import {
  AddCircleOutline as AddIcon,
  Update as UpdateIcon,
} from "@mui/icons-material";
import { Button, Grid, Paper, Typography } from "@mui/material";
import DeleteItemModal from "./custom/DeleteItemModal";
import EditDatasetModal from "./EditDatasetModal";
import {
  getDatasets as getDatasetsRequest,
  deleteDataset as deleteDatasetRequest,
} from "../api/datasets";
import { useSnackbar } from "notistack";

function DatasetsTable({ handleNewDataset, updateFlag, setUpdateFlag }) {
  const [loading, setLoading] = useState(true);
  const [datasets, setDatasets] = useState([]);
  const { enqueueSnackbar } = useSnackbar();

  const getDatasets = async () => {
    setLoading(true);
    try {
      const datasets = await getDatasetsRequest();
      setDatasets(datasets);
    } catch (error) {
      enqueueSnackbar("Error while trying to obtain the dataset table.", {
        variant: "error",
        anchorOrigin: {
          vertical: "top",
          horizontal: "right",
        },
      });
      if (error.response) {
        console.error("Response error:", error.message);
      } else if (error.request) {
        console.error("Request error", error.request);
      } else {
        console.error("Unkown Error", error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const deleteDataset = async (id) => {
    try {
      await deleteDatasetRequest(id);
      enqueueSnackbar("Dataset successfully deleted.", {
        variant: "success",
        anchorOrigin: {
          vertical: "top",
          horizontal: "right",
        },
      });
    } catch (error) {
      enqueueSnackbar("Error when trying to delete the dataset", {
        variant: "error",
        anchorOrigin: {
          vertical: "top",
          horizontal: "right",
        },
      });
      if (error.response) {
        console.error("Response error:", error.message);
      } else if (error.request) {
        console.error("Request error", error.request);
      } else {
        console.error("Unkown Error", error.message);
      }
    }
  };

  const createDeleteHandler = React.useCallback(
    (id) => () => {
      deleteDataset(id);
      setUpdateFlag(true);
    },
    [],
  );

  // Fetch datasets when the component is mounting
  useEffect(() => {
    getDatasets();
  }, []);

  // triggers an update of the table when updateFlag is set to true
  useEffect(() => {
    if (updateFlag) {
      getDatasets();
      setUpdateFlag(false);
    }
  }, [updateFlag]);

  const columns = React.useMemo(
    () => [
      {
        field: "id",
        headerName: "ID",
        minWidth: 50,
        editable: false,
      },
      {
        field: "name",
        headerName: "Name",
        minWidth: 250,
        editable: false,
      },
      {
        field: "task_name",
        headerName: "Task",
        minWidth: 200,
        editable: false,
      },
      {
        field: "file_path",
        headerName: "File Path",
        minWidth: 300,
        editable: false,
      },
      {
        field: "actions",
        type: "actions",
        minWidth: 150,
        getActions: (params) => [
          <EditDatasetModal
            key="edit-component"
            name={params.row.name}
            taskName={params.row.task_name}
            datasetId={params.id}
            updateDatasets={() => setUpdateFlag(true)}
          />,
          <DeleteItemModal
            key="delete-component"
            deleteFromTable={createDeleteHandler(params.id)}
          />,
        ],
      },
    ],
    [createDeleteHandler],
  );

  return (
    <Paper sx={{ py: 4, px: 6 }}>
      {/* Title and new datasets button */}
      <Grid
        container
        direction="row"
        justifyContent="space-between"
        alignItems="center"
        sx={{ mb: 4 }}
      >
        <Typography variant="h5" component="h2">
          Current datasets
        </Typography>
        <Grid item>
          <Grid container spacing={2}>
            <Grid item>
              <Button
                variant="contained"
                onClick={handleNewDataset}
                endIcon={<AddIcon />}
              >
                New Dataset
              </Button>
            </Grid>
            <Grid item>
              <Button
                variant="contained"
                onClick={() => setUpdateFlag(true)}
                endIcon={<UpdateIcon />}
              >
                Update
              </Button>
            </Grid>
          </Grid>
        </Grid>
      </Grid>

      {/* Datasets Table */}
      <DataGrid
        rows={datasets}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 5,
            },
          },
        }}
        pageSizeOptions={[10]}
        disableRowSelectionOnClick
        autoHeight
        loading={loading}
      />
    </Paper>
  );
}

DatasetsTable.propTypes = {
  handleNewDataset: PropTypes.func.isRequired,
  updateFlag: PropTypes.bool.isRequired,
  setUpdateFlag: PropTypes.func.isRequired,
};

export default DatasetsTable;
