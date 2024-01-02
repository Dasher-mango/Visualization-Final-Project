from utils import *

def PROBLEM_2(data_swjl):
    swjl_online = series_to_numpy(data_swjl, 'ONLINETIME')
    swjl_offline = series_to_numpy(data_swjl, 'OFFLINETIME')
    swjl_area = series_to_numpy(data_swjl, 'AREAID')
    swjl_birth = series_to_numpy(data_swjl, 'BIRTHDAY')
    swjl_xb = series_to_list(data_swjl, 'XB')
    float_peop = []
    for i in range(len(data_swjl)):
        area = str(swjl_area[i])
        # If the date is invalid, skip the iteration
        if area[0: 2] != "50" and len(area) == 6 and is_number(area):
            person_birth = swjl_birth[i]
            try:
                person_birth = int(person_birth)
            except:
                continue
            if person_birth > 20170000 or len(str(person_birth)) != 8:
                continue
            birth_format = dayformatter(str(person_birth))
            if birth_format == "Invalid date":
                continue
            onlinetime, offlinetime = swjl_online[i], swjl_offline[i]
            duration = timediff(str(onlinetime), str(offlinetime))
            # if onlinetime is less than offlinetime, then this row of data is invalid, skip it
            if duration > 0:
                average = average_time(str(onlinetime), str(offlinetime))
                if average:
                    med_hour = average.hour
                    float_peop.append({'area': area, 'hour': med_hour, 'duration': round(duration, 2), 'age': compute_age(birth_format), 'xb': swjl_xb[i]})
    return float_peop