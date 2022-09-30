import React, { useState, useEffect } from 'react';
import {
  Card,
  Button,
  Accordion,
} from 'react-bootstrap';
import PropTypes from 'prop-types';
import { useFormik } from 'formik';

function ClassInput({ modelName, paramJsonSchema, setFieldValue }) {
  ClassInput.propTypes = {
    modelName: PropTypes.string.isRequired,
    paramJsonSchema: PropTypes.objectOf(
      PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.bool,
        PropTypes.object,
      ]),
    ).isRequired,
    setFieldValue: PropTypes.func.isRequired,
  };
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState('KNN');
  const [paramSchema, setParamSchema] = useState({});
  const getOptions = async (parentClass) => {
    const fetchedOptions = await fetch(
      `http://localhost:8000/getChildren/${parentClass}`,
    );
    const receivedOptions = await fetchedOptions.json();
    setOptions(receivedOptions);
    console.log(receivedOptions);
  };
  const getParamSchema = async () => {
    if (selectedOption !== '') {
      const fetchedParams = await fetch(`http://localhost:8000/selectModel/${selectedOption}`);
      const parameterSchema = await fetchedParams.json();
      setParamSchema(parameterSchema);
    }
  };
  useEffect(() => { getOptions(paramJsonSchema.parent); }, []);
  useEffect(() => { getParamSchema(); }, [selectedOption]);
  return (
    <div key={modelName}>
      <div>
        <label htmlFor={modelName}>{modelName}</label>
        <select value={selectedOption} name="choice" onChange={(e) => setSelectedOption(e.target.value)}>
          {options.map((option) => <option key={option}>{option}</option>)}
        </select>
      </div>
      <Accordion>
        <Accordion.Item eventKey="0">
          <Accordion.Header>{`${selectedOption} parameters`}</Accordion.Header>
          <Accordion.Body>
            <SubForm
              name={modelName}
              parameterSchema={paramSchema}
              setFieldValue={setFieldValue}
              choice={selectedOption}
              key={`SubForm-${selectedOption}`}
            />
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    </div>
  );
}

const genInput = (modelName, paramJsonSchema, formik) => {
  const { type, properties } = paramJsonSchema;
  switch (type) {
    case 'object':
      return (
        <div key={modelName}>
          {
            Object.keys(properties)
              .map((parameter) => genInput(
                parameter,
                properties[parameter].oneOf[0],
                formik,
              ))
          }
        </div>
      );

    case 'integer':
      return (
        <div key={modelName}>
          <label htmlFor={modelName}>{modelName}</label>
          <input
            type="number"
            name={modelName}
            id={modelName}
            value={formik.values[modelName]}
            onChange={formik.handleChange}
          />
        </div>
      );

    case 'string':
      return (
        <div key={modelName}>
          <label htmlFor={modelName}>{modelName}</label>
          <select
            name={modelName}
            id={modelName}
            value={formik.values[modelName]}
            onChange={formik.handleChange}
          >
            {
              paramJsonSchema
                .enum
                .map((option) => <option key={option} value={option}>{option}</option>)
            }
          </select>
        </div>
      );

    case 'number':
      return (
        <div key={modelName}>
          <label htmlFor={modelName}>{modelName}</label>
          <input
            type="number"
            name={modelName}
            id={modelName}
            value={formik.values[modelName]}
            onChange={formik.handleChange}
          />
        </div>
      );

    case 'boolean':
      return (
        <div key={modelName}>
          <label htmlFor={modelName}>{modelName}</label>
          <select
            name={modelName}
            id={modelName}
            value={formik.values[modelName]}
            onChange={formik.handleChange}
          >
            <option key={`${modelName}-true`} value="True">True</option>
            <option key={`${modelName}-false`} value="False">False</option>
          </select>
        </div>
      );

    case 'class':
      return (
        <ClassInput
          modelName={modelName}
          paramJsonSchema={paramJsonSchema}
          setFieldValue={formik.setFieldValue}
          key={`rec-param-${modelName}`}
        />
      );

    default:
      return (
        <p style={{ color: 'red', fontWeight: 'bold' }}>{`Not a valid parameter type: ${type}`}</p>
      );
  }
};

function getDefaultValues(parameterJsonSchema) {
  const { properties } = parameterJsonSchema;
  if (typeof properties !== 'undefined') {
    const parameters = Object.keys(properties);
    const defaultValues = parameters.reduce(
      (prev, current) => ({
        ...prev,
        [current]:
             properties[current].oneOf[0].default
          || properties[current].oneOf[0].deafult
          || {},
      }),
      {},
    );
    return (defaultValues);
  }
  return ('null');
}

function SubForm({
  name,
  parameterSchema,
  setFieldValue,
  choice,
}) {
  SubForm.propTypes = {
    name: PropTypes.string,
    parameterSchema: PropTypes.objectOf(
      PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.bool,
        PropTypes.object,
      ]),
    ).isRequired,
    setFieldValue: PropTypes.func.isRequired,
    choice: PropTypes.string.isRequired,
  };

  SubForm.defaultProps = {
    name: 'undefined',
  };
  const defaultValues = getDefaultValues(parameterSchema);
  const newDefaultValues = { ...defaultValues, choice };
  if (defaultValues === 'null') {
    return (<p>Recursion</p>);
  }
  const formik = useFormik({
    initialValues: newDefaultValues,
  });
  useEffect(() => {
    setFieldValue(name, formik.values);
  }, [formik.values]);

  return (
    <div key={`parameterForm-${name}`}>
      { genInput(name, parameterSchema, formik) }
    </div>
  );
}

function ParameterForm({
  type,
  index,
  parameterSchema,
  setConfigByTableIndex,
}) {
  ParameterForm.propTypes = {
    type: PropTypes.string.isRequired,
    index: PropTypes.number.isRequired,
    parameterSchema: PropTypes.objectOf(
      PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.bool,
        PropTypes.object,
      ]),
    ).isRequired,
    setConfigByTableIndex: PropTypes.func.isRequired,
  };
  if (Object.keys(parameterSchema).length === 0) {
    return (<div />);
  }
  const defaultValues = getDefaultValues(parameterSchema);
  if (defaultValues === 'null') {
    return (<div />);
  }
  const formik = useFormik({
    initialValues: defaultValues,
    onSubmit: (values) => setConfigByTableIndex(index, type, values),
  });
  return (
    <Card className="sm-6">
      <Card.Header>Model parameters</Card.Header>
      <div style={{ padding: '40px 10px' }}>
        { genInput(type, parameterSchema, formik) }
      </div>
      <Card.Footer>
        <Button variant="dark" onClick={formik.handleSubmit} style={{ width: '100%' }}>Save</Button>
      </Card.Footer>
    </Card>
  );
}

export default ParameterForm;
