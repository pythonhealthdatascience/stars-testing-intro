# User filters data but no records match
empty_df = pd.DataFrame({
    'ARRIVAL_DATE': [],
    'ARRIVAL_TIME': [],
    'SERVICE_DATE': [],
    'SERVICE_TIME': []
})

result = calculate_wait_times(empty_df)
