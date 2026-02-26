FROM python:3.12-slim-trixie

RUN git clone https://github.com/appalca/apparun.git
RUN pip install apparun/requirements.txt
WORKDIR apparun

RUN mkdir samples/impact_models

COPY impact_models/ impact_models/

EXPOSE 8501
CMD ["streamlit", "run", "apparun/cli/main.py", "generate-gui", "samples/conf/sample_gui.yaml"]
