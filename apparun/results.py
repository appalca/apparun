from __future__ import annotations

import os
from typing import List, Optional, Union

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pydantic import BaseModel

from apparun.impact_model import ImpactModel

RESULTS = {}


def register_result(result_name):
    """
    This decorator registers a new ImpactModelResult class in RESULTS registry.
    :param result_name: name of the new result to register
    :return: new ImpactModelResult class
    """

    def decorator(decorated_class):
        if result_name not in RESULTS:
            RESULTS[result_name] = decorated_class
        return decorated_class

    return decorator


def get_result(result_name: str):
    """
    Get a registered ImpactModelResult class by name.
    :param result_name: registered name of the desired ImpactModelResult.
    :return: registered ImpactModelResult class corresponding to the name.
    """
    return RESULTS[result_name]


def registered_results() -> List[str]:
    """
    Get a list of registered ImpactModelResult names.
    :return: list of registered ImpactModelResult names.
    """
    return list(RESULTS.keys())


class ImpactModelResult(BaseModel):
    """
    An impact model result is one, or a collection of tables and/or figures generated
    by executing an impact model.
    """

    output_name: str
    impact_model: ImpactModel
    html_save_path: Optional[str] = None
    pdf_save_path: Optional[str] = None
    png_save_path: Optional[str] = None
    table_save_path: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

    def run(self):
        """
        Execute the result to generate wanted outputs.
        """
        table = self.get_table()
        self.get_figure(table)

    def get_table(self) -> Union[pd.DataFrame, pd.Series]:
        """
        Abstract method.
        Generate the output as a table, or a collection of tables.
        :return: tabular results as a pandas DataFrame.
        """
        return pd.DataFrame()

    def get_figure(self, table: pd.DataFrame):
        """
        Abstract method.
        Generate the output as a figures, or a collection of figures, using the output
        of the get_table method.
        :param table: tabular result data.
        :return: figure, or collection of figure generated.
        """
        return None

    def save_figure(self, fig, name_suffix=None):
        """
        Save a figure to disk, according to the configuration specified in result
        attributes.
        :param fig: figure to save
        :param name_suffix: optional file name suffix.
        """
        filename = (
            self.output_name + "-" + name_suffix
            if name_suffix is not None
            else self.output_name
        )
        if self.html_save_path is not None:
            os.makedirs(self.html_save_path, exist_ok=True)
            figure_path = os.path.join(self.html_save_path, f"{filename}.html")
            fig.write_html(figure_path)
        if self.pdf_save_path is not None:
            os.makedirs(self.pdf_save_path, exist_ok=True)
            figure_path = os.path.join(self.pdf_save_path, f"{filename}.pdf")
            fig.write_image(figure_path, width=self.width, height=self.height)
        if self.png_save_path is not None:
            os.makedirs(self.png_save_path, exist_ok=True)
            figure_path = os.path.join(self.png_save_path, f"{filename}.png")
            fig.write_image(figure_path, width=self.width, height=self.height)


@register_result("tree_map")
class TreeMapResult(ImpactModelResult):
    """
    Generate a TreeMap for each impact, representing the contribution of all nodes to
    the root node result.
    See https://plotly.com/python/treemaps/ for more information.
    """

    parameters: Optional[dict[str, Union[float, str]]] = {}

    def get_table(self) -> pd.DataFrame:
        """
        Generate treemap output as a table, or a collection of tables.
        Save it to disk according to configuration specified in result attributes.
        :return: tabular results as a pandas DataFrame.
        """
        node_scores = self.impact_model.get_nodes_scores(**self.parameters)
        node_scores = [node_score.to_unpivoted_df() for node_score in node_scores]
        node_scores = pd.concat(node_scores)
        if self.table_save_path is not None:
            os.makedirs(self.table_save_path, exist_ok=True)
            figure_path = os.path.join(self.table_save_path, f"{self.output_name}.csv")
            node_scores.to_csv(figure_path)
        return node_scores

    def get_figure(self, table: pd.DataFrame):
        """
        Generate one distinct treemap per impact method.
        Save figure(s) to disk, according to the configuration specified in result
        attributes.
        :param table: tabular treemap result data.
        :return: figure, or collection of figure generated.
        """
        figs = []
        for method_name in pd.unique(table["method"]):
            method_data = table[table["method"] == method_name]
            fig = go.Figure(
                go.Treemap(
                    labels=method_data["name"].values,
                    parents=method_data["parent"].values,
                    values=method_data["score"].values,
                    branchvalues="total",
                    root_color="lightgrey",
                )
            )
            self.save_figure(fig, name_suffix=method_name)
            figs.append(fig)
        return figs


