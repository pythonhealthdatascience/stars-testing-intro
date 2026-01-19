test_that("running summary_stats on a single value only returns the mean", {
  data <- c(10)
  res <- summary_stats(data)

  expect_identical(res$mean, 10)
  expect_true(is.na(res$std_dev))
  expect_true(is.na(res$ci_lower))
  expect_true(is.na(res$ci_upper))
})