from __future__ import annotations

from aenum import Enum, NoAlias


class MethodFullName(str, Enum):
    """
    Enumeration of impact methods supported by Brightway.
    So far, only some ReCiPe methods, and all EF v3.0 impact methods are supported.
    """

    # EFV3
    EFV3_ACIDIFICATION = "('EF v3.0', 'acidification', 'accumulated exceedance (AE)')"
    EFV3_CLIMATE_CHANGE = (
        "('EF v3.0', 'climate change', 'global warming potential (GWP100)')"
    )
    EFV3_CLIMATE_CHANGE_BIOGENIC = (
        "('EF v3.0', 'climate change: biogenic', 'global warming potential (GWP100)')"
    )
    EFV3_CLIMATE_CHANGE_FOSSIL = (
        "('EF v3.0', 'climate change: fossil', 'global warming potential (GWP100)')"
    )
    EFV3_CLIMATE_CHANGE_LAND_USE = "('EF v3.0', 'climate change: land use and land use change', 'global warming potential (GWP100)')"
    EFV3_ECOTOXICITY_FRESHWATER = "('EF v3.0', 'ecotoxicity: freshwater', 'comparative toxic unit for ecosystems (CTUe)')"
    EFV3_ECOTOXICITY_FRESHWATER_INORGANICS = "('EF v3.0', 'ecotoxicity: freshwater, inorganics', 'comparative toxic unit for ecosystems (CTUe)')"
    EFV3_ECOTOXICITY_FRESHWATER_METALS = "('EF v3.0', 'ecotoxicity: freshwater, metals', 'comparative toxic unit for ecosystems (CTUe)')"
    EFV3_ECOTOXICITY_FRESHWATER_ORGANICS = "('EF v3.0', 'ecotoxicity: freshwater, organics', 'comparative toxic unit for ecosystems (CTUe)')"
    EFV3_EUTROPHICATION_FRESHWATER = "('EF v3.0', 'eutrophication: freshwater', 'fraction of nutrients reaching freshwater end compartment (P)')"
    EFV3_EUTROPHICATION_MARINE = "('EF v3.0', 'eutrophication: marine', 'fraction of nutrients reaching marine end compartment (N)')"
    EFV3_EUTROPHICATION_TERRESTRIAL = (
        "('EF v3.0', 'eutrophication: terrestrial', 'accumulated exceedance (AE)')"
    )
    EFV3_HUMAN_TOXICITY_CARCINOGENIC = "('EF v3.0', 'human toxicity: carcinogenic', 'comparative toxic unit for human (CTUh)')"
    EFV3_HUMAN_TOXICITY_CARCINOGENIC_INORGANICS = "('EF v3.0', 'human toxicity: carcinogenic, inorganics', 'comparative toxic unit for human (CTUh)')"
    EFV3_HUMAN_TOXICITY_CARCINOGENIC_METALS = "('EF v3.0', 'human toxicity: carcinogenic, metals', 'comparative toxic unit for human (CTUh)')"
    EFV3_HUMAN_TOXICITY_CARCINOGENIC_ORGANICS = "('EF v3.0', 'human toxicity: carcinogenic, organics', 'comparative toxic unit for human (CTUh)')"
    EFV3_HUMAN_TOXICITY_NON_CARCINOGENIC = "('EF v3.0', 'human toxicity: non-carcinogenic', 'comparative toxic unit for human (CTUh)')"
    EFV3_HUMAN_TOXICITY_NON_CARCINOGENIC_INORGANICS = "('EF v3.0', 'human toxicity: non-carcinogenic, inorganics', 'comparative toxic unit for human (CTUh)')"
    EFV3_HUMAN_TOXICITY_NON_CARCINOGENIC_METALS = "('EF v3.0', 'human toxicity: non-carcinogenic, metals', 'comparative toxic unit for human (CTUh)')"
    EFV3_HUMAN_TOXICITY_NON_CARCINOGENIC_ORGANICS = "('EF v3.0', 'human toxicity: non-carcinogenic, organics', 'comparative toxic unit for human (CTUh)')"
    EFV3_IONISING_RADIATION = "('EF v3.0', 'ionising radiation: human health', 'human exposure efficiency relative to u235')"
    EFV3_LAND_USE = "('EF v3.0', 'land use', 'soil quality index')"
    EFV3_MATERIAL_RESOURCES = "('EF v3.0', 'material resources: metals/minerals', 'abiotic depletion potential (ADP): elements (ultimate reserves)')"
    EFV3_ENERGY_RESOURCES = "('EF v3.0', 'energy resources: non-renewable', 'abiotic depletion potential (ADP): fossil fuels')"
    EFV3_OZONE_DEPLETION = (
        "('EF v3.0', 'ozone depletion', 'ozone depletion potential (ODP)')"
    )
    EFV3_PARTICULATE_MATTER_FORMATION = (
        "('EF v3.0', 'particulate matter formation', 'impact on human health')"
    )
    EFV3_PHOTOCHEMICAL_OZONE_FORMATION = "('EF v3.0', 'photochemical oxidant formation: human health', 'tropospheric ozone concentration increase')"
    EFV3_WATER_USE = "('EF v3.0', 'water use', 'user deprivation potential (deprivation-weighted water consumption)')"

    # EF31
    EFV31_ACIDIFICATION = "(‘EF v3.1’, ‘acidification’, ‘accumulated exceedance (AE)’)"
    EFV31_CLIMATE_CHANGE = (
        "(‘EF v3.1’, ‘climate change’, ‘global warming potential (GWP100)’)"
    )
    EFV31_CLIMATE_CHANGE_BIOGENIC = (
        "(‘EF v3.1’, ‘climate change: biogenic’, ‘global warming potential (GWP100)’)"
    )
    EFV31_CLIMATE_CHANGE_FOSSIL = (
        "(‘EF v3.1’, ‘climate change: fossil’, ‘global warming potential (GWP100)’)"
    )
    EFV31_CLIMATE_CHANGE_LAND_USE = "(‘EF v3.1’, ‘climate change: land use and land use change’, ‘global warming potential (GWP100)’)"
    EFV31_ECOTOXICITY_FRESHWATER = "(‘EF v3.1’, ‘ecotoxicity: freshwater’, ‘comparative toxic unit for ecosystems (CTUe)’)"
    EFV31_ECOTOXICITY_FRESHWATER_INORGANICS = "(‘EF v3.1’, ‘ecotoxicity: freshwater, inorganics’, ‘comparative toxic unit for ecosystems (CTUe)’)"
    EFV31_ECOTOXICITY_FRESHWATER_ORGANICS = "(‘EF v3.1’, ‘ecotoxicity: freshwater, organics’, ‘comparative toxic unit for ecosystems (CTUe)’)"
    EFV31_ENERGY_RESOURCES = "(‘EF v3.1’, ‘energy resources: non-renewable’, ‘abiotic depletion potential (ADP): fossil fuels’)"
    EFV31_EUTROPHICATION_FRESHWATER = "(‘EF v3.1’, ‘eutrophication: freshwater’, ‘fraction of nutrients reaching freshwater end compartment (P)’)"
    EFV31_EUTROPHICATION_MARINE = "(‘EF v3.1’, ‘eutrophication: marine’, ‘fraction of nutrients reaching marine end compartment (N)’)"
    EFV31_EUTROPHICATION_TERRESTRIAL = (
        "(‘EF v3.1’, ‘eutrophication: terrestrial’, ‘accumulated exceedance (AE)’)"
    )
    EFV31_HUMAN_TOXICITY_CARCINOGENIC = "(‘EF v3.1’, ‘human toxicity: carcinogenic’, ‘comparative toxic unit for human (CTUh)’)"
    EFV31_HUMAN_TOXICITY_CARCINOGENIC_INORGANICS = "(‘EF v3.1’, ‘human toxicity: carcinogenic, inorganics’, ‘comparative toxic unit for human (CTUh)’)"
    EFV31_HUMAN_TOXICITY_CARCINOGENIC_ORGANICS = "(‘EF v3.1’, ‘human toxicity: carcinogenic, organics’, ‘comparative toxic unit for human (CTUh)’)"
    EFV31_HUMAN_TOXICITY_NON_CARCINOGENIC = "(‘EF v3.1’, ‘human toxicity: non-carcinogenic’, ‘comparative toxic unit for human (CTUh)’)"
    EFV31_HUMAN_TOXICITY_NON_CARCINOGENIC_INORGANICS = "(‘EF v3.1’, ‘human toxicity: non-carcinogenic, inorganics’, ‘comparative toxic unit for human (CTUh)’)"
    EFV31_HUMAN_TOXICITY_NON_CARCINOGENIC_ORGANICS = "(‘EF v3.1’, ‘human toxicity: non-carcinogenic, organics’, ‘comparative toxic unit for human (CTUh)’)"
    EFV31_IONISING_RADIATION = "(‘EF v3.1’, ‘ionising radiation: human health’, ‘human exposure efficiency relative to u235’)"
    EFV31_LAND_USE = "(‘EF v3.1’, ‘land use’, ‘soil quality index’)"
    EFV31_MATERIAL_RESOURCES = "(‘EF v3.1’, ‘material resources: metals/minerals’, ‘abiotic depletion potential (ADP): elements (ultimate reserves)’)"
    EFV31_OZONE_DEPLETION = (
        "(‘EF v3.1’, ‘ozone depletion’, ‘ozone depletion potential (ODP)’)"
    )
    EFV31_PARTICULATE_MATTER_FORMATION = (
        "(‘EF v3.1’, ‘particulate matter formation’, ‘impact on human health’)"
    )
    EFV31_PHOTOCHEMICAL_OZONE_FORMATION = "(‘EF v3.1’, ‘photochemical oxidant formation: human health’, ‘tropospheric ozone concentration increase’)"
    EFV31_WATER_USE = "(‘EF v3.1’, ‘water use’, ‘user deprivation potential (deprivation-weighted water consumption)’)"

    def to_short_name(self) -> MethodShortName:
        """
        Convert a full impact name (as specified in Brightway) to its shorter version.
        :return: short name version of full impact name.
        """
        return MethodShortName[self.name]


