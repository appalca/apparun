FROM python:3.12-slim-trixie

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y git
RUN git clone https://github.com/appalca/apparun.git
RUN pip install -r apparun/requirements.txt

WORKDIR apparun

RUN python -m hatchling build
RUN pip install dist/*.whl --progress-bar off
ENV APPARUN_IMPACT_MODELS_DIR=.

RUN mkdir -p samples/impact_models

EXPOSE 8501

ARG RESOURCES_PATH
ENV RESOURCES_PATH=$RESOURCES_PATH

COPY $RESOURCES_PATH .

ARG CUSTOM_RUN_SCRIPT="apparun/cli/main.py gui"
ENV STREAMLIT_RUN_ARGS=$CUSTOM_RUN_SCRIPT

CMD streamlit run $STREAMLIT_RUN_ARGS
