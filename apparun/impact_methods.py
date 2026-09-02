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
    EFV31_ACIDIFICATION = "('EF v3.1', 'acidification', 'accumulated exceedance (AE)')"
    EFV31_CLIMATE_CHANGE = (
        "('EF v3.1', 'climate change', 'global warming potential (GWP100)')"
    )
    EFV31_CLIMATE_CHANGE_BIOGENIC = (
        "('EF v3.1', 'climate change: biogenic', 'global warming potential (GWP100)')"
    )
    EFV31_CLIMATE_CHANGE_FOSSIL = (
        "('EF v3.1', 'climate change: fossil', 'global warming potential (GWP100)')"
    )
    EFV31_CLIMATE_CHANGE_LAND_USE = "('EF v3.1', 'climate change: land use and land use change', 'global warming potential (GWP100)')"
    EFV31_ECOTOXICITY_FRESHWATER = "('EF v3.1', 'ecotoxicity: freshwater', 'comparative toxic unit for ecosystems (CTUe)')"
    EFV31_ECOTOXICITY_FRESHWATER_INORGANICS = "('EF v3.1', 'ecotoxicity: freshwater, inorganics', 'comparative toxic unit for ecosystems (CTUe)')"
    EFV31_ECOTOXICITY_FRESHWATER_ORGANICS = "('EF v3.1', 'ecotoxicity: freshwater, organics', 'comparative toxic unit for ecosystems (CTUe)')"
    EFV31_ENERGY_RESOURCES = "('EF v3.1', 'energy resources: non-renewable', 'abiotic depletion potential (ADP): fossil fuels')"
    EFV31_EUTROPHICATION_FRESHWATER = "('EF v3.1', 'eutrophication: freshwater', 'fraction of nutrients reaching freshwater end compartment (P)')"
    EFV31_EUTROPHICATION_MARINE = "('EF v3.1', 'eutrophication: marine', 'fraction of nutrients reaching marine end compartment (N)')"
    EFV31_EUTROPHICATION_TERRESTRIAL = (
        "('EF v3.1', 'eutrophication: terrestrial', 'accumulated exceedance (AE)')"
    )
    EFV31_HUMAN_TOXICITY_CARCINOGENIC = "('EF v3.1', 'human toxicity: carcinogenic', 'comparative toxic unit for human (CTUh)')"
    EFV31_HUMAN_TOXICITY_CARCINOGENIC_INORGANICS = "('EF v3.1', 'human toxicity: carcinogenic, inorganics', 'comparative toxic unit for human (CTUh)')"
    EFV31_HUMAN_TOXICITY_CARCINOGENIC_ORGANICS = "('EF v3.1', 'human toxicity: carcinogenic, organics', 'comparative toxic unit for human (CTUh)')"
    EFV31_HUMAN_TOXICITY_NON_CARCINOGENIC = "('EF v3.1', 'human toxicity: non-carcinogenic', 'comparative toxic unit for human (CTUh)')"
    EFV31_HUMAN_TOXICITY_NON_CARCINOGENIC_INORGANICS = "('EF v3.1', 'human toxicity: non-carcinogenic, inorganics', 'comparative toxic unit for human (CTUh)')"
    EFV31_HUMAN_TOXICITY_NON_CARCINOGENIC_ORGANICS = "('EF v3.1', 'human toxicity: non-carcinogenic, organics', 'comparative toxic unit for human (CTUh)')"
    EFV31_IONISING_RADIATION = "('EF v3.1', 'ionising radiation: human health', 'human exposure efficiency relative to u235')"
    EFV31_LAND_USE = "('EF v3.1', 'land use', 'soil quality index')"
    EFV31_MATERIAL_RESOURCES = "('EF v3.1', 'material resources: metals/minerals', 'abiotic depletion potential (ADP): elements (ultimate reserves)')"
    EFV31_OZONE_DEPLETION = (
        "('EF v3.1', 'ozone depletion', 'ozone depletion potential (ODP)')"
    )
    EFV31_PARTICULATE_MATTER_FORMATION = (
        "('EF v3.1', 'particulate matter formation', 'impact on human health')"
    )
    EFV31_PHOTOCHEMICAL_OZONE_FORMATION = "('EF v3.1', 'photochemical oxidant formation: human health', 'tropospheric ozone concentration increase')"
    EFV31_WATER_USE = "('EF v3.1', 'water use', 'user deprivation potential (deprivation-weighted water consumption)')"

    # IPCC 2021 - identical between ecoinvent <= 3.10 and ecoinvent >= 3.11
    IPCC2021_CC_FOSSIL_GWP100 = "('IPCC 2021', 'climate change: fossil', 'global warming potential (GWP100)')"
    IPCC2021_NO_LT_CC_FOSSIL_GWP100 = "('IPCC 2021 no LT', 'climate change: fossil no LT', 'global warming potential (GWP100) no LT')"

    # IPCC 2021 - ecoinvent-3.10 and prior
    IPCC2021_CC_GTP100_EI310_INF = "('IPCC 2021', 'climate change', 'global temperature change potential (GTP100)')"
    IPCC2021_CC_GTP50_EI310_INF = "('IPCC 2021', 'climate change', 'global temperature change potential (GTP50)')"
    IPCC2021_CC_GWP100_EI310_INF = "('IPCC 2021', 'climate change', 'global warming potential (GWP100)')"
    IPCC2021_CC_GWP20_EI310_INF = "('IPCC 2021', 'climate change', 'global warming potential (GWP20)')"
    IPCC2021_CC_GWP500_EI310_INF = "('IPCC 2021', 'climate change', 'global warming potential (GWP500)')"
    IPCC2021_CC_BIOGENIC_GTP100_EI310_INF = "('IPCC 2021', 'climate change: biogenic', 'global temperature change potential (GTP100)')"
    IPCC2021_CC_BIOGENIC_GTP50_EI310_INF = "('IPCC 2021', 'climate change: biogenic', 'global temperature change potential (GTP50)')"
    IPCC2021_CC_BIOGENIC_GWP100_EI310_INF = "('IPCC 2021', 'climate change: biogenic', 'global warming potential (GWP100)')"
    IPCC2021_CC_BIOGENIC_GWP20_EI310_INF = "('IPCC 2021', 'climate change: biogenic', 'global warming potential (GWP20)')"
    IPCC2021_CC_BIOGENIC_GWP500_EI310_INF = "('IPCC 2021', 'climate change: biogenic', 'global warming potential (GWP500)')"
    IPCC2021_CC_BIOGENIC_INCL_SLCFS_GTP100_EI310_INF = "('IPCC 2021', 'climate change: biogenic, including SLCFs', 'global temperature change potential (GTP100)')"
    IPCC2021_CC_BIOGENIC_INCL_SLCFS_GWP100_EI310_INF = "('IPCC 2021', 'climate change: biogenic, including SLCFs', 'global warming potential (GWP100)')"
    IPCC2021_CC_BIOGENIC_INCL_SLCFS_GWP20_EI310_INF = "('IPCC 2021', 'climate change: biogenic, including SLCFs', 'global warming potential (GWP20)')"
    IPCC2021_CC_FOSSIL_GTP100_EI310_INF = "('IPCC 2021', 'climate change: fossil', 'global temperature change potential (GTP100)')"
    IPCC2021_CC_FOSSIL_GTP50_EI310_INF = "('IPCC 2021', 'climate change: fossil', 'global temperature change potential (GTP50)')"
    IPCC2021_CC_FOSSIL_GWP20_EI310_INF = "('IPCC 2021', 'climate change: fossil', 'global warming potential (GWP20)')"
    IPCC2021_CC_FOSSIL_GWP500_EI310_INF = "('IPCC 2021', 'climate change: fossil', 'global warming potential (GWP500)')"
    IPCC2021_CC_FOSSIL_INCL_SLCFS_GTP100_EI310_INF = "('IPCC 2021', 'climate change: fossil, including SLCFs', 'global temperature change potential (GTP100)')"
    IPCC2021_CC_FOSSIL_INCL_SLCFS_GWP100_EI310_INF = "('IPCC 2021', 'climate change: fossil, including SLCFs', 'global warming potential (GWP100)')"
    IPCC2021_CC_FOSSIL_INCL_SLCFS_GWP20_EI310_INF = "('IPCC 2021', 'climate change: fossil, including SLCFs', 'global warming potential (GWP20)')"
    IPCC2021_CC_INCL_SLCFS_GTP100_EI310_INF = "('IPCC 2021', 'climate change: including SLCFs', 'global temperature change potential (GTP100)')"
    IPCC2021_CC_INCL_SLCFS_GWP100_EI310_INF = "('IPCC 2021', 'climate change: including SLCFs', 'global warming potential (GWP100)')"
    IPCC2021_CC_INCL_SLCFS_GWP20_EI310_INF = "('IPCC 2021', 'climate change: including SLCFs', 'global warming potential (GWP20)')"
    IPCC2021_CC_LU_GTP100_EI310_INF = "('IPCC 2021', 'climate change: land use', 'global temperature change potential (GTP100)')"
    IPCC2021_CC_LU_GTP50_EI310_INF = "('IPCC 2021', 'climate change: land use', 'global temperature change potential (GTP50)')"
    IPCC2021_CC_LU_GWP100_EI310_INF = "('IPCC 2021', 'climate change: land use', 'global warming potential (GWP100)')"
    IPCC2021_CC_LU_GWP20_EI310_INF = "('IPCC 2021', 'climate change: land use', 'global warming potential (GWP20)')"
    IPCC2021_CC_LU_GWP500_EI310_INF = "('IPCC 2021', 'climate change: land use', 'global warming potential (GWP500)')"
    IPCC2021_CC_LU_INCL_SLCFS_GTP100_EI310_INF = "('IPCC 2021', 'climate change: land use, including SLCFs', 'global temperature change potential (GTP100)')"
    IPCC2021_CC_LU_INCL_SLCFS_GWP100_EI310_INF = "('IPCC 2021', 'climate change: land use, including SLCFs', 'global warming potential (GWP100)')"
    IPCC2021_CC_LU_INCL_SLCFS_GWP20_EI310_INF = "('IPCC 2021', 'climate change: land use, including SLCFs', 'global warming potential (GWP20)')"
    IPCC2021_NO_LT_CC_GTP100_EI310_INF = "('IPCC 2021 no LT', 'climate change no LT', 'global temperature change potential (GTP100) no LT')"
    IPCC2021_NO_LT_CC_GTP50_EI310_INF = "('IPCC 2021 no LT', 'climate change no LT', 'global temperature change potential (GTP50) no LT')"
    IPCC2021_NO_LT_CC_GWP100_EI310_INF = "('IPCC 2021 no LT', 'climate change no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_GWP20_EI310_INF = "('IPCC 2021 no LT', 'climate change no LT', 'global warming potential (GWP20) no LT')"
    IPCC2021_NO_LT_CC_GWP500_EI310_INF = "('IPCC 2021 no LT', 'climate change no LT', 'global warming potential (GWP500) no LT')"
    IPCC2021_NO_LT_CC_BIOGENIC_GTP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: biogenic no LT', 'global temperature change potential (GTP100) no LT')"
    IPCC2021_NO_LT_CC_BIOGENIC_GTP50_EI310_INF = "('IPCC 2021 no LT', 'climate change: biogenic no LT', 'global temperature change potential (GTP50) no LT')"
    IPCC2021_NO_LT_CC_BIOGENIC_GWP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: biogenic no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_BIOGENIC_GWP20_EI310_INF = "('IPCC 2021 no LT', 'climate change: biogenic no LT', 'global warming potential (GWP20) no LT')"
    IPCC2021_NO_LT_CC_BIOGENIC_GWP500_EI310_INF = "('IPCC 2021 no LT', 'climate change: biogenic no LT', 'global warming potential (GWP500) no LT')"
    IPCC2021_NO_LT_CC_BIOGENIC_INCL_SLCFS_GTP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: biogenic, including SLCFs no LT', 'global temperature change potential (GTP100) no LT')"
    IPCC2021_NO_LT_CC_BIOGENIC_INCL_SLCFS_GWP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: biogenic, including SLCFs no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_BIOGENIC_INCL_SLCFS_GWP20_EI310_INF = "('IPCC 2021 no LT', 'climate change: biogenic, including SLCFs no LT', 'global warming potential (GWP20) no LT')"
    IPCC2021_NO_LT_CC_FOSSIL_GTP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: fossil no LT', 'global temperature change potential (GTP100) no LT')"
    IPCC2021_NO_LT_CC_FOSSIL_GTP50_EI310_INF = "('IPCC 2021 no LT', 'climate change: fossil no LT', 'global temperature change potential (GTP50) no LT')"
    IPCC2021_NO_LT_CC_FOSSIL_GWP20_EI310_INF = "('IPCC 2021 no LT', 'climate change: fossil no LT', 'global warming potential (GWP20) no LT')"
    IPCC2021_NO_LT_CC_FOSSIL_GWP500_EI310_INF = "('IPCC 2021 no LT', 'climate change: fossil no LT', 'global warming potential (GWP500) no LT')"
    IPCC2021_NO_LT_CC_FOSSIL_INCL_SLCFS_GTP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: fossil, including SLCFs no LT', 'global temperature change potential (GTP100) no LT')"
    IPCC2021_NO_LT_CC_FOSSIL_INCL_SLCFS_GWP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: fossil, including SLCFs no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_FOSSIL_INCL_SLCFS_GWP20_EI310_INF = "('IPCC 2021 no LT', 'climate change: fossil, including SLCFs no LT', 'global warming potential (GWP20) no LT')"
    IPCC2021_NO_LT_CC_INCL_SLCFS_GTP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: including SLCFs no LT', 'global temperature change potential (GTP100) no LT')"
    IPCC2021_NO_LT_CC_INCL_SLCFS_GWP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: including SLCFs no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_INCL_SLCFS_GWP20_EI310_INF = "('IPCC 2021 no LT', 'climate change: including SLCFs no LT', 'global warming potential (GWP20) no LT')"
    IPCC2021_NO_LT_CC_LU_GTP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: land use no LT', 'global temperature change potential (GTP100) no LT')"
    IPCC2021_NO_LT_CC_LU_GTP50_EI310_INF = "('IPCC 2021 no LT', 'climate change: land use no LT', 'global temperature change potential (GTP50) no LT')"
    IPCC2021_NO_LT_CC_LU_GWP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: land use no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_LU_GWP20_EI310_INF = "('IPCC 2021 no LT', 'climate change: land use no LT', 'global warming potential (GWP20) no LT')"
    IPCC2021_NO_LT_CC_LU_GWP500_EI310_INF = "('IPCC 2021 no LT', 'climate change: land use no LT', 'global warming potential (GWP500) no LT')"
    IPCC2021_NO_LT_CC_LU_INCL_SLCFS_GTP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: land use, including SLCFs no LT', 'global temperature change potential (GTP100) no LT')"
    IPCC2021_NO_LT_CC_LU_INCL_SLCFS_GWP100_EI310_INF = "('IPCC 2021 no LT', 'climate change: land use, including SLCFs no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_LU_INCL_SLCFS_GWP20_EI310_INF = "('IPCC 2021 no LT', 'climate change: land use, including SLCFs no LT', 'global warming potential (GWP20) no LT')"

    # IPCC 2021 - ecoinvent-3.11 and later
    IPCC2021_CC_AIRCRAFT_EMISSIONS_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: aircraft emissions', 'global warming potential (GWP100)')"
    IPCC2021_CC_BIOGENIC_EXCL_CO2_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: biogenic (excl. CO2)', 'global warming potential (GWP100)')"
    IPCC2021_CC_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: direct land use change', 'global warming potential (GWP100)')"
    IPCC2021_CC_EMISSIONS_FROM_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: emissions from direct land use change', 'global warming potential (GWP100)')"
    IPCC2021_CC_FOSSIL_EMISSIONS_EXCL_AIRCRAFT_EMISSIONS_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: fossil emissions (excl. aircraft emissions)', 'global warming potential (GWP100)')"
    IPCC2021_CC_REMOVALS_FROM_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: removals from direct land use change', 'global warming potential (GWP100)')"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP500_EI311_SUP = "('IPCC 2021', 'climate change: total (excl. biogenic CO2)', 'global warming potential (GWP500)')"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP20_EI311_SUP = "('IPCC 2021', 'climate change: total (excl. biogenic CO2)', 'global warming potential (GWP20)')"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: total (excl. biogenic CO2)', 'global warming potential (GWP100)')"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_GTP50_EI311_SUP = "('IPCC 2021', 'climate change: total (excl. biogenic CO2)', 'global temperature change potential (GTP50)')"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_GTP100_EI311_SUP = "('IPCC 2021', 'climate change: total (excl. biogenic CO2)', 'global temperature change potential (GTP100)')"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: total (excl. biogenic CO2, incl. SLCFs)', 'global warming potential (GWP100)')"
    IPCC2021_CC_BIOGENIC_EXCL_CO2_INCL_SLCFS_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: biogenic (excl. CO2, incl. SLCFs)', 'global warming potential (GWP100)')"
    IPCC2021_CC_FOSSIL_EXCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: fossil (excl. biogenic CO2, incl. SLCFs)', 'global warming potential (GWP100)')"
    IPCC2021_CC_DIRECT_LU_CHANGE_INCL_SLCFS_GWP100_EI311_SUP = "('IPCC 2021', 'climate change: direct land use change (incl. SLCFs)', 'global warming potential (GWP100)')"
    IPCC2021_NO_LT_CC_BIOGENIC_EXCL_CO2_GWP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: biogenic (excl. CO2) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: direct land use change no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_EMISSIONS_FROM_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: emissions from direct land use change no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_FOSSIL_EMISSIONS_EXCL_AIRCRAFT_EMISSIONS_GWP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: fossil emissions (excl. aircraft emissions) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_REMOVALS_FROM_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: removals from direct land use change no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP500_EI311_SUP = "('IPCC 2021 no LT', 'climate change: total (excl. biogenic CO2) no LT', 'global warming potential (GWP500) no LT')"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP20_EI311_SUP = "('IPCC 2021 no LT', 'climate change: total (excl. biogenic CO2) no LT', 'global warming potential (GWP20) no LT')"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: total (excl. biogenic CO2) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_GTP50_EI311_SUP = "('IPCC 2021 no LT', 'climate change: total (excl. biogenic CO2) no LT', 'global temperature change potential (GTP50) no LT')"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_GTP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: total (excl. biogenic CO2) no LT', 'global temperature change potential (GTP100) no LT')"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: total (excl. biogenic CO2, incl. SLCFs) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_BIOGENIC_EXCL_CO2_INCL_SLCFS_GWP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: biogenic (excl. CO2, incl. SLCFs) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_FOSSIL_EXCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: fossil (excl. biogenic CO2, incl. SLCFs) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_NO_LT_CC_DIRECT_LU_CHANGE_INCL_SLCFS_GWP100_EI311_SUP = "('IPCC 2021 no LT', 'climate change: direct land use change (incl. SLCFs) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_INCL_BIOGENIC_CO2_CC_BIOGENIC_INCL_CO2_GWP100_EI311_SUP = "('IPCC 2021 (incl. biogenic CO2)', 'climate change: biogenic (incl. CO2)', 'global warming potential (GWP100)')"
    IPCC2021_INCL_BIOGENIC_CO2_CC_BIOGENIC_EMISSIONS_INCL_CO2_GWP100_EI311_SUP = "('IPCC 2021 (incl. biogenic CO2)', 'climate change: biogenic emissions (incl. CO2)', 'global warming potential (GWP100)')"
    IPCC2021_INCL_BIOGENIC_CO2_CC_BIOGENIC_REMOVALS_INCL_CO2_GWP100_EI311_SUP = "('IPCC 2021 (incl. biogenic CO2)', 'climate change: biogenic removals (incl. CO2)', 'global warming potential (GWP100)')"
    IPCC2021_INCL_BIOGENIC_CO2_CC_TOTAL_INCL_BIOGENIC_CO2_GWP100_EI311_SUP = "('IPCC 2021 (incl. biogenic CO2)', 'climate change: total (incl. biogenic CO2)', 'global warming potential (GWP100)')"
    IPCC2021_INCL_BIOGENIC_CO2_CC_TOTAL_INCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "('IPCC 2021 (incl. biogenic CO2)', 'climate change: total (incl. biogenic CO2, incl. SLCFs)', 'global warming potential (GWP100)')"
    IPCC2021_INCL_BIOGENIC_CO2_NO_LT_CC_BIOGENIC_INCL_CO2_GWP100_EI311_SUP = "('IPCC 2021 (incl. biogenic CO2) no LT', 'climate change: biogenic (incl. CO2) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_INCL_BIOGENIC_CO2_NO_LT_CC_BIOGENIC_EMISSIONS_INCL_CO2_GWP100_EI311_SUP = "('IPCC 2021 (incl. biogenic CO2) no LT', 'climate change: biogenic emissions (incl. CO2) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_INCL_BIOGENIC_CO2_NO_LT_CC_BIOGENIC_REMOVALS_INCL_CO2_GWP100_EI311_SUP = "('IPCC 2021 (incl. biogenic CO2) no LT', 'climate change: biogenic removals (incl. CO2) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_INCL_BIOGENIC_CO2_NO_LT_CC_TOTAL_INCL_BIOGENIC_CO2_GWP100_EI311_SUP = "('IPCC 2021 (incl. biogenic CO2) no LT', 'climate change: total (incl. biogenic CO2) no LT', 'global warming potential (GWP100) no LT')"
    IPCC2021_INCL_BIOGENIC_CO2_NO_LT_CC_TOTAL_INCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "('IPCC 2021 (incl. biogenic CO2) no LT', 'climate change: total (incl. biogenic CO2, incl. SLCFs) no LT', 'global warming potential (GWP100) no LT')"

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
    EFV3_ACIDIFICATION = "Acidification (AE)"
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
    EFV31_ACIDIFICATION = "Acidification (AE)"
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

    # IPCC 2021 - identical between ecoinvent <= 3.10 and ecoinvent >= 3.11
    IPCC2021_CC_FOSSIL_GWP100 = "Climate change: fossil (GWP100)"
    IPCC2021_NO_LT_CC_FOSSIL_GWP100 = "Climate change: fossil (GWP100) no LT"

    # IPCC 2021 - ecoinvent-3.10 and prior
    IPCC2021_CC_GTP100_EI310_INF = "Climate change (GTP100)"
    IPCC2021_CC_GTP50_EI310_INF = "Climate change (GTP50)"
    IPCC2021_CC_GWP100_EI310_INF = "Climate change (GWP100)"
    IPCC2021_CC_GWP20_EI310_INF = "Climate change (GWP20)"
    IPCC2021_CC_GWP500_EI310_INF = "Climate change (GWP500)"
    IPCC2021_CC_BIOGENIC_GTP100_EI310_INF = "Climate change: biogenic (GTP100)"
    IPCC2021_CC_BIOGENIC_GTP50_EI310_INF = "Climate change: biogenic (GTP50)"
    IPCC2021_CC_BIOGENIC_GWP100_EI310_INF = "Climate change: biogenic (GWP100)"
    IPCC2021_CC_BIOGENIC_GWP20_EI310_INF = "Climate change: biogenic (GWP20)"
    IPCC2021_CC_BIOGENIC_GWP500_EI310_INF = "Climate change: biogenic (GWP500)"
    IPCC2021_CC_BIOGENIC_INCL_SLCFS_GTP100_EI310_INF = "Climate change: biogenic, including SLCFs (GTP100)"
    IPCC2021_CC_BIOGENIC_INCL_SLCFS_GWP100_EI310_INF = "Climate change: biogenic, including SLCFs (GWP100)"
    IPCC2021_CC_BIOGENIC_INCL_SLCFS_GWP20_EI310_INF = "Climate change: biogenic, including SLCFs (GWP20)"
    IPCC2021_CC_FOSSIL_GTP100_EI310_INF = "Climate change: fossil (GTP100)"
    IPCC2021_CC_FOSSIL_GTP50_EI310_INF = "Climate change: fossil (GTP50)"
    IPCC2021_CC_FOSSIL_GWP20_EI310_INF = "Climate change: fossil (GWP20)"
    IPCC2021_CC_FOSSIL_GWP500_EI310_INF = "Climate change: fossil (GWP500)"
    IPCC2021_CC_FOSSIL_INCL_SLCFS_GTP100_EI310_INF = "Climate change: fossil, including SLCFs (GTP100)"
    IPCC2021_CC_FOSSIL_INCL_SLCFS_GWP100_EI310_INF = "Climate change: fossil, including SLCFs (GWP100)"
    IPCC2021_CC_FOSSIL_INCL_SLCFS_GWP20_EI310_INF = "Climate change: fossil, including SLCFs (GWP20)"
    IPCC2021_CC_INCL_SLCFS_GTP100_EI310_INF = "Climate change: including SLCFs (GTP100)"
    IPCC2021_CC_INCL_SLCFS_GWP100_EI310_INF = "Climate change: including SLCFs (GWP100)"
    IPCC2021_CC_INCL_SLCFS_GWP20_EI310_INF = "Climate change: including SLCFs (GWP20)"
    IPCC2021_CC_LU_GTP100_EI310_INF = "Climate change: land use (GTP100)"
    IPCC2021_CC_LU_GTP50_EI310_INF = "Climate change: land use (GTP50)"
    IPCC2021_CC_LU_GWP100_EI310_INF = "Climate change: land use (GWP100)"
    IPCC2021_CC_LU_GWP20_EI310_INF = "Climate change: land use (GWP20)"
    IPCC2021_CC_LU_GWP500_EI310_INF = "Climate change: land use (GWP500)"
    IPCC2021_CC_LU_INCL_SLCFS_GTP100_EI310_INF = "Climate change: land use, including SLCFs (GTP100)"
    IPCC2021_CC_LU_INCL_SLCFS_GWP100_EI310_INF = "Climate change: land use, including SLCFs (GWP100)"
    IPCC2021_CC_LU_INCL_SLCFS_GWP20_EI310_INF = "Climate change: land use, including SLCFs (GWP20)"
    IPCC2021_NO_LT_CC_GTP100_EI310_INF = "Climate change (GTP100) no LT"
    IPCC2021_NO_LT_CC_GTP50_EI310_INF = "Climate change (GTP50) no LT"
    IPCC2021_NO_LT_CC_GWP100_EI310_INF = "Climate change (GWP100) no LT"
    IPCC2021_NO_LT_CC_GWP20_EI310_INF = "Climate change (GWP20) no LT"
    IPCC2021_NO_LT_CC_GWP500_EI310_INF = "Climate change (GWP500) no LT"
    IPCC2021_NO_LT_CC_BIOGENIC_GTP100_EI310_INF = "Climate change: biogenic (GTP100) no LT"
    IPCC2021_NO_LT_CC_BIOGENIC_GTP50_EI310_INF = "Climate change: biogenic (GTP50) no LT"
    IPCC2021_NO_LT_CC_BIOGENIC_GWP100_EI310_INF = "Climate change: biogenic (GWP100) no LT"
    IPCC2021_NO_LT_CC_BIOGENIC_GWP20_EI310_INF = "Climate change: biogenic (GWP20) no LT"
    IPCC2021_NO_LT_CC_BIOGENIC_GWP500_EI310_INF = "Climate change: biogenic (GWP500) no LT"
    IPCC2021_NO_LT_CC_BIOGENIC_INCL_SLCFS_GTP100_EI310_INF = "Climate change: biogenic, including SLCFs (GTP100) no LT"
    IPCC2021_NO_LT_CC_BIOGENIC_INCL_SLCFS_GWP100_EI310_INF = "Climate change: biogenic, including SLCFs (GWP100) no LT"
    IPCC2021_NO_LT_CC_BIOGENIC_INCL_SLCFS_GWP20_EI310_INF = "Climate change: biogenic, including SLCFs (GWP20) no LT"
    IPCC2021_NO_LT_CC_FOSSIL_GTP100_EI310_INF = "Climate change: fossil (GTP100) no LT"
    IPCC2021_NO_LT_CC_FOSSIL_GTP50_EI310_INF = "Climate change: fossil (GTP50) no LT"
    IPCC2021_NO_LT_CC_FOSSIL_GWP20_EI310_INF = "Climate change: fossil (GWP20) no LT"
    IPCC2021_NO_LT_CC_FOSSIL_GWP500_EI310_INF = "Climate change: fossil (GWP500) no LT"
    IPCC2021_NO_LT_CC_FOSSIL_INCL_SLCFS_GTP100_EI310_INF = "Climate change: fossil, including SLCFs (GTP100) no LT"
    IPCC2021_NO_LT_CC_FOSSIL_INCL_SLCFS_GWP100_EI310_INF = "Climate change: fossil, including SLCFs (GWP100) no LT"
    IPCC2021_NO_LT_CC_FOSSIL_INCL_SLCFS_GWP20_EI310_INF = "Climate change: fossil, including SLCFs (GWP20) no LT"
    IPCC2021_NO_LT_CC_INCL_SLCFS_GTP100_EI310_INF = "Climate change: including SLCFs (GTP100) no LT"
    IPCC2021_NO_LT_CC_INCL_SLCFS_GWP100_EI310_INF = "Climate change: including SLCFs (GWP100) no LT"
    IPCC2021_NO_LT_CC_INCL_SLCFS_GWP20_EI310_INF = "Climate change: including SLCFs (GWP20) no LT"
    IPCC2021_NO_LT_CC_LU_GTP100_EI310_INF = "Climate change: land use (GTP100) no LT"
    IPCC2021_NO_LT_CC_LU_GTP50_EI310_INF = "Climate change: land use (GTP50) no LT"
    IPCC2021_NO_LT_CC_LU_GWP100_EI310_INF = "Climate change: land use (GWP100) no LT"
    IPCC2021_NO_LT_CC_LU_GWP20_EI310_INF = "Climate change: land use (GWP20) no LT"
    IPCC2021_NO_LT_CC_LU_GWP500_EI310_INF = "Climate change: land use (GWP500) no LT"
    IPCC2021_NO_LT_CC_LU_INCL_SLCFS_GTP100_EI310_INF = "Climate change: land use, including SLCFs (GTP100) no LT"
    IPCC2021_NO_LT_CC_LU_INCL_SLCFS_GWP100_EI310_INF = "Climate change: land use, including SLCFs (GWP100) no LT"
    IPCC2021_NO_LT_CC_LU_INCL_SLCFS_GWP20_EI310_INF = "Climate change: land use, including SLCFs (GWP20) no LT"

    # IPCC 2021 - ecoinvent-3.11 and later
    IPCC2021_CC_AIRCRAFT_EMISSIONS_GWP100_EI311_SUP = "Climate change: aircraft emissions (GWP100)"
    IPCC2021_CC_BIOGENIC_EXCL_CO2_GWP100_EI311_SUP = "Climate change: biogenic (excl. CO2) (GWP100)"
    IPCC2021_CC_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "Climate change: direct land use change (GWP100)"
    IPCC2021_CC_EMISSIONS_FROM_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "Climate change: emissions from direct land use change (GWP100)"
    IPCC2021_CC_FOSSIL_EMISSIONS_EXCL_AIRCRAFT_EMISSIONS_GWP100_EI311_SUP = "Climate change: fossil emissions (excl. aircraft emissions) (GWP100)"
    IPCC2021_CC_REMOVALS_FROM_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "Climate change: removals from direct land use change (GWP100)"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP500_EI311_SUP = "Climate change: total (excl. biogenic CO2) (GWP500)"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP20_EI311_SUP = "Climate change: total (excl. biogenic CO2) (GWP20)"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP100_EI311_SUP = "Climate change: total (excl. biogenic CO2) (GWP100)"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_GTP50_EI311_SUP = "Climate change: total (excl. biogenic CO2) (GTP50)"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_GTP100_EI311_SUP = "Climate change: total (excl. biogenic CO2) (GTP100)"
    IPCC2021_CC_TOTAL_EXCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "Climate change: total (excl. biogenic CO2, incl. SLCFs) (GWP100)"
    IPCC2021_CC_BIOGENIC_EXCL_CO2_INCL_SLCFS_GWP100_EI311_SUP = "Climate change: biogenic (excl. CO2, incl. SLCFs) (GWP100)"
    IPCC2021_CC_FOSSIL_EXCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "Climate change: fossil (excl. biogenic CO2, incl. SLCFs) (GWP100)"
    IPCC2021_CC_DIRECT_LU_CHANGE_INCL_SLCFS_GWP100_EI311_SUP = "Climate change: direct land use change (incl. SLCFs) (GWP100)"
    IPCC2021_NO_LT_CC_BIOGENIC_EXCL_CO2_GWP100_EI311_SUP = "Climate change: biogenic (excl. CO2) (GWP100) no LT"
    IPCC2021_NO_LT_CC_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "Climate change: direct land use change (GWP100) no LT"
    IPCC2021_NO_LT_CC_EMISSIONS_FROM_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "Climate change: emissions from direct land use change (GWP100) no LT"
    IPCC2021_NO_LT_CC_FOSSIL_EMISSIONS_EXCL_AIRCRAFT_EMISSIONS_GWP100_EI311_SUP = "Climate change: fossil emissions (excl. aircraft emissions) (GWP100) no LT"
    IPCC2021_NO_LT_CC_REMOVALS_FROM_DIRECT_LU_CHANGE_GWP100_EI311_SUP = "Climate change: removals from direct land use change (GWP100) no LT"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP500_EI311_SUP = "Climate change: total (excl. biogenic CO2) (GWP500) no LT"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP20_EI311_SUP = "Climate change: total (excl. biogenic CO2) (GWP20) no LT"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_GWP100_EI311_SUP = "Climate change: total (excl. biogenic CO2) (GWP100) no LT"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_GTP50_EI311_SUP = "Climate change: total (excl. biogenic CO2) (GTP50) no LT"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_GTP100_EI311_SUP = "Climate change: total (excl. biogenic CO2) (GTP100) no LT"
    IPCC2021_NO_LT_CC_TOTAL_EXCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "Climate change: total (excl. biogenic CO2, incl. SLCFs) (GWP100) no LT"
    IPCC2021_NO_LT_CC_BIOGENIC_EXCL_CO2_INCL_SLCFS_GWP100_EI311_SUP = "Climate change: biogenic (excl. CO2, incl. SLCFs) (GWP100) no LT"
    IPCC2021_NO_LT_CC_FOSSIL_EXCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "Climate change: fossil (excl. biogenic CO2, incl. SLCFs) (GWP100) no LT"
    IPCC2021_NO_LT_CC_DIRECT_LU_CHANGE_INCL_SLCFS_GWP100_EI311_SUP = "Climate change: direct land use change (incl. SLCFs) (GWP100) no LT"
    IPCC2021_INCL_BIOGENIC_CO2_CC_BIOGENIC_INCL_CO2_GWP100_EI311_SUP = "Climate change: biogenic (incl. CO2) (GWP100)"
    IPCC2021_INCL_BIOGENIC_CO2_CC_BIOGENIC_EMISSIONS_INCL_CO2_GWP100_EI311_SUP = "Climate change: biogenic emissions (incl. CO2) (GWP100)"
    IPCC2021_INCL_BIOGENIC_CO2_CC_BIOGENIC_REMOVALS_INCL_CO2_GWP100_EI311_SUP = "Climate change: biogenic removals (incl. CO2) (GWP100)"
    IPCC2021_INCL_BIOGENIC_CO2_CC_TOTAL_INCL_BIOGENIC_CO2_GWP100_EI311_SUP = "Climate change: total (incl. biogenic CO2) (GWP100)"
    IPCC2021_INCL_BIOGENIC_CO2_CC_TOTAL_INCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "Climate change: total (incl. biogenic CO2, incl. SLCFs) (GWP100)"
    IPCC2021_INCL_BIOGENIC_CO2_NO_LT_CC_BIOGENIC_INCL_CO2_GWP100_EI311_SUP = "Climate change: biogenic (incl. CO2) (GWP100) no LT"
    IPCC2021_INCL_BIOGENIC_CO2_NO_LT_CC_BIOGENIC_EMISSIONS_INCL_CO2_GWP100_EI311_SUP = "Climate change: biogenic emissions (incl. CO2) (GWP100) no LT"
    IPCC2021_INCL_BIOGENIC_CO2_NO_LT_CC_BIOGENIC_REMOVALS_INCL_CO2_GWP100_EI311_SUP = "Climate change: biogenic removals (incl. CO2) (GWP100) no LT"
    IPCC2021_INCL_BIOGENIC_CO2_NO_LT_CC_TOTAL_INCL_BIOGENIC_CO2_GWP100_EI311_SUP = "Climate change: total (incl. biogenic CO2) (GWP100) no LT"
    IPCC2021_INCL_BIOGENIC_CO2_NO_LT_CC_TOTAL_INCL_BIOGENIC_CO2_INCL_SLCFS_GWP100_EI311_SUP = "Climate change: total (incl. biogenic CO2, incl. SLCFs) (GWP100) no LT"

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