class MethodShortName(str, Enum):
    """
    Short version of impact methods supported by Brightway, to ease readability of
    figures.
    So far, only EF v3.0 and EF v3.1 impact methods are supported.
    """

    _settings_ = NoAlias

    # EFV3
    EFV3_ACIDIFICATION = "Acification (AE)"
    EFV3_CLIMATE_CHANGE = "Climate change (GWP100)"
    EFV3_CLIMATE_CHANGE_BIOGENIC = "Climate change: biogenic (GWP100)"
    EFV3_CLIMATE_CHANGE_FOSSIL = "Climate change: fossil (GWP100)"
    EFV3_CLIMATE_CHANGE_LAND_USE = "Climate change: land use/land use change (GWP100)"
    EFV3_ECOTOXICITY_FRESHWATER = "Ecotoxicity: freshwater (CTUe)"
    EFV3_ECOTOXICITY_FRESHWATER_INORGANICS = (
        "Ecotoxicity: freshwater, inorganics (CTUe)"
    )
    EFV3_ECOTOXICITY_FRESHWATER_METALS = "Ecotoxicity: freshwater, metals (CTUe)"
    EFV3_ECOTOXICITY_FRESHWATER_ORGANICS = "Ecotoxicity: freshwater, organics (CTUe)"
    EFV3_EUTROPHICATION_FRESHWATER = "Eutrophication: freshwater (kgPeq)"
    EFV3_EUTROPHICATION_MARINE = "Eutrophication: marine (N)"
    EFV3_EUTROPHICATION_TERRESTRIAL = "Eutrophication: terrestrial (AE)"
    EFV3_HUMAN_TOXICITY_CARCINOGENIC = "Human toxicity: carcinogenic (CTUh)"
    EFV3_HUMAN_TOXICITY_CARCINOGENIC_INORGANICS = (
        "Human toxicity: carcinogenic, inorganics (CTUh)"
    )
    EFV3_HUMAN_TOXICITY_CARCINOGENIC_METALS = (
        "Human toxicity: carcinogenic, metals (CTUh)"
    )
    EFV3_HUMAN_TOXICITY_CARCINOGENIC_ORGANICS = (
        "Human toxicity: carcinogenic, organics (CTUh)"
    )
    EFV3_HUMAN_TOXICITY_NON_CARCINOGENIC = "Human toxicity: non-carcinogenic (CTUh)"
    EFV3_HUMAN_TOXICITY_NON_CARCINOGENIC_INORGANICS = (
        "Human toxicity: non-carcinogenic, inorganics (CTUh)"
    )
    EFV3_HUMAN_TOXICITY_NON_CARCINOGENIC_METALS = (
        "Human toxicity: non-carcinogenic, metals (CTUh)"
    )
    EFV3_HUMAN_TOXICITY_NON_CARCINOGENIC_ORGANICS = (
        "Human toxicity: non-carcinogenic, organics (CTUh)"
    )
    EFV3_IONISING_RADIATION = "Ionising radiation: human health (kBqU235)"
    EFV3_LAND_USE = "Land use (soil quality index)"
    EFV3_MATERIAL_RESOURCES = "Resource use, metals and minerals (kgSbeq)"
    EFV3_ENERGY_RESOURCES = "Energy use, energy carriers (MJ)"
    EFV3_OZONE_DEPLETION = "Ozone depletion (ODP)"
    EFV3_PARTICULATE_MATTER_FORMATION = (
        "Particulate matter formation: impact on human health (disease incidences)"
    )
    EFV3_PHOTOCHEMICAL_OZONE_FORMATION = "Photochemical ozone formation (kgNMVOCeq)"
    EFV3_WATER_USE = "Depr.-weighted water cons. (kg world eq. deprived)"

    # EFV31
    EFV31_ACIDIFICATION = "Acification (AE)"
    EFV31_CLIMATE_CHANGE = "Climate change (GWP100)"
    EFV31_CLIMATE_CHANGE_BIOGENIC = "Climate change: biogenic (GWP100)"
    EFV31_CLIMATE_CHANGE_FOSSIL = "Climate change: fossil (GWP100)"
    EFV31_CLIMATE_CHANGE_LAND_USE = "Climate change: land use/land use change (GWP100)"
    EFV31_ECOTOXICITY_FRESHWATER = "Ecotoxicity: freshwater (CTUe)"
    EFV31_ECOTOXICITY_FRESHWATER_INORGANICS = (
        "Ecotoxicity: freshwater, inorganics (CTUe)"
    )
    EFV31_ECOTOXICITY_FRESHWATER_ORGANICS = "Ecotoxicity: freshwater, organics (CTUe)"
    EFV31_EUTROPHICATION_FRESHWATER = "Eutrophication: freshwater (kgPeq)"
    EFV31_EUTROPHICATION_MARINE = "Eutrophication: marine (N)"
    EFV31_EUTROPHICATION_TERRESTRIAL = "Eutrophication: terrestrial (AE)"
    EFV31_HUMAN_TOXICITY_CARCINOGENIC = "Human toxicity: carcinogenic (CTUh)"
    EFV31_HUMAN_TOXICITY_CARCINOGENIC_INORGANICS = (
        "Human toxicity: carcinogenic, inorganics (CTUh)"
    )
    EFV31_HUMAN_TOXICITY_CARCINOGENIC_ORGANICS = (
        "Human toxicity: carcinogenic, organics (CTUh)"
    )
    EFV31_HUMAN_TOXICITY_NON_CARCINOGENIC = "Human toxicity: non-carcinogenic (CTUh)"
    EFV31_HUMAN_TOXICITY_NON_CARCINOGENIC_INORGANICS = (
        "Human toxicity: non-carcinogenic, inorganics (CTUh)"
    )
    EFV31_HUMAN_TOXICITY_NON_CARCINOGENIC_ORGANICS = (
        "Human toxicity: non-carcinogenic, organics (CTUh)"
    )
    EFV31_IONISING_RADIATION = "Ionising radiation: human health (kBqU235)"
    EFV31_LAND_USE = "Land use (soil quality index)"
    EFV31_MATERIAL_RESOURCES = "Resource use, metals and minerals (kgSbeq)"
    EFV31_OZONE_DEPLETION = "Ozone depletion (ODP)"
    EFV31_ENERGY_RESOURCES = "Energy use, energy carriers (MJ)"
    EFV31_PARTICULATE_MATTER_FORMATION = (
        "Particulate matter formation: impact on human health (disease incidences)"
    )
    EFV31_PHOTOCHEMICAL_OZONE_FORMATION = "Photochemical ozone formation (kgNMVOCeq)"
    EFV31_WATER_USE = "Depr.-weighted water cons. (kg world eq. deprived)"

    def to_full_name(self) -> MethodFullName:
        """
        Convert a short impact name to its full version (as specified in Brightway).
        :return: full name version of short impact name.
        """
        return MethodFullName[self.name]


class MethodUniqueScore(str, Enum):
    """
    PEF methods to apply normalisation and weighting to scores.
    """

    EF30 = "apparun/resources/pef30/"
    EF31 = "apparun/resources/pef31/"

    def path_to_norm(self) -> str:
        return self.value + "normalisation_factor.csv"

    def path_to_weight(self) -> str:
        return self.value + "weighting_factor.csv"
