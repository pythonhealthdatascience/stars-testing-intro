incomplete_df <- data.frame(
  ARRIVAL_DATE = c('2026-01-15', '2026-01-15'),
  ARRIVAL_TIME = c('0900', '1030')
)

result <- calculate_wait_times(incomplete_df)
