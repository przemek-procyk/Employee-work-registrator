import datetime




def seconds_to_hours_from_timedelta(timedelta_obj):
    decimal_hours = timedelta_obj.days * 24 + timedelta_obj.seconds / 3600
    full_hours = int(decimal_hours // 1)
    fraction_part = decimal_hours % 1
    clock_minutes =  round(fraction_part * 60)
    return {"full_hours":full_hours, "clock_minutes":clock_minutes}



########################################## development quickTesting here
# if __name__ == "__main__":
#     delta = datetime.timedelta(seconds=333695)
#     print(str(delta))
#     hours = seconds_to_hours_from_timedelta(delta)
#     print(hours)
    

