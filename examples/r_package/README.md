# R example: patient waiting times

This small R example is used in our HDR UK testing tutorial to show how to test analysis code on patient waiting times.

The package includes functions that:

1. Load patient-level data from a CSV file and check that it has the expected columns.
2. Calculate waiting time in minutes from arrival and service start datetimes.
3. Compute basic summary statistics (mean, standard deviation, and 95% confidence interval) for waiting time.

The example also includes tests for each function, so you can see how to write and run tests to check that your analysis code behaves as expected.
