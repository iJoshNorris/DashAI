from typing import Any

from DashAI.back.registries.relationship_manager import RelationshipManager


class Registry:
    """An object that stores all components registered in a execution of DashAI."""

    def __init__(
        self,
        initial_components: list[type] | None = None,
    ) -> None:
        """Initializes the registry.

        Parameters
        ----------
        initial_components : List[Type]
            List with the initial objects to be entered in the registry,
            by default None.

        Raises
        ------
        TypeError
            If initial_components is not a list of types.
        TypeError
            If the task registry is neither none nor an instance of BaseRegistry.
        """

        if not isinstance(initial_components, list | type(None)):
            raise TypeError(
                f"initial_components should be a list of component classes or None, "
                f"got {initial_components}."
            )

        self._registry: dict[str, dict[str, type]] = {}
        self._relationship_manager = RelationshipManager()

        if initial_components is not None:
            for component in initial_components:
                self.register_component(component)

    @property
    def registry(self) -> dict[str, dict[str, type]]:
        return self._registry

    @registry.setter
    def registry(self, _) -> None:
        raise RuntimeError("It is not allowed to set the registry values directly.")

    @registry.deleter
    def registry(self, _) -> None:
        raise RuntimeError("It is not allowed to delete the registry list.")

    def __contains__(self, item: str) -> bool:
        """Indicates if some component is in the registry.

        Parameters
        ----------
        item : str
            The component name to be searched.

        Returns
        -------
        bool
            True if the component exists in the task registry, False otherwise.
        """
        if not isinstance(item, str):
            raise TypeError(f"The key should be str, got {item}.")

        for base_type_container in self._registry.values():
            if item in base_type_container:
                return True
        return False

    def __getitem__(self, key: str) -> type:
        """Obtains a component from the registry using an indexer.

        Parameters
        ----------
        key : str
            A string to be used as an indexer.

        Returns
        -------
        Type
            The object if it exists in the task registry.

        Raises
        ------
        TypeError
            If the indexer is not a string.
        KeyError
            If the object does not exist in the registry.
        """
        if not isinstance(key, str):
            raise TypeError(f"The indexer should be a string, got {key}.")

        for base_type_container in self._registry.values():
            if key in base_type_container:
                return base_type_container[key]

        raise KeyError(f"Component '{key}' does not exists in the registry.")

    def _get_base_type(self, new_component: type) -> str:
        # select only base classes ancestors
        component_base_ancestors = [
            ancestor
            for ancestor in new_component.__mro__
            if "Base" in ancestor.__name__
        ]

        base_classes_cantidates = [
            ancestor_cls
            for ancestor_cls in component_base_ancestors
            if hasattr(ancestor_cls, "TYPE")
        ]

        # check if there is only one type candidate.
        if len(base_classes_cantidates) == 0:
            raise TypeError(
                f"Component {new_component.__name__} does not a DashAI base class with "
                f"a 'TYPE' class attribute. Classes that the component extends (MRO): "
                f"{new_component.__mro__}"
            )
        elif len(base_classes_cantidates) > 1:
            raise TypeError(
                f"Component {new_component.__name__} has more than one base class with "
                f"a 'TYPE' class attribute: "
                f"{[_cls.__name__ for _cls in base_classes_cantidates]}."
            )

        return base_classes_cantidates[0].TYPE

    def register_component(self, new_component: type) -> None:
        """Register a component within the registry.

        Parameters
        ----------
        new_component : Type
            The object to be registred.

        Raises
        ------
        TypeError
            If the provided component is not a class.
        TypeError
            If some task that the component declares compatible does not exist in the
            taskm registry.
        """

        if not isinstance(new_component, type):
            raise TypeError(
                f'new_component "{new_component}" should be a class, '
                f"got {type(new_component)}."
            )

        base_type = self._get_base_type(new_component)

        is_configurable_object = "ConfigObject" in [
            _class.__name__ for _class in new_component.__mro__
        ]

        if is_configurable_object and not hasattr(new_component, "get_schema"):
            raise TypeError(
                f"The component {new_component.__name__} does not implement "
                '"get_schema" method although it was declared as a configurable '
                "object."
            )

        new_register_component = {
            "name": new_component.__name__,
            "type": base_type,
            "class": new_component,
            "configurable_object": is_configurable_object,
            "schema": new_component.get_schema() if is_configurable_object else None,
            "description": getattr(new_component, "DESCRIPTION", None),
        }

        if base_type not in self._registry:
            self._registry[base_type] = {new_component.__name__: new_register_component}
        else:
            self._registry[base_type][new_component.__name__] = new_register_component

        if hasattr(new_component, "_compatible_tasks"):
            for compatible_task in new_component._compatible_tasks:
                self._relationship_manager.add_relationship(
                    new_component.__name__,
                    compatible_task,
                )

    def query_components_by_type(
        self,
        select: str | list[str] | None = None,
        ignore: str | list[str] | None = None,
    ) -> list[str, dict[str, Any]]:
        """Obtains all the components according to the indicated types.

        Only one of select or ignore should be provided.
        In any other case an exception will be raised.

        Parameters
        ----------
        select : str | list[str] | None, optional
            The types of components selected for return, by default None
        ignore : str | list[str] | None, optional
            The types of components ignored for return., by default None

        Returns
        -------
        list[str, dict[str, Any]]
            A list with the selected components.

        Raises
        ------
        ValueError
            If select and ignore are not None.
        ValueError
            If select and ignore are None.
        TypeError
            When select provided, if select is not a string o a list of strings.
        TypeError
            When select provided, if some element of select list is not a string.
        ValueError
            When select provided, when a provided type does not exists in the registry.
        TypeError
            When ignore provided, if ignore is not a string o a list of strings.
        TypeError
            When ignore provided, if some element of ignore list is not a string.
        ValueError
            When ignore provided, when a provided type does not exists in the registry.
        """
        if select is not None and ignore is not None:
            raise ValueError(
                "Only select or ignore can be provided, not both at the same time."
            )

        if select is None and ignore is None:
            raise ValueError(
                "At least one of select or ignore parameters must be non-null."
            )

        # case 1: select is provided.
        if select is not None:
            # check passed select types
            if not isinstance(select, (str, list)):
                raise TypeError(
                    f"Select must be a string or an array of strings, got {select}."
                )
            for idx, type_ in enumerate(select):
                if not isinstance(type_, str):
                    raise TypeError(
                        f"type in position {idx} should be a string, got {type_}."
                    )
                if type_ not in self._registry:
                    raise ValueError(
                        f"Component type {type_} does not exists in the registry."
                    )

            # cast select into string
            if isinstance(select, str):
                select = [select]

            return [
                component
                for selected_type in select
                for component in self._registry[selected_type]
            ]

        # case 2: ignore is provided.
        else:
            # check passed ignore types
            if not isinstance(select, (str, list)):
                raise TypeError(
                    f"Ignore must be a string or an array of strings, got {ignore}."
                )
            # cast select into string
            if isinstance(select, str):
                select = [select]

            # check each type
            for idx, type_ in enumerate(ignore):
                if not isinstance(type_, str):
                    raise TypeError(
                        f"type in position {idx} should be a string, got {type_}."
                    )
                if type_ not in self._registry:
                    raise ValueError(
                        f"Component type {type_} does not exists in the registry."
                    )

            return [
                component
                for component_type in self.registry
                if component_type not in ignore
                for component in self._registry[component_type]
            ]

    def get_child_classes(self, parent_name: str) -> list[str]:
        """Obtain the compoments that inherits from the specified parent component.

        Note that the method will not raise an exception when a non existant parent
        name is passed.

        Parameters
        ----------
        parent_name : str
            Class name of the parent component

        Returns
        -------
        List[str]
            List of component names that inherits from the parent component.
        """
        selected_components = []
        for type_registry in self._registry.values():
            for component_dict in type_registry.values():
                component_bases = [
                    base_class.__name__
                    for base_class in component_dict["class"].__bases__
                    if base_class.__name__ != "object"
                ]
                if parent_name in component_bases:
                    selected_components.append(component_dict)

        return [component["name"] for component in selected_components]
