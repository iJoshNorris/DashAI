import { Stack } from "@mui/material";
import React, { useEffect, useMemo, useState } from "react";
import { useFormSchemaStore } from "../../contexts/schema";
import FormSchemaBreadScrumbs from "./FormSchemaBreadScrumbs";
import FormSchema from "./FormSchema";
import FormSchemaModelSelect from "./FormSchemaModelSelect";
import PropTypes from "prop-types";

/**
 * This component is a form schema with a selected model
 * @param {string} modelToConfigure - The model to configure
 * @param {object} initialValues - The initial values of the form
 * @param {function} onFormSubmit - The function to submit the form
 * @param {function} onCancel - The function to cancel the form
 */

function FormSchemaWithSelectedModel({
  modelToConfigure,
  initialValues,
  onFormSubmit,
  onCancel,
}) {
  const {
    formValues,
    properties,
    propertyData,
    valuesByProperties,
    removeLastProperty,
  } = useFormSchemaStore();

  const [selectedModel, setSelectedModel] = useState(
    modelToConfigure || propertyData?.model,
  );

  const selectedProperty = Boolean(propertyData?.selected);

  const defaultValues = useMemo(() => {
    if (selectedProperty) {
      if (selectedModel === propertyData.model) {
        return propertyData.params;
      } else return null;
    }

    return initialValues ?? valuesByProperties;
  }, [selectedModel, propertyData.params]);

  useEffect(() => {
    setSelectedModel(propertyData.model);
  }, [propertyData.model, propertyData.params]);

  return (
    <Stack spacing={4} sx={{ py: 2 }}>
      {/* Dropdown to select a configurable object to render a subform */}

      {Boolean(propertyData) && (
        <>
          <FormSchemaBreadScrumbs properties={properties} />
          <FormSchemaModelSelect
            parent={propertyData.parent}
            selectedModel={selectedModel}
            onChange={setSelectedModel}
          />
        </>
      )}

      <FormSchema
        model={selectedModel}
        initialValues={defaultValues}
        onFormSubmit={() => onFormSubmit(formValues)}
        onCancel={() => {
          if (properties.length > 0) {
            removeLastProperty();
          } else {
            onCancel();
          }
        }}
      />
    </Stack>
  );
}

FormSchemaWithSelectedModel.propTypes = {
  modelToConfigure: PropTypes.string,
  initialValues: PropTypes.object,
  onFormSubmit: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
};

export default FormSchemaWithSelectedModel;
