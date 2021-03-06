import copy
import datetime
import typing
import pytest
from energuide import dwelling
from energuide.embedded import upgrade
from energuide.embedded import measurement
from energuide.embedded import composite
from energuide.embedded import walls
from energuide.embedded import region
from energuide.embedded import evaluation_type
from energuide.exceptions import InvalidInputDataError
from energuide.exceptions import InvalidGroupSizeError


# pylint: disable=no-self-use


@pytest.fixture
def upgrades_input() -> typing.List[str]:
    return [
        '<Ceilings cost="0" priority="12" />',
        '<MainWalls cost="1" priority="2" />',
        '<Foundation cost="2" priority="3" />',
        ]


@pytest.fixture
def sample_input_d(upgrades_input: typing.List[str]) -> typing.Dict[str, typing.Any]:

    return {
        'HOUSE_ID': '456',
        'EVAL_ID': '123',
        'EVAL_TYPE': 'D',
        'ENTRYDATE': '2018-01-01',
        'CREATIONDATE': '2018-01-08 09:00:00',
        'MODIFICATIONDATE': '2018-06-01 09:00:00',
        'CLIENTCITY': 'Ottawa',
        'forwardSortationArea': 'K1P',
        'HOUSEREGION': 'Ontario',
        'YEARBUILT': '2000',
        'BUILDER': '4K13D01404',
        'HEATEDFLOORAREA': '12.34',
        'TYPEOFHOUSE': 'Single detached',
        'ERSRATING': '567',
        'UGRERSRATING': '565',
        'ERSGHG': '12.5',
        'UGRERSGHG': '12.34',
        'upgrades': upgrades_input,
        'ERSENERGYINTENSITY': '0.82',
        'UGRERSENERGYINTENSITY': '0.80',
        'EGHRATING': '50.5',
        'UGRRATING': '49.0',

        'WALLDEF': '45.3;12;50;12;4.7;12',
        'UGRWALLDEF': '45.3;12;50;12;4.7;10',
        'EGHHLWALLS': '27799.9',
        'UGRHLWALLS': '27799.9',
        'EGHDESHTLOSS': '11242.1',
        'UGRDESHTLOSS': '10757.3',
    }


