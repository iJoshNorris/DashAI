import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { PlayArrow as PlayArrowIcon } from "@mui/icons-material";
import { DataGrid, GridActionsCellItem } from "@mui/x-data-grid";
import {
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Paper,
  Typography,
} from "@mui/material";
import { getRuns as getRunsRequest } from "../../api/run";
import { executeRun as executeRunRequest } from "../../api/runner";
import { useSnackbar } from "notistack";
import { getRunStatus } from "../../utils/runStatus";
import { LoadingButton } from "@mui/lab";

/**
 * Modal for selecting the runs to be sent to execute in an experiment
 * @param {object} experiment contains the information of an experiment as received from the backend (IExperiment)
 */
function RunnerDialog({ experiment, expRunning, setExpRunning }) {
  const { enqueueSnackbar } = useSnackbar();
  const [open, setOpen] = useState(false);
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [rowSelectionModel, setRowSelectionModel] = useState([]);

  const [runQueue, setRunQueue] = useState([]);
  const [runNext, setRunNext] = useState(false);
  const [runningNow, setRunningNow] = useState("");

  const getRuns = async () => {
    setLoading(true);
    try {
      const runs = await getRunsRequest(experiment.id.toString());
      const firstRunInExecution = runs.find((run) => run.status === 2); // searches for a run with the status "running"
      if (firstRunInExecution !== undefined) {
        setExpRunning({ ...expRunning, [experiment.id]: true });
      }
      const runsWithStringStatus = runs.map((run) => {
        return { ...run, status: getRunStatus(run.status) };
      });
      setRows(runsWithStringStatus);

      if (rowSelectionModel.length === 0) {
        setRowSelectionModel(runs.map((run, idx) => run.id));
      }

      const running = runs.find((run) => run.id === runningNow);

      if (running && running.status === 3) {
        const allRunsFinished = runs
          .filter((run) => rowSelectionModel.includes(run.id))
          .every((run) => run.status === 3);
        if (allRunsFinished) {
          setExpRunning({ ...expRunning, [experiment.id]: false });
          enqueueSnackbar(
            `${experiment.name} has succesfully finished running`,
            {
              variant: "success",
            },
          );
        } else {
          setRunNext(true);
        }
      }
    } catch (error) {
      enqueueSnackbar(
        `Error while trying to obtain the runs associated to ${experiment.name}`,
      );
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

  const handleExecuteRuns = async () => {
    setExpRunning({ ...expRunning, [experiment.id]: true });
    setRunQueue(rowSelectionModel);
    setRunNext(true);
  };

  const columns = [
    {
      field: "name",
      headerName: "Name",
      minWidth: 250,
      editable: false,
    },
    {
      field: "model_name",
      headerName: "Model Name",
      minWidth: 300,
      editable: false,
    },
    {
      field: "status",
      headerName: "Status",
      minWidth: 150,
      editable: false,
    },
  ];

  // on mount, fetches runs associated to the experiment.
  useEffect(() => {
    getRuns();
  }, []);

  // polling to update the sate of the runs
  useEffect(() => {
    if (expRunning[experiment.id]) {
      // Fetch data initially
      getRuns();

      // Start polling
      const intervalId = setInterval(getRuns, 1000); // Poll every 1 second

      // Clean up the interval when the component unmounts
      return () => clearInterval(intervalId);
    }
  }, [expRunning]);

  const executeRun = async (runId) => {
    try {
      await executeRunRequest(runId);
    } catch (error) {
      setExpRunning({ ...expRunning, [experiment.id]: false });
      setRunNext(false);
      setRunningNow("");
      enqueueSnackbar(`Error while running the model with id ${runId}`);
      if (error.response) {
        console.error("Response error:", error.message);
      } else if (error.request) {
        console.error("Request error", error.request);
      } else {
        console.error("Unknown Error", error.message);
      }
    }
  };

  useEffect(() => {
    if (runNext && runQueue.length > 0) {
      setRunningNow(runQueue[0]);
      const newList = runQueue.filter((runId) => runId !== runQueue[0]);
      setRunQueue(newList);
      setRunNext(false);
      executeRun(runQueue[0]);
    }
  }, [runNext]);

  return (
    <React.Fragment>
      <GridActionsCellItem
        key="runner-button"
        icon={
          expRunning[experiment.id] ? (
            <CircularProgress size={18} />
          ) : (
            <PlayArrowIcon />
          )
        }
        label="Run"
        disabled={
          !expRunning[experiment.id] &&
          Object.values(expRunning).some((value) => value === true)
        }
        onClick={() => setOpen(true)}
      />
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        fullWidth
        maxWidth={"md"}
      >
        <DialogTitle>{`Runs in ${experiment.name}`}</DialogTitle>
        <DialogContent>
          <Paper
            sx={{ px: 3, py: 2 }}
            // solves a mui problem related to putting datagrid inside another datagrid
            onClick={(event) => {
              event.target = document.body;
            }}
          >
            <Typography variant="subtitle1" component="h3" sx={{ pb: 1 }}>
              Select models to run
            </Typography>
            <DataGrid
              rows={rows}
              columns={columns}
              checkboxSelection
              onRowSelectionModelChange={(newRowSelectionModel) => {
                setRowSelectionModel(newRowSelectionModel);
              }}
              rowSelectionModel={rowSelectionModel}
              initialState={{
                pagination: {
                  paginationModel: {
                    pageSize: 5,
                  },
                },
              }}
              pageSizeOptions={[5]}
              disableRowSelectionOnClick
              autoHeight
              loading={loading}
            />
          </Paper>
        </DialogContent>
        <DialogActions>
          <LoadingButton
            variant="contained"
            loading={expRunning[experiment.id]}
            endIcon={<PlayArrowIcon />}
            size="large"
            onClick={handleExecuteRuns}
          >
            Start
          </LoadingButton>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}

RunnerDialog.propTypes = {
  experiment: PropTypes.shape({
    name: PropTypes.string,
    id: PropTypes.number,
  }).isRequired,
  expRunning: PropTypes.objectOf(PropTypes.bool).isRequired,
  setExpRunning: PropTypes.func.isRequired,
};

export default RunnerDialog;
