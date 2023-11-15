import api from "./api";
import type { IDataset } from "../types/dataset";

const datasetEndpoint = "/v1/dataset";

export const uploadDataset = async (formData: object): Promise<object> => {
  const response = await api.post<IDataset[]>(datasetEndpoint, formData);
  return response.data;
};

export const getDatasets = async (): Promise<IDataset[]> => {
  const response = await api.get<IDataset[]>(datasetEndpoint);
  return response.data;
};
export const getDatasetSample = async (id: number): Promise<object> => {
  const response = await api.get<object>(`${datasetEndpoint}/sample/${id}`);
  return response.data;
};
export const getDatasetTypes = async (id: number): Promise<object> => {
  const response = await api.get<object>(`${datasetEndpoint}/types/${id}`);
  return response.data;
};

export const updateDataset = async (
  id: number,
  datasetName: string | undefined = undefined,
  columnsType:
    | Record<string, { type: string; dtype: string }>
    | undefined = undefined,
): Promise<IDataset> => {
  let params = {};

  if (datasetName !== undefined) {
    params = { ...params, name: datasetName };
  }

  if (columnsType !== undefined) {
    if (columnsType !== undefined) {
      params = { ...params, columns: columnsType };
    }
  }
  const response = await api.patch<IDataset>(`${datasetEndpoint}/${id}`, null, {
    params,
  });
  return response.data;
};

export const deleteDataset = async (id: string): Promise<object> => {
  const response = await api.delete(`${datasetEndpoint}/${id}`);
  return response.data;
};
