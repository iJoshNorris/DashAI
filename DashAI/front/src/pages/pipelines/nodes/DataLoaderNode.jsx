import React, { useState } from "react";
import { Grid, Paper, CircularProgress, Typography, Table, TableBody, TableCell, TableRow, TableHead, TableContainer } from "@mui/material";
import Upload from "./Upload";
import { useSnackbar } from "notistack";
import Papa from "papaparse";

function DataLoaderNode() {
  const [newDataset, setNewDataset] = useState({ file: null, url: "", data: [] });
  const [loading, setLoading] = useState(false);
  const { enqueueSnackbar } = useSnackbar();

  const handleFileUpload = (file, url) => {
    setLoading(true);
    setNewDataset({ file, url, data: [] });

    const reader = new FileReader();
    reader.onload = (event) => {
      const csvData = Papa.parse(event.target.result, {
        header: true,
        preview: 5,
      });
      setNewDataset({ file, url, data: csvData.data });
      setLoading(false);
      enqueueSnackbar("File uploaded successfully", { variant: "success" });
    };
    reader.readAsText(file);
  };

  return (
    <Paper variant="outlined" sx={{ p: 4, m: 2 }}>
      <Grid container direction="row" justifyContent="center" alignItems="center">
        <Grid item xs={12} md={6} display="flex" justifyContent="center">
          <Upload onFileUpload={handleFileUpload} />
        </Grid>
      </Grid>

      {loading && (
        <Grid container justifyContent="center" sx={{ marginTop: 2 }}>
          <CircularProgress />
        </Grid>
      )}

      {!loading && newDataset.data.length > 0 && (
        <Grid container justifyContent="center" sx={{ marginTop: 2 }}>
          <Typography variant="h6" gutterBottom>
            Dataset Head (First 5 Rows)
          </Typography>
          <TableContainer sx={{ overflowX: "auto", mt: 2 }}>
            <Table>
              <TableHead>
                <TableRow>
                  {Object.keys(newDataset.data[0]).map((key) => (
                    <TableCell key={key}>{key}</TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {newDataset.data.map((row, index) => (
                  <TableRow key={index}>
                    {Object.values(row).map((value, idx) => (
                      <TableCell key={idx}>{value}</TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>
      )}
    </Paper>
  );
}

export default DataLoaderNode;
