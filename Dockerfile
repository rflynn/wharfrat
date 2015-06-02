from python:2.7-onbuild

ENTRYPOINT ["python"]
CMD ["setup.py", "test"]
