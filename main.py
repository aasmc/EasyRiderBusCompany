import json
import re

BUS_ID = "bus_id"
STOP_ID = "stop_id"
STOP_NAME = "stop_name"
NEXT_STOP = "next_stop"
STOP_TYPE = "stop_type"
ARRIVAL_TIME = "a_time"

FORMAT_REQUIRED_FIELDS = [STOP_NAME, STOP_TYPE, ARRIVAL_TIME]


class NoStartEndStopException(Exception):
    def __init__(self, bus_id):
        self.message = f"There is no start or end stop for the line: {bus_id}."
        super().__init__(self.message)


def get_bus_stop_info():
    info = {}
    with open("test.json", 'r') as f:
        info = json.load(f)
    # info = json.loads(input())
    return info


errors_dict = {
    BUS_ID: 0,
    STOP_ID: 0,
    STOP_NAME: 0,
    NEXT_STOP: 0,
    STOP_TYPE: 0,
    ARRIVAL_TIME: 0,
}

bus_id_to_num_stops = dict()


def check_info_ignore_format(bus_info_dict, pos_to_check, type_to_check, required):
    info = bus_info_dict.get(pos_to_check)
    if type_to_check == int and info == 0:
        return 0
    if (not info and required) or not isinstance(info, type_to_check):
        errors_dict[pos_to_check] += 1
        return 1
    else:
        return 0


def check_info_and_format(bus_dict_info, pos_to_check, type_to_check, required, pattern):
    info = bus_dict_info.get(pos_to_check)
    if (not info and required) or not isinstance(info, type_to_check):
        errors_dict[pos_to_check] += 1
        return 1
    elif not info and not required:
        return 0
    elif type_to_check == str and not pattern.match(info):
        errors_dict[pos_to_check] += 1
        return 1
    else:
        return 0


def check_bus_id(bus_info_dict):
    return check_info_ignore_format(bus_info_dict, BUS_ID, int, True)


def check_stop_id(bus_info_dict):
    return check_info_ignore_format(bus_info_dict, STOP_ID, int, True)


def check_stop_name(bus_info_dict):
    pattern = re.compile(r"^\b[A-Z]\w+\b (\b[A-Z]\w+\b )?(Road|Avenue|Boulevard|Street)$")
    return check_info_and_format(bus_info_dict, STOP_NAME, str, True, pattern)


def check_next_stop(bus_info_dict):
    return check_info_ignore_format(bus_info_dict, NEXT_STOP, int, True)


def check_stop_type(bus_info_dict):
    pattern = re.compile(r"^[SOF]$")
    return check_info_and_format(bus_info_dict, STOP_TYPE, str, False, pattern)


def check_arrival_time(bus_info_dict):
    pattern = re.compile(r"^[0-2]\d:[0-5]\d$")
    return check_info_and_format(bus_info_dict, ARRIVAL_TIME, str, True, pattern)


def check_bus_info_dict(bus_info_dict):
    res = 0
    res += check_bus_id(bus_info_dict)
    res += check_stop_id(bus_info_dict)
    res += check_stop_name(bus_info_dict)
    res += check_next_stop(bus_info_dict)
    res += check_stop_type(bus_info_dict)
    res += check_arrival_time(bus_info_dict)
    return res


def check_bus_stops(bus_info_list):
    total_errs = 0
    for bus_info_dict in bus_info_list:
        total_errs += check_bus_info_dict(bus_info_dict)
    return total_errs


def check_bus_stops_for_format_errors(bus_info_list):
    total = 0
    for d in bus_info_list:
        total += check_format_errors_in_dict(d)
    return total


def check_format_errors_in_dict(bus_info_dict):
    res = 0
    res += check_stop_name(bus_info_dict)
    res += check_stop_type(bus_info_dict)
    res += check_arrival_time(bus_info_dict)
    return res


def check_format_errors():
    bus_list = get_bus_stop_info()
    res = check_bus_stops_for_format_errors(bus_list)
    print(f"Format validation: {res} errors")
    for key in FORMAT_REQUIRED_FIELDS:
        print(f"{key}: {errors_dict.get(key)}")


def check_errors():
    bus_list = get_bus_stop_info()
    res = check_bus_stops(bus_list)
    print(f"Type and required field validation: {res} errors")
    for key, val in errors_dict.items():
        print(f"{key}: {val}")


def collect_and_print_statistics():
    bus_list = get_bus_stop_info()
    for bus_dict in bus_list:
        bus_id = bus_dict[BUS_ID]
        if bus_id_to_num_stops.get(bus_id):
            bus_id_to_num_stops[bus_id] += 1
        else:
            bus_id_to_num_stops[bus_id] = 1
    print("Line names and number of stops:")
    for key, value in bus_id_to_num_stops.items():
        print(f"bus_id: {key}, stops: {value}")


bus_id_to_start_stop = dict()
bus_id_to_final_stop = dict()
bus_id_to_all_stops = dict()
bus_id_to_ondemand_stops = dict()
start_stops = set()
final_stops = set()


