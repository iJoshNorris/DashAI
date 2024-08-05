import React, { useState } from "react";
import PropTypes from "prop-types";
import { GridActionsCellItem } from "@mui/x-data-grid";
import { Settings } from "@mui/icons-material";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  Grid,
  Button,
  DialogActions,
  Typography,
} from "@mui/material";
import DatasetSummaryTable from "./DatasetSummaryTable";
import ConverterSelector from "./ConverterSelector";
import ConverterTable from "./ConverterTable";
import { updateDataset as updateDatasetRequest } from "../../api/datasets";
import { useSnackbar } from "notistack";

function ConvertDatasetModal({ datasetId }) {
  const { enqueueSnackbar } = useSnackbar();
  const [open, setOpen] = useState(false);
  const [appliedConverters, setAppliedConverters] = useState([]);

  const handleCloseContent = () => {
    setOpen(false);
  };

  const modifyDataset = async () => {
    try {
      await updateDatasetRequest(datasetId, {
        converters: appliedConverters.reduce((acc, { name, parameters, scope }) => {
          acc[name] = { params: parameters, scope: scope };
          return acc;
        }, {}),
      });
      enqueueSnackbar("Dataset updated successfully", {
        variant: "success",
      });
      setAppliedConverters([]);
    } catch (error) {
      enqueueSnackbar("Error while trying to update the dataset");
      if (error.response) {
        console.error("Response error:", error.message);
      } else if (error.request) {
        console.error("Request error", error.request);
      } else {
        console.error("Unknown Error", error.message);
      }
    }
  };

  const handleSaveConfig = () => {
    modifyDataset();
    setOpen(false);
  };

  return (
    <React.Fragment>
      <GridActionsCellItem
        key="converter-component"
        icon={<Settings />}
        label="Apply converters"
        onClick={() => setOpen(true)}
        sx={{ color: "warning.main" }}
      />
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        fullWidth
        maxWidth={"md"}
      >
        <DialogTitle>Apply converters</DialogTitle>
        <DialogContent dividers>
          <Grid
            container
            direction="row"
            justifyContent="space-around"
            alignItems="stretch"
            rowGap={2}
            onClick={(event) => event.stopPropagation()}
          >
            {/* Dataset summary table */}
            <Grid item xs={12}>
              <Typography variant="subtitle1" component="h3" mb={1}>
                Dataset preview
              </Typography>
            </Grid>
            <DatasetSummaryTable datasetId={datasetId} />

            {/* Converter selector */}
            <Grid item xs={12}>
              <Typography variant="subtitle1" component="h3" mb={1}>
                Add converter
              </Typography>
            </Grid>
            <ConverterSelector
              datasetId={datasetId}
              updateAppliedConvertersList={setAppliedConverters}
            />
            {/* Selected converters table */}
            <ConverterTable
              appliedConvertersList={appliedConverters}
              updateAppliedConvertersList={setAppliedConverters}
            />
          </Grid>
        </DialogContent>
        {/* Actions - Close and Modify */}
        <DialogActions>
          <Button onClick={handleCloseContent}>Close</Button>
          <Button
            onClick={handleSaveConfig}
            autoFocus
            variant="contained"
            color="primary"
            disabled={appliedConverters.length === 0}
          >
            Modify
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}

ConvertDatasetModal.propTypes = {
  datasetId: PropTypes.number.isRequired,
};

export default ConvertDatasetModal;