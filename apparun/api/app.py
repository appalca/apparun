from typing import Dict, List, Union

from fastapi import FastAPI
from pydantic import BaseModel

import apparun.core

app = FastAPI()


class ComputeParams(BaseModel):
    impact_model_name: str
    params: Dict[str, Union[str, float, List[Union[str, float]]]]


class GetModelParams(BaseModel):
    impact_model_name: str


@app.post("/compute/")
def compute(params: ComputeParams):
    scores = apparun.core.compute_impacts(params.impact_model_name, params.params)
    return scores


@app.post("/compute_nodes/")
def compute_nodes(params: ComputeParams):
    scores = apparun.core.compute_impacts(
        params.impact_model_name, params.params, all_nodes=True
    )
    return scores


@app.get("/get_models/")
def get_models():
    valid_impact_models = apparun.core.get_valid_models()
    return valid_impact_models


@app.post("/get_model_params/")
def get_model_params(params: GetModelParams):
    impact_models_params = apparun.core.get_model_params(params.impact_model_name)
    return impact_models_params
