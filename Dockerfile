FROM python
WORKDIR /test_project/
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV ENV=dev
CMD mkdir ./logs/ && python3 -m pytest -s --alluredir=test_results/ /tests_project/tests/
#CMD python -m pytest -s --alluredir=test_results/ /tests_project/tests/