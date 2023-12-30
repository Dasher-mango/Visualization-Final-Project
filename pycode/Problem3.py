from utils import *

def count_people():
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
        if isinstance(swjl_online[i], str) or isinstance(swjl_offline[i], str):
            continue
        personid = swjl_personid[i]
        if personid not in people:
            people[personid] = [i]
        else:
            new_value = people[personid]
            new_value.append(i)
            people[personid] = new_value 
    return people

def filter_info(people):
    '''
    find the people who has no less than 3 online records
    '''
    new_info = []
    for key, value in people.items():
        times = len(value)
        if times >= 5:
            for j in range(times):
                index = value[j]
                new_info.append({'id': swjl_personid[index], 'siteid': swjl_siteid[index], 'online': swjl_online[index], 'offline': swjl_offline[index]})
    return new_info

def compute_weight(info):
    info = sorted(info, key=lambda x:x['online'], reverse=False)
    weighted_graph = {}
    for i in range(len(info)):
        for j in range(i + 1, len(info)):
            record_from, record_to = info[i], info[j]
            if record_from['id'] == record_to['id']:
                continue
            # if their onlinetime gap is more than 15 mins, we assume that they're not related
            if minutediff(str(record_from['online']), str(record_to['online'])) > 15:
                break
            weight = 1
            # if their offlinetime gap is more than 15 mins, we assume that they're more likely to be related 
            if abs(minutediff(str(record_from['offline']), str(record_to['offline']))) <= 15:
                weight += 1
            # if they are at the same bar, add weight
            if record_from['siteid'] == record_to['siteid']:
                weight += 1
            new_id = str(record_from['id']) + "-" + str(record_to['id'])
            new_reverse_id = str(record_to['id']) + "-" + str(record_from['id'])
            if new_id not in weighted_graph:
                if new_reverse_id not in weighted_graph:
                    weighted_graph[new_id] = weight
                else:
                    continue
            else:
                weighted_graph[new_id] += weight
        for j in range(i - 1, -1, -1):
            record_from, record_to = info[i], info[j]
            if record_from['id'] == record_to['id']:
                continue
            # if their onlinetime gap is more than 15 mins, we assume that they're not related
            if minutediff(str(record_to['online']), str(record_from['online'])) > 15:
                break
            weight = 1
            # if their offlinetime gap is more than 15 mins, we assume that they're more likely to be related 
            if abs(minutediff(str(record_from['offline']), str(record_to['offline']))) <= 15:
                weight += 1
            # if they are at the same bar, add weight
            if record_from['siteid'] == record_to['siteid']:
                weight += 1
            new_id = str(record_from['id']) + "-" + str(record_to['id'])
            new_reverse_id = str(record_to['id']) + "-" + str(record_from['id'])
            if new_id not in weighted_graph:
                if new_reverse_id not in weighted_graph:
                    weighted_graph[new_id] = weight
                else:
                    continue
            else:
                weighted_graph[new_id] += weight
    return weighted_graph

def decoder(graph):
    new_graph = []
    for key, value in graph.items():
        source, target = key.split('-')
        new_graph.append({'source': source, 'target': target, 'weight': value})
    return new_graph

def filter_graph(graph):
    '''
    find the relationship with weight greater or equal than 4
    '''
    new_graph = []
    for i in range(len(graph)):
        if graph[i]['weight'] >= 6:
            new_graph.append(graph[i])
    return new_graph

def write_as_json(graph):
    data = {'nodes': [], 'links': graph}
    edges = []
    for i in range(len(graph)):
        edges.append((graph[i]['source'], graph[i]['target']))
    G = nx.Graph()
    G.add_edges_from(edges)
    group = list(nx.connected_components(G))
    for j in range(len(group)):
        for each in group[j]:
            data['nodes'].append({'id': each, 'group': j + 1})
    file_path = "./templates/weighted_graph.json"
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("File %s has been created in success!" % file_path)
    print("-----------------------------------------------")


def PROBLEM_3(swjl, wb):
    global swjl_personid, swjl_siteid, swjl_offline, swjl_online, swjl_birth, swjl_area
    # get the value of the global varibles from swjl
    swjl_personid = series_to_list(swjl, 'PERSONID')
    swjl_siteid = series_to_numpy(swjl, 'SITEID')
    swjl_offline = series_to_numpy(swjl, 'OFFLINETIME')
    swjl_online = series_to_numpy(swjl, 'ONLINETIME')
    swjl_birth = series_to_numpy(swjl, 'BIRTHDAY')
    swjl_area = series_to_numpy(swjl, 'AREAID')

    people  = count_people()
    info = filter_info(people)
    graph = compute_weight(info)
    graph = decoder(graph)
    graph = filter_graph(graph)
    write_as_json(graph)