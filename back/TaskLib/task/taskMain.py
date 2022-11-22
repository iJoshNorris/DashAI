from abc import ABC, abstractclassmethod, abstractmethod
import numpy as np
from Models.classes.getters import filter_by_parent
from TaskLib.task.taskMetaclass import TaskMetaclass
import joblib

class Task(metaclass=TaskMetaclass):
    """
    Task is an abstract class for all the Task implemented in the framework.
    Never use this class directly.
    """

    NAME: str = ""
    compatible_models: list = []
    executions_id = []
    executions = []

    def __init__(self):
        self.executions: list = []
        self.set_compatible_models()
    
    def save(self, filename) -> None:
        joblib.dump(self, filename)
    
    @staticmethod
    def load(filename):
        return joblib.load(filename)

    def set_compatible_models(self) -> None:
        # TODO do not use the name of the task, just look for 
        # models that have the task into its comptaible task.
        task_name = self.NAME if self.NAME else Exception("Need specify task name")
        model_class_name = f"{task_name[:-4]}Model"
        models_dict = filter_by_parent(model_class_name)
        self.compatible_models = models_dict
        return self.compatible_models

    def set_executions(self, model: str, param: dict) -> None:
        """
        This method configures one execution per model in models with the parameters
        in the params[model] dictionary.
        The executions were temporaly save in self.executions.
        """
        def parse_params(model_json, model_params):
            """
            Generate model's parameter dictionary, instantiating recursive
            parameters.
            """
            execution_params = {}
            for json_param in model_json:
                if model_json.get(json_param)["oneOf"][0].get("type") == "class":
                    param_choice = model_params[json_param].pop("choice")
                    param_class = filter_by_parent(model_json.get(json_param)["oneOf"][0].get("parent")).get(param_choice)
                    param_sub_params = parse_params(param_class.SCHEMA.get("properties"), model_params[json_param])
                    execution_params[json_param] = param_class(**param_sub_params)
                else:
                    execution_params[json_param] = model_params[json_param]
            return execution_params
        # TODO Generate a Grid to search the best model
        execution = self.compatible_models[model]
        model_json = execution.SCHEMA.get("properties")
        # TODO use JSON_SCHEMA to check user params
        execution_params = parse_params(model_json, param)
        return execution(**execution_params)

    def run_experiments(self, input_data: dict):
        """
        This method train all the executions in self.executions with the data in
        input_data.
        The input_data dictionary must have train and test keys to perform the training.
        The test results were temporaly save in self.experimentResults.
        """
        x_train = np.array(input_data["train"]["x"])
        y_train = np.array(input_data["train"]["y"])
        x_test = np.array(input_data["test"]["x"])
        y_test = np.array(input_data["test"]["y"])

        # Stores the input categories to map it later
        # TODO better to do in the orchester.
        self.categories = []
        for cat in y_train:
            if cat not in self.categories:
                self.categories.append(cat)
        for cat in y_test:
            if cat not in self.categories:
                self.categories.append(cat)

        # Use a number instead of the input caategory
        numeric_y_train = []
        for sample in y_train:
            numeric_y_train.append(self.categories.index(sample))
        numeric_y_test = []
        for sample in y_test:
            numeric_y_test.append(self.categories.index(sample))

        experimentResults = {}

        for execution in self.executions:
            execution.fit(x_train, numeric_y_train)

            trainResults = execution.score(x_train, numeric_y_train)
            testResults = execution.score(x_test, numeric_y_test)

            experimentResults[execution.MODEL] = {
                "train": trainResults,
                "test": testResults,
            }
        return experimentResults

    def map_category(self, index):
        """Returns the original category for the index artificial category"""
        return self.categories[index]
    
    def parse_single_input_from_string(self, x : str):
        return x

    def get_prediction(self, execution, x):
        """Returns the predicted output of x, given by the execution"""
        cat = execution.predict(self.parse_single_input_from_string(x))
        final_cat = self.map_category(int(cat[0]))
        return final_cat
