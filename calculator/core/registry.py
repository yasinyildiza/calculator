"""A facade on top of standard libraries to collect a set of classes by their name.

Usage:
------
Imagine that you have a package where you define a set of classes
under different modules, each of them inherited from the same base class.

my_pack/my_mod1.py
class MyAwesomeClass1(BaseAwesomeClass):
    ...

my_pack/my_mod2.py
class MyAwesomeClass2(BaseAwesomeClass):
    ...

In another module, you will probably import and use these awesome classes.
Instead of importing them one by one, this module provides a programmatic way
to import all of them and store them in a registry.

The only prerequisite is that each of these awesome classes must have a unique
`name` attribute.

class MyAwesomeClass1(BaseAwesomeClass):
    name = "my_awesome_class_1"


class MyAwesomeClass2(BaseAwesomeClass):
    name = "my_awesome_class_2"


# initialize the registry with base awesome class
registry = Registry(element_cls=BaseAwesomeClass)

# register your package
registry.register_package(my_pack)

# find your awesome class by its name
my_awesome_cls = registry.get(name="my_awesome_class_1")

# instantiate your awesome class
my_awesome_object = my_awesome_cls(...)


Alternatively, you can do it in a more declarative way by inheriting from Registry.

class MyAwesomeRegistry(Registry):
    element_cls = BaseAwesomeClass
    package = my_pack
    auto_collect = True


registry = MyAwesomeRegistry()
my_awesome_cls = registry.get(name="my_awesome_class_1")
my_awesome_object = my_awesome_cls(...)
"""

import abc
import importlib
import inspect
import pkgutil
import types
import typing


class BaseElement(abc.ABC):
    """Base class for elements to be registered in the registry for convenience.

    The only requirement for a class to be registered in the registry is
    to have a `name` attribute at class level. So, subclassing BaseElement is optional.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return the unique name of the Element class."""


class RegistryError(Exception):
    """Base Registry Exception."""


class InvalidElementClassError(RegistryError):
    """Provided element_cls is invalid; i.e., does not have `name` attribute."""


class DuplicateElementError(RegistryError):
    """Element class already registered; i.e., duplicate name."""


class ElementNotFoundError(RegistryError):
    """Element for the given name not found in the registry."""


class Registry:
    """A class that registers subclasses of element_cls by their name.

    Attributes:
        element_cls:
            base class to be collected from the package/module
            defaults to BaseElement class
        module: python module to be traversed for the given element_cls
        package: python package to be traversed for the given element_cls
        auto_collect:
            indicates whether or not the classes should be auto collected
            without waiting for explicit register call
        collection: a dict to store the classes with their names as dict keys
    """

    def __init__(
        self,
        element_cls: typing.Optional[typing.Type] = None,
        module: types.ModuleType = None,
        package: types.ModuleType = None,
        auto_collect: typing.Optional[bool] = True,
    ):
        """Initialize registry class."""
        self._element_cls = element_cls
        self._module = module
        self._package = package
        self._auto_collect = auto_collect

        self.collection: dict = {}

    def __str__(self) -> str:
        """Return string representation of the collection."""
        return "-" + "\n-".join(list(self.collection.keys()))

    @property
    def element_cls(self) -> typing.Type:
        """Return base element class."""
        return self._element_cls or BaseElement

    @property
    def module(self) -> typing.Optional[types.ModuleType]:
        """Return root module to traverse."""
        return self._module

    @property
    def package(self) -> typing.Optional[types.ModuleType]:
        """Return root package to traverse."""
        return self._package

    @property
    def auto_collect(self) -> typing.Optional[bool]:
        """Return auto_collect."""
        return self._auto_collect

    def register(self, cls: typing.Type):
        """Register the given class by its name attribute.

        Args:
            cls: class to be registered with its name

        Raises:
            DuplicateElementError: if the name of the class is already registered
        """
        if cls.name in self.collection and id(cls) != id(self.collection[cls.name]):
            raise DuplicateElementError(
                f'"{cls.name}" is already in the registry:'
                f"\ncurrent  : {self.collection[cls.name]}"
                f"\nduplicate: {cls}"
                f"\ncurrent id  : {id(self.collection[cls.name])}"
                f"\nduplicate id: {id(cls)}"
                f"\ncurrent path  : {inspect.getfile(self.collection[cls.name])}"
                f"\nduplicate path: {inspect.getfile(cls)}"
            )

        self.collection[cls.name] = cls

    def register_class(self, cls):
        """Register the given class by if it is a subclass of element_cls.

        Args:
            cls: class to be registered with its name
        """
        if issubclass(cls, self.element_cls):
            self.register(cls)

    def register_module(self, module: types.ModuleType):
        """Traverse all classes under the given module and register them accordingly.

        Args:
            module: python module to be traversed
        """
        for _name, pyobj in inspect.getmembers(module, inspect.isclass):
            cls_module = inspect.getmodule(pyobj)
            if cls_module is None or cls_module.__file__ == module.__file__:
                self.register_class(pyobj)

    def register_package(self, package: types.ModuleType):
        """Traverse all classes under the given package and register them accordingly.

        Args:
            package: python package to be traversed with its subpackages and modules
        """
        for importer, name, is_package in pkgutil.iter_modules(package.__path__):
            spec = importer.find_spec(name, package.__path__)  # type: ignore
            pyobj = importlib.util.module_from_spec(spec)  # type: ignore
            spec.loader.exec_module(pyobj)  # type: ignore

            if is_package:
                self.register_package(pyobj)
            else:
                self.register_module(pyobj)

    def collect(self):
        """Collect the classes from the given package/module."""
        if self.collection:
            return

        if self.package is not None:
            self.register_package(self.package)

        if self.module is not None:
            self.register_module(self.module)

    def get(self, name: str) -> typing.Type:
        """Get the class by the given name from the collection.

        Args:
            name: name of the class to be searched in the collection

        Returns:
            class: the class that is found in the collection

        Raises:
            ElementNotFoundError: the given name is not found in the collection
        """
        if self.auto_collect:
            self.collect()

        try:
            cls = self.collection[name]
        except KeyError as exc:
            raise ElementNotFoundError(
                f'"{name}" not found in the registry\n{self}',
            ) from exc

        return cls

    def __getitem__(self, key: str) -> typing.Type:
        """Return item by the given key.

        dict-like interface for `get` method.

        Args:
            key: name of the element to search in the registry
        """
        return self.get(name=key)
