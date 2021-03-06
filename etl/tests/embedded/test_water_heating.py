import pytest
from energuide import element
from energuide.embedded import water_heating
from energuide.exceptions import InvalidEmbeddedDataTypeError


@pytest.fixture
def sample_ef() -> element.Element:
    data = """
<HotWater>
<Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
"""energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
    <EquipmentInformation>
        <Manufacturer>Wizard DHW man</Manufacturer>
        <Model>Wizard DHW mod</Model>
    </EquipmentInformation>
    <EnergySource code="1">
        <English>Electricity</English>
        <French>Électricité</French>
    </EnergySource>
    <TankType code="2">
        <English>Conventional tank</English>
        <French>Réservoir classique</French>
    </TankType>
    <TankVolume code="4" value="189.3001">
        <English>189.3 L, 41.6 Imp, 50 US gal</English>
        <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
    </TankVolume>
    <EnergyFactor code="1" value="0.8217" inputCapacity="0">
        <English>Use defaults</English>
        <French>Valeurs par défaut</French>
    </EnergyFactor>
    <TankLocation code="2">
        <English>Basement</English>
        <French>Sous-sol</French>
    </TankLocation>
</Primary>
</HotWater>
    """
    return element.Element.from_string(data)


@pytest.fixture
def sample_percentage() -> element.Element:
    data = """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
    """energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
        <EquipmentInformation>
            <Manufacturer>Wizard DHW man</Manufacturer>
            <Model>Wizard DHW mod</Model>
        </EquipmentInformation>
        <EnergySource code="1">
            <English>Electricity</English>
            <French>Électricité</French>
        </EnergySource>
        <TankType code="2">
            <English>Conventional tank</English>
            <French>Réservoir classique</French>
        </TankType>
        <TankVolume code="4" value="189.3001">
            <English>189.3 L, 41.6 Imp, 50 US gal</English>
            <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
        </TankVolume>
        <EnergyFactor code="3" standbyHeatLoss="49" standbyHeatLossMode="0" thermalEfficiency="98" inputCapacity="3800">
            <English>Standby</English>
            <French>Mode d'attente</French>
        </EnergyFactor>
        <TankLocation code="2">
            <English>Basement</English>
            <French>Sous-sol</French>
        </TankLocation>
    </Primary>
</HotWater>
    """
    return element.Element.from_string(data)


@pytest.fixture
def sample_drain_water_heat_recovery() -> element.Element:
    data = """
<HotWater id="19">
    <Primary hasDrainWaterHeatRecovery="true" insulatingBlanket="0" combinedFlue="false" """ + \
    """flueDiameter="76.2" energyStar="false" ecoEnergy="false" userDefinedPilot="false" pilotEnergy="0">
        <EquipmentInformation>
            <Manufacturer>Triangle Tube</Manufacturer>
            <Model>Prestige Excellence</Model>
        </EquipmentInformation>
        <EnergySource code="2">
            <English>Natural gas</English>
            <French>Gaz naturel</French>
        </EnergySource>
        <TankType code="5">
            <English>Instantaneous</English>
            <French>Instantané</French>
        </TankType>
        <TankVolume code="7" value="0">
            <English>Not applicable</English>
            <French>Sans objet</French>
        </TankVolume>
        <EnergyFactor code="2" value="0.79" inputCapacity="0">
            <English>User specified</English>
            <French>Spécifié par l'utilisateur</French>
        </EnergyFactor>
        <TankLocation code="2">
            <English>Basement</English>
            <French>Sous-sol</French>
        </TankLocation>
        <DrainWaterHeatRecovery showerLength="6.5" dailyShowers="2.2286" """ + \
        """preheatShowerTank="false" effectivenessAt9.5="41.5">
            <Efficiency code="2" />
            <EquipmentInformation>
                <Manufacturer>Generic</Manufacturer>
                <Model>1-Low Efficiency</Model>
            </EquipmentInformation>
            <ShowerTemperature code="2">
                <English>Warm 41°C (106°F)</English>
                <French>Tempérée 41°C (106°F)</French>
            </ShowerTemperature>
            <ShowerHead code="2">
                <English>Standard 9.5 L/min (2.5 US gpm)</English>
                <French>Standard 9.5 L/min (2.5 ÉU gpm)</French>
            </ShowerHead>
        </DrainWaterHeatRecovery>
    </Primary>
</HotWater>
    """
    return element.Element.from_string(data)


