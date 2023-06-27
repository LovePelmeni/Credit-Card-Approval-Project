import numpy
import pandas

applications = pandas.read_csv("application_record.csv")
credit_dataset = pandas.read_csv("credit_record.csv")

print(applications.info())
print(credit_dataset.info())