@pytest.fixture
def sample_input_e(sample_input_d: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    output = copy.deepcopy(sample_input_d)
    output['EVAL_TYPE'] = 'E'
    output['ENTRYDATE'] = '2018-01-02'
    return output


@pytest.fixture
def sample_input_missing(sample_input_d: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    output = copy.deepcopy(sample_input_d)
    output['MODIFICATIONDATE'] = None
    output['ERSRATING'] = None
    output['UGRERSRATING'] = None
    return output


@pytest.fixture
def sample_parsed_d(sample_input_d: typing.Dict[str, typing.Any]) -> dwelling.ParsedDwellingDataRow:
    return dwelling.ParsedDwellingDataRow.from_row(sample_input_d)


@pytest.fixture
def sample_parsed_e(sample_input_e: typing.Dict[str, typing.Any]) -> dwelling.ParsedDwellingDataRow:
    return dwelling.ParsedDwellingDataRow.from_row(sample_input_e)



class TestParsedDwellingDataRow:

    def test_from_row(self, sample_input_d: typing.Dict[str, typing.Any]) -> None:
        output = dwelling.ParsedDwellingDataRow.from_row(sample_input_d)

        assert output == dwelling.ParsedDwellingDataRow(
            house_id=456,
            eval_id=123,
            file_id='4K13D01404',
            eval_type=evaluation_type.EvaluationType.PRE_RETROFIT,
            entry_date=datetime.date(2018, 1, 1),
            creation_date=datetime.datetime(2018, 1, 8, 9),
            modification_date=datetime.datetime(2018, 6, 1, 9),
            year_built=2000,
            city='Ottawa',
            region=region.Region.ONTARIO,
            forward_sortation_area='K1P',
            energy_upgrades=[
                upgrade.Upgrade(
                    upgrade_type='Ceilings',
                    cost=0,
                    priority=12,
                ),
                upgrade.Upgrade(
                    upgrade_type='MainWalls',
                    cost=1,
                    priority=2,
                ),
                upgrade.Upgrade(
                    upgrade_type='Foundation',
                    cost=2,
                    priority=3,
                ),
            ],
            house_type='Single detached',
            heated_floor_area=12.34,
            egh_rating=measurement.Measurement(
                measurement=50.5,
                upgrade=49.0,
            ),
            ers_rating=measurement.Measurement(
                measurement=567,
                upgrade=565,
            ),
            greenhouse_gas_emissions=measurement.Measurement(
                measurement=12.5,
                upgrade=12.34,
            ),
            energy_intensity=measurement.Measurement(
                measurement=0.82,
                upgrade=0.80,
            ),
            walls=measurement.Measurement(
                measurement=walls.Wall(
                    insulation=[
                        composite.CompositeValue(
                            percentage=45.3,
                            value=12.0,
                            value_name='rValue'
                        ),
                        composite.CompositeValue(
                            percentage=50.0,
                            value=12.0,
                            value_name='rValue'
                        ),
                        composite.CompositeValue(
                            percentage=4.7,
                            value=12.0,
                            value_name='rValue'
                        ),
                    ],
                    heat_lost=27799.9
                ),
                upgrade=walls.Wall(
                    insulation=[
                        composite.CompositeValue(
                            percentage=45.3,
                            value=12.0,
                            value_name='rValue'
                        ),
                        composite.CompositeValue(
                            percentage=50.0,
                            value=12.0,
                            value_name='rValue'
                        ),
                        composite.CompositeValue(
                            percentage=4.7,
                            value=10.0,
                            value_name='rValue'
                        ),
                    ],
                    heat_lost=27799.9
                )
            ),
            design_heat_loss=measurement.Measurement(
                measurement=11242.1,
                upgrade=10757.3,
            ),
        )

    def test_null_fields_are_accepted(self, sample_input_missing: typing.Dict[str, typing.Any]) -> None:
        output = dwelling.ParsedDwellingDataRow.from_row(sample_input_missing)

        assert output.modification_date is None
        assert output.ers_rating == measurement.Measurement(None, None)

    def test_bad_postal_code(self, sample_input_d: typing.Dict[str, typing.Any]) -> None:
        sample_input_d['forwardSortationArea'] = 'K16'
        with pytest.raises(InvalidInputDataError):
            dwelling.ParsedDwellingDataRow.from_row(sample_input_d)

    def test_from_bad_row(self) -> None:
        input_data = {
            'EVAL_ID': 123
        }
        with pytest.raises(InvalidInputDataError) as ex:
            dwelling.ParsedDwellingDataRow.from_row(input_data)
        assert 'EVAL_TYPE' in ex.exconly()
        assert 'EVAL_ID' not in ex.exconly()


class TestDwellingEvaluation:

    def test_eval_type(self, sample_parsed_d: dwelling.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.evaluation_type == evaluation_type.EvaluationType.PRE_RETROFIT

    def test_entry_date(self, sample_parsed_d: dwelling.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.entry_date == datetime.date(2018, 1, 1)

    def test_creation_date(self, sample_parsed_d: dwelling.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.creation_date == datetime.datetime(2018, 1, 8, 9)

    def test_modification_date(self, sample_parsed_d: dwelling.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d)
        assert output.modification_date == datetime.datetime(2018, 6, 1, 9)

    def test_to_dict(self, sample_parsed_d: dwelling.ParsedDwellingDataRow) -> None:
        output = dwelling.Evaluation.from_data(sample_parsed_d).to_dict()
        assert output == {
            'fileId': '4K13D01404',
            'evaluationId': 123,
            'houseType': 'Single detached',
            'evaluationType': evaluation_type.EvaluationType.PRE_RETROFIT.value,
            'entryDate': '2018-01-01',
            'creationDate': '2018-01-08T09:00:00',
            'modificationDate': '2018-06-01T09:00:00',
            'energyUpgrades': [
                {
                    'upgradeType': 'Ceilings',
                    'cost': 0,
                    'priority': 12,
                },
                {
                    'upgradeType': 'MainWalls',
                    'cost': 1,
                    'priority': 2,
                },
                {
                    'upgradeType': 'Foundation',
                    'cost': 2,
                    'priority': 3,
                },
            ],
            'heatedFloorArea': 12.34,
            'eghRating': {
                'measurement': 50.5,
                'upgrade': 49.0,
            },
            'ersRating': {
                'measurement': 567,
                'upgrade': 565,
            },
            'greenhouseGasEmissions': {
                'measurement': 12.5,
                'upgrade': 12.34,
            },
            'energyIntensity': {
                'measurement': 0.82,
                'upgrade': 0.80,
            },
            'walls': {
                'measurement': {
                    'insulation': [
                        {
                            'percentage': 45.3,
                            'rValue': 12.0,
                        },
                        {
                            'percentage': 50.0,
                            'rValue': 12.0,
                        },
                        {
                            'percentage': 4.7,
                            'rValue': 12.0,
                        },
                    ],
                    'heatLost': 27799.9
                },
                'upgrade': {
                    'insulation': [
                        {
                            'percentage': 45.3,
                            'rValue': 12.0,
                        },
                        {
                            'percentage': 50.0,
                            'rValue': 12.0,
                        },
                        {
                            'percentage': 4.7,
                            'rValue': 10.0,
                        },
                    ],
                    'heatLost': 27799.9
                }
            },
            'designHeatLoss': {
                'measurement': 11242.1,
                'upgrade': 10757.3,
            }
        }


class TestDwelling:

    @pytest.fixture
    def sample(self,
               sample_input_d: typing.Dict[str, typing.Any],
               sample_input_e: typing.Dict[str, typing.Any],
              ) -> typing.List[typing.Dict[str, typing.Any]]:
        return [sample_input_d, sample_input_e].copy()

    @pytest.fixture
    def dummy_sample(self,
                     sample_input_d: typing.Dict[str, typing.Any],
                     sample_input_e: typing.Dict[str, typing.Any],
                    ) -> typing.List[typing.Dict[str, typing.Any]]:
        dummy_d = sample_input_e.copy()
        dummy_d['EVAL_TYPE'] = 'D'

        new_e = sample_input_e.copy()
        new_e['ENTRYDATE'] = '2018-06-01'

        new_f = sample_input_e.copy()
        new_f['EVAL_TYPE'] = 'F'
        new_f['ENTRYDATE'] = '2018-08-01'

        return [sample_input_d, sample_input_e, dummy_d, new_e, new_f].copy()

    def test_house_id(self, sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert output.house_id == 456

    def test_year_built(self, sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert output.year_built == 2000

    def test_address_data(self, sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert output.city == 'Ottawa'
        assert output.region == region.Region.ONTARIO
        assert output.forward_sortation_area == 'K1P'

    def test_evaluations(self, sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(sample)
        assert len(output.evaluations) == 2

    def test_no_data(self) -> None:
        data: typing.List[typing.Any] = []
        with pytest.raises(InvalidGroupSizeError):
            dwelling.Dwelling.from_group(data)

    def test_to_dict(self, sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(sample).to_dict()
        evaluations = output.pop('evaluations')

        assert output == {
            'houseId': 456,
            'yearBuilt': 2000,
            'city': 'Ottawa',
            'region': region.Region.ONTARIO.value,
            'forwardSortationArea': 'K1P',
        }

        assert 'postalCode' not in output
        assert len(evaluations) == 2

    def test_filter_dummies(self, dummy_sample: typing.List[typing.Dict[str, typing.Any]]) -> None:
        output = dwelling.Dwelling.from_group(dummy_sample)
        assert len(output.evaluations) == 4
