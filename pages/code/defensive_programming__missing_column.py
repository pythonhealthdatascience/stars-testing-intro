# User forgot to include SERVICE columns
incomplete_df = pd.DataFrame({
    'ARRIVAL_DATE': ['2026-01-15', '2026-01-15'],
    'ARRIVAL_TIME': ['0900', '1030']
})

result = calculate_wait_times(incomplete_df)