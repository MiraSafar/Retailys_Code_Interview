FROM python:3.8-alpine

COPY retailys_code_interview.py /
COPY export_full.xml /

ENTRYPOINT [ "python", "./retailys_code_interview.py" ]