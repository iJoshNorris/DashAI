import React from "react";
import { Button } from "@mui/material";
import PropTypes from "prop-types";

/**
 * Upload component for selecting and uploading a file.
 * @param {function} onFileUpload
 */

function Upload({ onFileUpload }) {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const fileURL = URL.createObjectURL(file);
      onFileUpload(file, fileURL);
    }
  };

  return (
    <>
      <input
        accept=".csv, .xlsx"
        style={{ display: "none" }}
        id="file-upload"
        type="file"
        onChange={handleFileChange}
      />
      <label htmlFor="file-upload">
        <Button variant="contained" component="span" color="primary">
          Upload File
        </Button>
      </label>
    </>
  );
}

Upload.propTypes = {
  onFileUpload: PropTypes.func.isRequired,
};

export default Upload;
