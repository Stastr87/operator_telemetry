set telemetry_date=23-05-2023
start py get_general_channel_record_statistic.py localhost %telemetry_date%
start py get_record_statistic_by_channell.py localhost %telemetry_date%
start py get_hardware_statistic.py localhost %telemetry_date%