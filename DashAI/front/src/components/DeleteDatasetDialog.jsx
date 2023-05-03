import React from "react";
import PropTypes from "prop-types";
import { GridActionsCellItem } from "@mui/x-data-grid";
import DeleteIcon from "@mui/icons-material/Delete";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@mui/material";

function DeleteDatasetDialog({ deleteFromTable }) {
  const [open, setOpen] = React.useState(false);
  const handleDelete = () => {
    deleteFromTable();
    setOpen(false);
  };
  return (
    <React.Fragment>
      <GridActionsCellItem
        key="delete-button"
        icon={<DeleteIcon />}
        label="Delete"
        onClick={() => setOpen(true)}
        sx={{ color: "#ff8383" }}
      />
      <Dialog open={open} onClose={() => setOpen(false)}>
        <div>
          <DialogTitle>Confirm Deletion</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Are you sure you want to delete this dataset?
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpen(false)} autoFocus>
              Cancel
            </Button>
            <Button onClick={handleDelete}>Delete</Button>
          </DialogActions>
        </div>
      </Dialog>
    </React.Fragment>
  );
}
DeleteDatasetDialog.propTypes = {
  deleteFromTable: PropTypes.func.isRequired,
};

export default DeleteDatasetDialog;
