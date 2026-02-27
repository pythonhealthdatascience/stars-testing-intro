# Functions to import, process, and summarise patient waiting time data.

library(readr)
library(dplyr)
library(lubridate)


#' Import raw patient data and check that required columns are present.
#'
#' Raises an error if the CSV file does not contain exactly the expected
#' columns in the expected order.
#'
#' @param path Character string giving path to the CSV file containing the
#'   patient data.
#' 
#' @importFrom readr read_csv
#'
#' @return A data frame containing the raw patient-level data.
#'
#' @export
import_patient_data <- function(path) {
  df <- read_csv(path, show_col_types = FALSE)

  # Expected columns in the raw data (names and order must match)
  expected <- c(
    "PATIENT_ID",
    "ARRIVAL_DATE", "ARRIVAL_TIME",
    "SERVICE_DATE", "SERVICE_TIME"
  )
  if (!identical(colnames(df), expected)) {
    stop(
      sprintf(
        "Unexpected columns: %s (expected %s)",
        paste(colnames(df), collapse = ", "),
        paste(expected, collapse = ", ")
      )
    )
  }

  df
}


#' Add arrival/service datetimes and waiting time in minutes.
#'
#' @param df Data frame with patient-level data containing `ARRIVAL_DATE`,
#'   `ARRIVAL_TIME`, `SERVICE_DATE`, and `SERVICE_TIME` columns.
#'
#' @return A copy of the input data frame with additional columns:
#'   `arrival_datetime`, `service_datetime`, and `waittime`.
#'
#' @export
calculate_wait_times <- function(df) {
  df <- df |>
    dplyr::mutate(
      arrival_datetime = lubridate::ymd_hm(
        paste(
          as.character(ARRIVAL_DATE),
          sprintf("%04d", as.integer(ARRIVAL_TIME))
        )
      ),
      service_datetime = lubridate::ymd_hm(
        paste(
          as.character(SERVICE_DATE),
          sprintf("%04d", as.integer(SERVICE_TIME))
        )
      )
    )

  if (any(is.na(df$arrival_datetime) | is.na(df$service_datetime))) {
    stop(
      "Failed to parse arrival or service datetimes; ",
      "check for missing or invalid dates/times."
    )
  }

  df <- df |>
    dplyr::mutate(
      waittime = as.numeric(
        difftime(service_datetime, arrival_datetime, units = "mins")
      )
    )

  df
}


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
