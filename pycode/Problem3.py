from utils import *

def find_people():
    people = {}
    for i in range(len(swjl_birth)):
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
        time_difference = timediff(str(swjl_online[i]), str(swjl_offline[i]))
        if time_difference <= 0:
            continue
        personid = swjl_personid[i]
        if personid not in people:
            people[personid] = 1
        else:
            people[personid] += 1
    # find the people with online time greater or equal than 5
    admissible_people = []
    for key, value in people.items():
        if value >= 5:
            admissible_people.append(key)
    return admissible_people

def sort_and_find(count_people):
    pass

def PROBLEM_3(swjl, wb):
    global swjl_personid, swjl_siteid, swjl_offline, swjl_online, swjl_birth, swjl_area
    # get the value of the global varibles from swjl
    swjl_personid = series_to_list(swjl, 'PERSONID')
    swjl_siteid = series_to_numpy(swjl, 'SITEID')
    swjl_offline = series_to_numpy(swjl, 'OFFLINETIME')
    swjl_online = series_to_numpy(swjl, 'ONLINETIME')
    swjl_birth = series_to_numpy(swjl, 'BIRTHDAY')
    swjl_area = series_to_numpy(swjl, 'AREAID')

    count_people = find_people()
    community = sort_and_find(count_people)