BAD_XML_DATA = [
    # This XML block is missing all subtags of the <Primary> tag
    """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
    """energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
    </Primary>
</HotWater>
    """,

    # This XML block has EnergySource and TankType <English> tag text that does not map to an existing tank type
    """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
    """energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
        <EquipmentInformation>
            <Manufacturer>Wizard DHW man</Manufacturer>
            <Model>Wizard DHW mod</Model>
        </EquipmentInformation>
        <EnergySource code="1">
            <English>Something That Doesn't Exist</English>
            <French>Électricité</French>
        </EnergySource>
        <TankType code="2">
            <English>Something That Doesn't Exist tank</English>
            <French>Réservoir classique</French>
        </TankType>
        <TankVolume code="4" value="189.3001">
            <English>189.3 L, 41.6 Imp, 50 US gal</English>
            <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
        </TankVolume>
        <EnergyFactor code="1" value="0.8217" inputCapacity="0">
            <English>Use defaults</English>
            <French>Valeurs par défaut</French>
        </EnergyFactor>
        <TankLocation code="2">
            <English>Basement</English>
            <French>Sous-sol</French>
        </TankLocation>
    </Primary>
</HotWater>
    """,

    # This XML block is missing the value attribute on <TankVolume> and <EnergyFactor> tags
    """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
    """energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
        <EquipmentInformation>
            <Manufacturer>Wizard DHW man</Manufacturer>
            <Model>Wizard DHW mod</Model>
        </EquipmentInformation>
        <EnergySource code="1">
            <English>Electricity</English>
            <French>Électricité</French>
        </EnergySource>
        <TankType code="2">
            <English>Conventional tank</English>
            <French>Réservoir classique</French>
        </TankType>
        <TankVolume code="4">
            <English>189.3 L, 41.6 Imp, 50 US gal</English>
            <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
        </TankVolume>
        <EnergyFactor>
            <English>Use defaults</English>
            <French>Valeurs par défaut</French>
        </EnergyFactor>
        <TankLocation code="2">
            <English>Basement</English>
            <French>Sous-sol</French>
        </TankLocation>
    </Primary>
</HotWater>
    """,

    # This XML block has non-numeric string for the value attribute of the <TankVolume> and <EnergyFactor>
    """
<HotWater>
    <Primary hasDrainWaterHeatRecovery="false" insulatingBlanket="0" combinedFlue="false" flueDiameter="0" """ + \
    """energyStar="false" ecoEnergy="false" userDefinedPilot="false" connectedUnitsDwhr="0">
        <EquipmentInformation>
            <Manufacturer>Wizard DHW man</Manufacturer>
            <Model>Wizard DHW mod</Model>
        </EquipmentInformation>
        <EnergySource code="1">
            <English>Electricity</English>
            <French>Électricité</French>
        </EnergySource>
        <TankType code="2">
            <English>Conventional tank</English>
            <French>Réservoir classique</French>
        </TankType>
        <TankVolume code="4" value="bad">
            <English>189.3 L, 41.6 Imp, 50 US gal</English>
            <French>189.3 L, 41.6 imp, 50 gal ÉU</French>
        </TankVolume>
        <EnergyFactor code="1" value="data" inputCapacity="0">
            <English>Use defaults</English>
            <French>Valeurs par défaut</French>
        </EnergyFactor>
        <TankLocation code="2">
            <English>Basement</English>
            <French>Sous-sol</French>
        </TankLocation>
    </Primary>
</HotWater>
    """
]


def test_from_data_ef(sample_ef: element.Element) -> None:
    output = water_heating.WaterHeating.from_data(sample_ef)[0]
    assert output.water_heater_type == water_heating.WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK
    assert output.efficiency_ef == 0.8217


def test_from_data_percentage(sample_percentage: element.Element) -> None:
    output = water_heating.WaterHeating.from_data(sample_percentage)[0]
    assert output.water_heater_type == water_heating.WaterHeaterType.ELECTRICITY_CONVENTIONAL_TANK
    assert output.efficiency_percentage == 98.0


def test_drain_water_heat_recovery(sample_drain_water_heat_recovery: element.Element) -> None:
    output = water_heating.WaterHeating.from_data(sample_drain_water_heat_recovery)[0]
    assert output.drain_water_heat_recovery_efficiency_percentage == 41.5


@pytest.mark.parametrize("bad_xml", BAD_XML_DATA)
def test_bad_data(bad_xml: str) -> None:
    water_heating_node = element.Element.from_string(bad_xml)
    with pytest.raises(InvalidEmbeddedDataTypeError) as excinfo:
        water_heating.WaterHeating.from_data(water_heating_node)

    assert excinfo.value.data_class == water_heating.WaterHeating


def test_to_dict(sample_ef: element.Element) -> None:
    output = water_heating.WaterHeating.from_data(sample_ef)[0].to_dict()
    assert output == {
        'typeEnglish': 'Electric storage tank',
        'typeFrench': 'Réservoir électrique',
        'tankVolumeLitres': 189.3001,
        'tankVolumeGallon': 50.0077860172,
        'efficiencyEf': 0.8217,
        'efficiencyPercentage': None,
        'drainWaterHeatRecoveryEfficiencyPercentage': None,
    }


def test_properties(sample_ef: element.Element) -> None:
    output = water_heating.WaterHeating.from_data(sample_ef)[0]
    assert output.tank_volume_gallon == 50.0077860172
