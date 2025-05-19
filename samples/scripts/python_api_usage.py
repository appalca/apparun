import os

import pandas as pd
import plotly.express as px
import plotly.io as pio

from apparun.impact_model import ImpactModel
from apparun.results import (
    ImpactModelResult,
    NodesUncertaintyResult,
    get_result,
    register_result,
)

OUTPUT_FILES_PATH = "outputs/"

# This script aims to illustrate how to use main functions of Appa Run. We will
# compute impacts, generate figures and tables, and create user-defined custom results.

impact_model = ImpactModel.from_yaml("samples/impact_models/nvidia_ai_gpu_chip.yaml")

# Get scores and scores for each node
scores = impact_model.get_scores(
    lifespan=3,
    architecture="Maxwell",
    cuda_core=[256, 512, 1024],
    energy_per_inference=[0.05, 0.06, 0.065],
)
print(scores)
nodes_scores = impact_model.get_nodes_scores(
    lifespan=3,
    architecture="Maxwell",
    cuda_core=[256, 512, 1024],
    energy_per_inference=[0.05, 0.06, 0.065],
)
print(nodes_scores)

# Generate Tree Map figures for nodes
# We can update default values
# of impact models are changed beforehand. New min and max will be automatically adapted
# using pm and pm_perc.
impact_model.parameters.update_defaults({"cuda_core": 256, "architecture": "Maxwell"})

tree_map_result = get_result("tree_map")(
    impact_model=impact_model,
    output_name="tree_map",
    pdf_save_path=os.path.join(OUTPUT_FILES_PATH, "figures/"),
    table_save_path=os.path.join(OUTPUT_FILES_PATH, "tables/"),
    html_save_path=os.path.join(OUTPUT_FILES_PATH, "figures/"),
)
tree_map_table = tree_map_result.get_table()
tree_map_result.get_figure(tree_map_table)

# Generate Sankey figures for nodes
sankey_result = get_result("sankey")(
    impact_model=impact_model,
    output_name="sankey",
    pdf_save_path=os.path.join(OUTPUT_FILES_PATH, "figures/"),
    table_save_path=os.path.join(OUTPUT_FILES_PATH, "tables/"),
    html_save_path=os.path.join(OUTPUT_FILES_PATH, "figures/"),
)
sankey_table = sankey_result.get_table()
sankey_result.get_figure(sankey_table)

# Generate Sobol figures for nodes
sobol_result = get_result("sobol")(
    impact_model=impact_model,
    n=4096,
    output_name="sobol",
    pdf_save_path=os.path.join(OUTPUT_FILES_PATH, "figures/"),
    table_save_path=os.path.join(OUTPUT_FILES_PATH, "tables/"),
    html_save_path=os.path.join(OUTPUT_FILES_PATH, "figures/"),
)
sobol_table = sobol_result.get_table()
sobol_result.get_figure(sobol_table)

# Generate uncertainty figure for nodes
uncertainty_nodes_result = get_result("nodes_uncertainty")(
    impact_model=impact_model,
    n=4096,
    output_name="uncertainty_nodes",
    pdf_save_path=os.path.join(OUTPUT_FILES_PATH, "figures/"),
    table_save_path=os.path.join(OUTPUT_FILES_PATH, "tables/"),
    html_save_path=os.path.join(OUTPUT_FILES_PATH, "figures/"),
)
uncertainty_nodes_table = uncertainty_nodes_result.get_table()
uncertainty_nodes_result.get_figure(uncertainty_nodes_table)


# New types of results can be generated in user script, without modifying Appa Run
# source code, thanks to register_result decorator.


@register_result("new_nodes_uncertainty")
class NewNodesUncertaintyResult(NodesUncertaintyResult):
    """
    Generate uncertainty for each node using Monte Carlo. Result figure as a boxplot.
    """

    def get_figure(self, table: pd.DataFrame):
        """ """
        figures = []
        for method in pd.unique(table["method"]):
            fig = px.box(table[table["method"] == method], x="score", y="node")
            pio.full_figure_for_development(fig, warn=False)
            self.save_figure(fig, name_suffix=method)
            figures.append(fig)
        return figures


# Let's compute nodes uncertainty again, with custom class.


@register_result("uncertainty")
class UncertaintyResult(ImpactModelResult):
    n: int
    """
    Generate uncertainty for each node using Monte Carlo. Result figure as a boxplot.
    """

    def get_table(self) -> pd.DataFrame:
        """ """
        lcia_score = self.impact_model.get_uncertainty_scores(n=self.n)
        lcia_score = lcia_score.to_unpivoted_df()
        lcia_score = lcia_score.rename(columns={"name": "node"})
        lcia_score["node"] = "fu"
        if self.table_save_path is not None:
            os.makedirs(self.table_save_path, exist_ok=True)
            figure_path = os.path.join(self.table_save_path, f"{self.output_name}.csv")
            lcia_score.to_csv(figure_path)
        return lcia_score

    def get_figure(self, table: pd.DataFrame):
        """ """
        figures = []
        for method in pd.unique(table["method"]):
            fig = px.box(table[table["method"] == method], x="node", y="score")
            pio.full_figure_for_development(fig, warn=False)
            self.save_figure(fig, name_suffix=method)
            figures.append(fig)
        return figures


new_nodes_uncertainty_result = get_result("new_nodes_uncertainty")(
    impact_model=impact_model,
    n=4096,
    output_name="new_uncertainty_nodes",
    pdf_save_path=os.path.join(OUTPUT_FILES_PATH, "figures/"),
    table_save_path=os.path.join(OUTPUT_FILES_PATH, "tables/"),
    html_save_path=os.path.join(OUTPUT_FILES_PATH, "figures/"),
)
new_nodes_uncertainty_table = new_nodes_uncertainty_result.get_table()
new_nodes_uncertainty_result.get_figure(new_nodes_uncertainty_table)
