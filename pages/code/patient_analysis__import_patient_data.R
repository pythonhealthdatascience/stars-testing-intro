#' Import raw patient data and check that required columns are present.
#'
#' Raises an error if the CSV file does not contain exactly the expected
#' columns in the expected order.
#'
#' @param path Character string giving path to the CSV file containing the
#'   patient data.
#'
#' @return A data frame containing the raw patient-level data.
#'
#' @export
import_patient_data <- function(path) {
  df <- readr::read_csv(path, show_col_types = FALSE)

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