@register_result("sankey")
class SankeyDiagramResult(ImpactModelResult):
    """
    Generate a Sankey diagram for each impact, representing the contribution of all
    nodes to the root node result.
    See https://plotly.com/python/sankey-diagram/ for more information.
    """

    parameters: Optional[dict[str, Union[float, str]]] = {}

    def get_table(self) -> pd.DataFrame:
        """
        Generate Sankey output as a table, or a collection of tables.
        Save it to disk according to configuration specified in result attributes.
        :return: tabular results as a pandas DataFrame.
        """
        node_scores = self.impact_model.get_nodes_scores(**self.parameters)
        node_scores = [node_score.to_unpivoted_df() for node_score in node_scores]
        node_scores = pd.concat(node_scores)
        if self.table_save_path is not None:
            os.makedirs(self.table_save_path, exist_ok=True)
            figure_path = os.path.join(self.table_save_path, f"{self.output_name}.csv")
            node_scores.to_csv(figure_path)
        names_to_indices = {
            node_scores["name"].unique()[i]: i
            for i in range(node_scores["name"].unique().shape[0])
        }
        node_scores["source"] = node_scores["name"]
        node_scores = node_scores.replace(
            {"source": names_to_indices, "parent": names_to_indices}
        )
        return node_scores

    def get_figure(self, table: pd.DataFrame) -> List[go.Figure]:
        """
        Generate one distinct Sankey diagram per impact method.
        Save figure(s) to disk, according to the configuration specified in result
        attributes.
        :param table: tabular sankey result data.
        :return: figure, or collection of figure generated.
        """
        figs = []
        for method_name in pd.unique(table["method"]):
            method_data = table[table["method"] == method_name]
            fig = go.Figure(
                data=[
                    go.Sankey(
                        node=dict(
                            pad=15,
                            thickness=20,
                            line=dict(color="black", width=0.5),
                            label=method_data["name"].values,
                            color="blue",
                        ),
                        link=dict(
                            source=method_data["source"].values,
                            target=method_data["parent"].values,
                            value=method_data["score"].values,
                        ),
                    )
                ]
            )
            self.save_figure(fig, name_suffix=method_name)
            figs.append(fig)
        return figs


@register_result("sobol")
class SobolIndexResult(ImpactModelResult):
    """
    Generate sobol S1 index for each impact as a heatmap. Sobol S1 indices represent
    the first order contribution of each model's parameter to the score variance.
    See https://plotly.com/python/sankey-diagram/ for more information.
    """

    parameters: Optional[dict[str, Union[float, str]]] = None
    n: int

    def get_table(self) -> pd.DataFrame:
        """
        Generate sobol S1 indices.
        Save it to disk according to configuration specified in result attributes.
        :return: tabular results as a pandas DataFrame.
        """
        sobol_indices = self.impact_model.get_sobol_s1_indices(n=self.n)
        table = pd.DataFrame(sobol_indices)
        if self.table_save_path is not None:
            os.makedirs(self.table_save_path, exist_ok=True)
            figure_path = os.path.join(self.table_save_path, f"{self.output_name}.csv")
            table.to_csv(figure_path)
        return table

    def get_figure(self, table: pd.DataFrame):
        """
        Generate a heatmap for S1 sobol indices of each model's parameter, and for each
        impact method.
        Save figure(s) to disk, according to the configuration specified in result
        attributes.
        :param table: tabular sankey result data.
        :return: figure, or collection of figure generated.
        """
        pivoted_table = table.pivot(
            index="parameter", columns="method", values="sobol_s1"
        )
        fig = px.imshow(pivoted_table, text_auto=True)
        self.save_figure(fig)
        return fig


@register_result("nodes_sobol")
class NodesSobolIndexResult(ImpactModelResult):
    """ """

    parameters: Optional[dict[str, Union[float, str]]] = None
    n: int

    def get_table(self) -> pd.DataFrame:
        """ """
        sobol_indices = self.impact_model.get_sobol_s1_indices(n=self.n, all_nodes=True)
        table = pd.DataFrame(sobol_indices)
        if self.table_save_path is not None:
            os.makedirs(self.table_save_path, exist_ok=True)
            figure_path = os.path.join(self.table_save_path, f"{self.output_name}.csv")
            table.to_csv(figure_path)
        return table

    def get_figure(self, table: pd.DataFrame):
        """ """
        figures = []
        for method in pd.unique(table["method"]):
            pivoted_table = table[table["method"] == method]
            pivoted_table = pivoted_table.pivot(
                index="parameter", columns="node", values="sobol_s1"
            )
            fig = px.imshow(pivoted_table, text_auto=True)
            self.save_figure(fig, name_suffix=method)
            figures.append(fig)
        return figures


@register_result("nodes_uncertainty")
class NodesUncertaintyResult(ImpactModelResult):
    """
    Generate uncertainty for each node using Monte Carlo. Result figure as a boxplot.
    """

    n: int

    def get_table(self) -> pd.DataFrame:
        """
        Run monte carlo simulation for each node, get all values as a long format table.
        :return: results of each draw for each node as a long format table
        """
        nodes_scores = self.impact_model.get_uncertainty_nodes_scores(n=self.n)
        nodes_scores = [node_scores.to_unpivoted_df() for node_scores in nodes_scores]
        table = pd.concat(nodes_scores)
        table = table.rename(columns={"name": "node"})
        if self.table_save_path is not None:
            os.makedirs(self.table_save_path, exist_ok=True)
            figure_path = os.path.join(self.table_save_path, f"{self.output_name}.csv")
            table.to_csv(figure_path)
        return table

    def get_figure(self, table: pd.DataFrame):
        """
        Display uncertainty result of each node with boxplots, one figure per impact.
        :param table: results of each draw for each node as a long format table
        :return: all figures generated
        """
        figures = []
        for method in pd.unique(table["method"]):
            fig = px.box(table[table["method"] == method], x="node", y="score")
            self.save_figure(fig, name_suffix=method)
            figures.append(fig)
        return figures


@register_result("uncertainty")
class UncertaintyResult(ImpactModelResult):
    n: int
    """
    Generate uncertainty for FU using Monte Carlo. Result figure as a boxplot.
    """

    def get_table(self) -> pd.DataFrame:
        """
        Run monte carlo simulation for FU, get all values as a long format table.
        :return: results of each draw as a long format table
        """
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
        """
        Display uncertainty result of FU with boxplot, one figure per impact.
        :param table: results of each draw for each node as a long format table
        :return: all figures generated
        """
        figures = []
        for method in pd.unique(table["method"]):
            fig = px.box(table[table["method"] == method], x="node", y="score")
            self.save_figure(fig, name_suffix=method)
            figures.append(fig)
        return figures
