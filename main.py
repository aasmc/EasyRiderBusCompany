import json
import re


BUS_ID = "bus_id"
STOP_ID = "stop_id"
STOP_NAME = "stop_name"
NEXT_STOP = "next_stop"
STOP_TYPE = "stop_type"
ARRIVAL_TIME = "a_time"


FORMAT_REQUIRED_FIELDS = [STOP_NAME, STOP_TYPE, ARRIVAL_TIME]


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


if __name__ == '__main__':
    check_format_errors()

