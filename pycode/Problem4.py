from utils import *

def PROBLEM_4(data_swjl, data_wb):
    global swjl_online, swjl_offline, swjl_siteid, swjl_birth, swjl_areaid, swjl_xb
    swjl_online = series_to_numpy(data_swjl, 'ONLINETIME')
    swjl_offline = series_to_numpy(data_swjl, 'OFFLINETIME')
    swjl_siteid = series_to_numpy(data_swjl, 'SITEID')
    swjl_birth = series_to_numpy(data_swjl, 'BIRTHDAY')
    swjl_areaid = series_to_numpy(data_swjl, 'AREAID')
    swjl_xb = series_to_list(data_swjl, 'XB')

    # we need the information of siteid, xb, duration, areaid, age, hour
    all_info = []
    for i in range(len(data_swjl)):
        # check area
        area = str(swjl_areaid[i])
        if len(area) != 6 or not is_number(area):
            continue
        # check birthday
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
        if duration > 0:
            average = average_time(str(onlinetime), str(offlinetime))
            if average:
                med_hour = average.hour
                all_info.append({'siteid': swjl_siteid[i], 'xb': swjl_xb[i], 'duration': round(duration, 2),
                                 'area': area, 'age': compute_age(birth_format), 'hour': med_hour})

    return all_info