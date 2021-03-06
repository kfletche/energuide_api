import typing
from energuide import element
from energuide.exceptions import ElementGetValueError


class _Codes(typing.NamedTuple):
    wall: typing.List[str]
    window: typing.List[str]


class Codes(_Codes):

    EMPTY_SNIPPET: typing.Dict[str, typing.Dict[str, typing.List[str]]] = {
        'codes': {
            'wall': [],
            'window': [],
        }
    }

    def to_dict(self) -> typing.Dict[str, typing.Dict[str, typing.List[str]]]:
        return {
            'codes': {
                'wall': self.wall,
                'window': self.window,
            }
        }


class _HouseSnippet(typing.NamedTuple):
    ceilings: typing.List[str]
    floors: typing.List[str]
    walls: typing.List[str]
    doors: typing.List[str]
    windows: typing.List[str]
    heated_floor_area: typing.Optional[str]
    heating_cooling: typing.Optional[str]
    ventilation: typing.List[str]
    water_heating: typing.Optional[str]
    basements: typing.List[str]
    crawlspaces: typing.List[str]
    slabs: typing.List[str]


class HouseSnippet(_HouseSnippet):

    EMPTY_SNIPPET: typing.Dict[str, typing.Union[typing.List[str], typing.Optional[str]]] = {
        'ceilings': [],
        'floors': [],
        'walls': [],
        'doors': [],
        'windows': [],
        'heatedFloorArea': None,
        'heating_cooling': None,
        'ventilations': [],
        'waterHeatings': None,
        'basements': [],
        'crawlspaces': [],
        'slabs': [],
    }

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'ceilings': self.ceilings,
            'floors': self.floors,
            'walls': self.walls,
            'doors': self.doors,
            'windows': self.windows,
            'heatedFloorArea': self.heated_floor_area,
            'heating_cooling': self.heating_cooling,
            'ventilations': self.ventilation,
            'waterHeatings': self.water_heating,
            'basements': self.basements,
            'crawlspaces': self.crawlspaces,
            'slabs': self.slabs,
        }


class _EnergyUpgradesSnippet(typing.NamedTuple):
    upgrades: typing.List[str]


class EnergyUpgradesSnippet(_EnergyUpgradesSnippet):

    EMPTY_SNIPPET: typing.Dict[str, typing.List[str]] = {
        'upgrades': [],
    }

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'upgrades': self.upgrades,
        }


class _OtherDataSnippet(typing.NamedTuple):
    forward_sortation_area: typing.Optional[str]
    ers_rating: typing.Optional[str]


class OtherDataSnippet(_OtherDataSnippet):

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'forwardSortationArea': self.forward_sortation_area,
            'ersRating': self.ers_rating,
        }


def _extract_nodes(node: element.Element, path: str) -> typing.List[element.Element]:
    return node.xpath(path)


def _get_nullable_fields(root: element.Element, path: str) -> typing.Optional[str]:
    data: typing.Optional[str]
    try:
        data = root.get(path, str)
    except ElementGetValueError:
        data = None
    return data


def snip_other_data(root: element.Element) -> OtherDataSnippet:
    postal_code = _get_nullable_fields(root, 'ProgramInformation/Client/StreetAddress/PostalCode/text()')
    return OtherDataSnippet(
        forward_sortation_area=postal_code[0:3] if postal_code else None,
        ers_rating=_get_nullable_fields(root, 'Program/Results/Tsv/ERSRating/@value'),
    )


def snip_house(house: element.Element) -> HouseSnippet:
    ceilings = _extract_nodes(house, 'Components/Ceiling')
    floors = _extract_nodes(house, 'Components/Floor')
    walls = _extract_nodes(house, 'Components/Wall')
    doors = _extract_nodes(house, 'Components//Components/Door')
    windows = _extract_nodes(house, 'Components//Components/Window')
    heated_floor_area = _extract_nodes(house, 'Specifications/HeatedFloorArea')
    heating_cooling = _extract_nodes(house, 'HeatingCooling')
    heating_cooling_string = heating_cooling[0].to_string() if heating_cooling else None
    ventilation = _extract_nodes(house, 'Ventilation/WholeHouseVentilatorList/Hrv')
    ventilation_strings = [hrv.to_string() for hrv in ventilation]

    water_heating = _extract_nodes(house, 'Components/HotWater')
    water_heating_string = water_heating[0].to_string() if water_heating else None

    basements = _extract_nodes(house, 'Components/Basement')
    crawlspaces = _extract_nodes(house, 'Components/Crawlspace')
    slabs = _extract_nodes(house, 'Components/Slab')

    return HouseSnippet(
        ceilings=[node.to_string() for node in ceilings],
        floors=[node.to_string() for node in floors],
        walls=[node.to_string() for node in walls],
        doors=[node.to_string() for node in doors],
        windows=[node.to_string() for node in windows],
        heated_floor_area=heated_floor_area[0].to_string() if heated_floor_area else None,
        heating_cooling=heating_cooling_string,
        ventilation=ventilation_strings,
        water_heating=water_heating_string,
        basements=[node.to_string() for node in basements],
        crawlspaces=[node.to_string() for node in crawlspaces],
        slabs=[node.to_string() for node in slabs],
    )


def snip_codes(codes: element.Element) -> Codes:
    wall_codes = codes.xpath('Wall/*/Code')
    window_codes = codes.xpath('Window/*/Code')

    return Codes(
        wall=[node.to_string() for node in wall_codes],
        window=[node.to_string() for node in window_codes],
    )


def snip_energy_upgrades(energy_upgrades: element.Element) -> EnergyUpgradesSnippet:
    upgrades = _extract_nodes(energy_upgrades, 'Settings/*')

    return EnergyUpgradesSnippet(
        upgrades=[upgrade.to_string() for upgrade in upgrades],
    )
