patient_data <- list(
  ARRIVAL_DATE = c('2026-01-15', '2026-01-15'),
  ARRIVAL_TIME = c('0900', '1030'),
  SERVICE_DATE = c('2026-01-15', '2026-01-15'),
  SERVICE_TIME = c('0930', '1100')
)

result <- calculate_wait_times(patient_data)
