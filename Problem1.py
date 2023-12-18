from utils import *

def find_illegal_minor_and_adult(illegal_minor_id, illegal_adult_id, illegal_bar_id):
    for i in range(len(swjl_online)):
        # If the date is invalid, skip the iteration
        person_birth = swjl_birth[i]
        try:
            person_birth = int(person_birth)
        except:
            continue
        if person_birth > 20170000 or len(str(person_birth)) != 8:
            continue
        # check areaid
        area = str(swjl_area[i])
        if len(area) != 6 or not is_number(area):
            continue
        birth_format = dayformatter(str(person_birth))
        if birth_format == "Invalid date":
            continue
        # check if the customer is an adult
        is_adult = daydiff(birth_format)
        time_difference = timediff(str(swjl_online[i]), str(swjl_offline[i]))
        if time_difference <= 0:
            continue
        # find the illegal minors
        if not is_adult:
            now_illegal_bar = swjl_siteid[i]
            now_illegal_id = swjl_personid[i]
            now_illegal_birth = swjl_birth[i]
            now_illegal_name = swjl_name[i]
            if now_illegal_bar not in illegal_bar_id:
                illegal_bar_id[now_illegal_bar] = {"adult": 0, "minor": 1}
            else:
                illegal_bar_id[now_illegal_bar]['minor'] += 1
            if now_illegal_id not in illegal_minor_id:
                illegal_minor_id[now_illegal_id] = {'id': now_illegal_id, 'name': now_illegal_name, 'times': 1,
                                                    'birthday': now_illegal_birth}
            else:
                illegal_minor_id[now_illegal_id]['times'] += 1
        # If a person is online for more than 1000 hours successively, we assert that the ID card was illegally
        # use by minors
        elif time_difference >= 168:
            now_illegal_bar = swjl_siteid[i]
            now_illegal_id = swjl_personid[i]
            now_illegal_name = swjl_name[i]
            if now_illegal_bar not in illegal_bar_id:
                illegal_bar_id[now_illegal_bar] = {"adult": 1, "minor": 0}
            else:
                illegal_bar_id[now_illegal_bar]['adult'] += 1
            if now_illegal_id not in illegal_adult_id:
                illegal_adult_id[now_illegal_id] = {'id': now_illegal_id, 'name': now_illegal_name, 'times': 1}
            else:
                illegal_adult_id[now_illegal_id]['times'] += 1
    return illegal_minor_id, illegal_adult_id, illegal_bar_id

def find_illegal_bar(bar):
    illegal_bar_info = {}
    for id in bar.keys():
        for j in range(len(wb_id)):
            if wb_id[j] == id:
                title = wb_title[j]
                illegal_bar_info[id] = {'id': id, 'title': title, 'times': bar[id]['adult'] + bar[id]['minor'],
                                        'adult': bar[id]['adult'], 'minor': bar[id]['minor'],
                                        'lng': wb_lng[j], 'lat': wb_lat[j]}
    return illegal_bar_info

def PROBELM_1(data_swjl, data_wb):
    global swjl_online, swjl_offline, swjl_siteid, swjl_personid, swjl_birth, swjl_name, swjl_area
    global wb_id, wb_title, wb_lng, wb_lat
    swjl_online = series_to_numpy(data_swjl, 'ONLINETIME')
    swjl_offline = series_to_numpy(data_swjl, 'OFFLINETIME')
    swjl_siteid = series_to_numpy(data_swjl, 'SITEID')
    swjl_personid = series_to_list(data_swjl, 'PERSONID')
    swjl_birth = series_to_numpy(data_swjl, 'BIRTHDAY')
    swjl_name = series_to_list(data_swjl, 'CUSTOMERNAME')
    swjl_area = series_to_numpy(data_swjl, 'AREAID')
    wb_id = series_to_numpy(data_wb, 'SITEID')
    wb_title = series_to_list(data_wb, 'TITLE')
    wb_lng = series_to_numpy(data_wb, 'lng')
    wb_lat = series_to_numpy(data_wb, 'lat')


    illegal_bar_id = {}
    illegal_minor_id, illegal_adult_id = {}, {}

    illegal_minor_id, illegal_adult_id, illegal_bar_id = (
                                find_illegal_minor_and_adult(illegal_minor_id, illegal_adult_id, illegal_bar_id))
    illegal_bar_info = find_illegal_bar(illegal_bar_id)

    # sort these results based on the times of illegal use on the Internet
    illegal_adult = sorted(illegal_adult_id.values(), key=lambda x:x['times'], reverse=True)
    illegal_minor = sorted(illegal_minor_id.values(), key=lambda x:x['times'], reverse=True)
    illegal_bar = sorted(illegal_bar_info.values(), key=lambda x:(x['times'], x['minor'], x['adult']), reverse=True)
    return illegal_bar, illegal_adult, illegal_minor