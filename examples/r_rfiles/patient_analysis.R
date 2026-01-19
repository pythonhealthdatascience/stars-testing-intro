# Function to summarise patient waiting time data.

# Just contains this function, as this folder is used to demonstrate how to run
# tests when code is not structured as package. For full example code (which is
# structured as a package), see examples/python_package/.

library(dplyr)


#' Calculate mean, standard deviation and 95% confidence interval (CI).
#'
#' CI is calculated using the t-distribution, which is appropriate for
#' small samples and converges to the normal distribution as the sample
#' size increases.
#'
#' @param data Numeric vector of data to use in the calculation.
#'
#' @return A named list with elements `mean`, `std_dev`, `ci_lower` and 
#'   `ci_upper`. Each value is a numeric, or `NA` if it can't be computed.
#'
#' @export
summary_stats <- function(data) {
  tibble::tibble(value = data) |>
    dplyr::reframe(
      n_complete = sum(!is.na(value)),
      mean = mean(value, na.rm = TRUE),
      std_dev = stats::sd(value, na.rm = TRUE),
      ci_lower   = {
        if (n_complete < 2L) {
          NA_real_
        } else if (std_dev == 0 || is.na(std_dev)) {
          mean       # CI collapses to mean when no variation
        } else {
          stats::t.test(value)$conf.int[1L]
        }
      },
      ci_upper   = {
        if (n_complete < 2L) {
          NA_real_
        } else if (std_dev == 0 || is.na(std_dev)) {
          mean       # CI collapses to mean when no variation
        } else {
          stats::t.test(value)$conf.int[2L]
        }
      }
    ) |>
    dplyr::select(-n_complete) |>
    as.list()
}
