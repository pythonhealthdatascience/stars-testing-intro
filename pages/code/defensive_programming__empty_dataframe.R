empty_df <- data.frame(
  ARRIVAL_DATE = character(0),
  ARRIVAL_TIME = character(0),
  SERVICE_DATE = character(0),
  SERVICE_TIME = character(0)
)

result <- calculate_wait_times(empty_df)