def check_bus_start_final_stops(bus_dict):
    bus_id = bus_dict[BUS_ID]
    stop_type = bus_dict[STOP_TYPE]
    if bus_id_to_all_stops.get(bus_id) is not None:
        bus_id_to_all_stops[bus_id].append(bus_dict[STOP_NAME])
    else:
        bus_id_to_all_stops[bus_id] = []
        bus_id_to_all_stops[bus_id].append(bus_dict[STOP_NAME])
    if stop_type == "S":
        if bus_id_to_start_stop.get(bus_id) is not None:
            raise NoStartEndStopException(bus_id)
        else:
            bus_id_to_start_stop[bus_id] = bus_dict[STOP_NAME]
            start_stops.add(bus_dict[STOP_NAME])
    elif stop_type == "F":
        if bus_id_to_final_stop.get(bus_id) is not None:
            raise NoStartEndStopException(bus_id)
        else:
            bus_id_to_final_stop[bus_id] = bus_dict[STOP_NAME]
            final_stops.add(bus_dict[STOP_NAME])
    elif stop_type == "O":
        if bus_id_to_ondemand_stops.get(bus_id) is None:
            bus_id_to_ondemand_stops[bus_id] = []
        bus_id_to_ondemand_stops[bus_id].append(bus_dict[STOP_NAME])


def find_transfer_stops():
    result = set()
    for bus_id, stop_names in bus_id_to_all_stops.items():
        for name in stop_names:
            for other_bus_id, other_stop_names in bus_id_to_all_stops.items():
                if bus_id != other_bus_id:
                    if name in other_stop_names:
                        result.add(name)
    return result


def print_start_final_transfer_stops():
    start = sorted(start_stops)
    final = sorted(final_stops)
    transfer = sorted(find_transfer_stops())
    print(f"Start stops: {len(start_stops)} {list(start)}")
    print(f"Transfer stops: {len(transfer)} {list(transfer)}")
    print(f"Finish stops: {len(final_stops)} {list(final)}")


bus_id_to_stop_name_arrival_time = dict()


def collect_arrival_times():
    bus_lines = get_bus_stop_info()
    for bus_dict in bus_lines:
        bus_id = bus_dict[BUS_ID]
        stop_name = bus_dict[STOP_NAME]
        arrival_time = bus_dict[ARRIVAL_TIME]
        pattern = re.compile(":")
        arrival_time_int = int(pattern.sub("", arrival_time))
        if bus_id_to_stop_name_arrival_time.get(bus_id) is None:
            bus_id_to_stop_name_arrival_time[bus_id] = []
        bus_id_to_stop_name_arrival_time[bus_id].append((stop_name, arrival_time_int))


bus_id_to_incorrect_stop = dict()


def process_arrival_times():
    for bus_id, arrivals in bus_id_to_stop_name_arrival_time.items():
        if arrivals:
            current_arrival_time = arrivals[0][1]
            for i in range(1, len(arrivals)):
                next_arrival_time = arrivals[i][1]
                next_stop_name = arrivals[i][0]
                if next_arrival_time <= current_arrival_time:
                    bus_id_to_incorrect_stop[bus_id] = next_stop_name
                    break
                else:
                    current_arrival_time = next_arrival_time


def print_incorrect_arrival_times():
    print("Arrival time test:")
    if len(bus_id_to_incorrect_stop) == 0:
        print("OK")
    else:
        for bus_id, stop_name in bus_id_to_incorrect_stop.items():
            print(f"bus_id line {bus_id}: wrong time on station {stop_name}")


def check_arrival_times():
    collect_arrival_times()
    process_arrival_times()
    print_incorrect_arrival_times()


def check_on_demand_stops():
    bus_lines = get_bus_stop_info()
    for bus_dict in bus_lines:
        check_bus_start_final_stops(bus_dict)
    transfer_stops = find_transfer_stops()
    error_set = set()
    for bus_id, stops in bus_id_to_ondemand_stops.items():
        for stop in stops:
            if stop in start_stops:
                error_set.add(stop)
            elif stop in final_stops:
                error_set.add(stop)
            elif stop in transfer_stops:
                error_set.add(stop)
    errors = sorted(error_set)
    print("On demand stops test:")
    if len(errors) == 0:
        print("OK")
    else:
        print(f"Wrong stop type: {list(errors)}")


def check_all_buses_start_final_stops():
    bus_lines = get_bus_stop_info()
    try:
        for bus_dict in bus_lines:
            check_bus_start_final_stops(bus_dict)

        for bus_dict in bus_lines:
            bus_id = bus_dict[BUS_ID]
            if bus_id_to_start_stop.get(bus_id) is None or bus_id_to_final_stop.get(bus_id) is None:
                raise NoStartEndStopException(bus_id)

        print_start_final_transfer_stops()
    except NoStartEndStopException as e:
        print(e)


if __name__ == '__main__':
    check_on_demand_stops()

