import typing
from lxml import etree
from energuide.exceptions import EnerguideError, ElementGetValueError


class MalformedXmlError(EnerguideError):
    pass


T = typing.TypeVar('T', int, float, str)


class Element:

    _PARSER = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

    def __init__(self, node: etree._Element) -> None:
        self.__node = node

    @classmethod
    def new(cls, tag: str) -> 'Element':
        return cls(etree.Element(tag))

    @classmethod
    def from_string(cls, data: str) -> 'Element':
        output: typing.Optional[etree._Element] = etree.fromstring(data.encode('utf-8'), parser=cls._PARSER)
        if output is None:
            raise MalformedXmlError(f'Invalid XML fragment: {data}')
        return cls(output)

    @classmethod
    def parse(cls, *args, **kwargs):
        output = etree.parse(*args, **kwargs)
        return cls(output.find('.'))

    def findtext(self, *args, **kwargs) -> typing.Optional[str]:
        return self.__node.findtext(*args, **kwargs)

    def get_text(self, *args, **kwargs) -> str:
        result: typing.Optional[str] = self.__node.findtext(*args, **kwargs)
        if result is None:
            error_message = (
                f"Couldn't find text at path {args[0]} in tag {self.tag}"
                if args
                else "Couldn't find text in {self.tag}"
            )
            raise ElementGetValueError(error_message)
        return result

    @property
    def attrib(self) -> typing.Dict[str, typing.Any]:
        return self.__node.attrib

    def xpath(self, *args, **kwargs) -> typing.List[typing.Any]:
        output = self.__node.xpath(*args, **kwargs)
        return [Element(node) if isinstance(node, etree._Element) else node for node in output]

    def find(self, *args, **kwargs) -> typing.Optional['Element']:
        output = self.__node.find(*args, **kwargs)
        return Element(output) if output is not None else None

    def to_string(self) -> str:
        return etree.tostring(self.__node, encoding='unicode')

    def __iter__(self) -> typing.Iterator[typing.Any]:
        for child in self.__node.__iter__():
            yield Element(child)

    @property
    def tag(self) -> str:
        return self.__node.tag

    def insert(self, index: int, element: 'Element') -> None:
        self.__node.insert(index, element.__node)

    def get(self, xpath: str, type_: typing.Type[T]) -> T:
        try:
            value = self.__node.xpath(xpath)[0]
        except IndexError as ex:
            raise ElementGetValueError(f"Couldn't find element at {xpath} in {self.tag}") from ex

        try:
            result = type_(value)
        except ValueError as ex:
            raise ElementGetValueError(f"Unable to cast {value} to {type_} in {self.tag}") from ex
        return typing.cast(T, result)
