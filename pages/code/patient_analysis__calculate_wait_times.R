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
