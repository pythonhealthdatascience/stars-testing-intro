#' Add arrival/service datetimes and waiting time in minutes.
#'
#' @param df Data frame with patient-level data containing `ARRIVAL_DATE`, 
#'   `ARRIVAL_TIME`, `SERVICE_DATE`, and `SERVICE_TIME` columns.
#'
#' @return A copy of the input data frame with additional columns:
#'   `arrival_datetime`, `service_datetime`, and `waittime`.
#'
#' @section Errors:#<<
#' The function will stop with an error if:#<<
#' \itemize{#<<
#'   \item `df` is not a data frame#<<
#'   \item Required columns (`ARRIVAL_DATE`, `ARRIVAL_TIME`,#<<
#'         `SERVICE_DATE`, `SERVICE_TIME`) are missing#<<
#' }#<<
#'
#' @section Warnings:#<<
#' A warning is issued if the input data frame is empty (has no rows).#<<
#'
#' @export
calculate_wait_times <- function(df) {

  # Check `df` is a data frame. Hard fail using stop().#<<
  if (!is.data.frame(df)) {#<<
    stop(sprintf("Expected data frame, got %s", class(df)[1]))#<<
  }#<<
  
  # Check required columns are provided. Hard fail using stop().#<<
  required_cols <- c("ARRIVAL_DATE", "ARRIVAL_TIME", "SERVICE_DATE", "SERVICE_TIME")#<<
  missing_cols <- setdiff(required_cols, names(df))#<<
  if (length(missing_cols) > 0) {#<<
    stop(sprintf("Missing required columns: %s", paste(missing_cols, collapse = ", ")))#<<
  }#<<
  
  # Check if data frame is empty. Graceful fail: return early + raise warning#<<
  if (nrow(df) == 0) {#<<
    warning("Input data frame is empty; returning empty result with expected columns")#<<
    df$arrival_datetime <- as.POSIXct(character(0))#<<
    df$service_datetime <- as.POSIXct(character(0))#<<
    df$waittime <- numeric(0)#<<
    return(df)#<<
  }#<<

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
