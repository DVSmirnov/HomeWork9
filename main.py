import os
import sys
import operator
import json
import re


def maker_parsing(dir, name_of_logs):
    def the_most_common_ip(most_common_ip, ip, count_of_cases):
        if ip in (item["IP"] for item in most_common_ip):
            next(item for item in most_common_ip if item["IP"] == ip)["CASES"] = count_of_cases
            result = sorted(most_common_ip, key=operator.itemgetter("CASES"), reverse=True)
        else:
            most_common_ip.append({"IP": ip, "CASES": count_of_cases})
            result = sorted(most_common_ip, key=operator.itemgetter("CASES"), reverse=True)[:3]
        return result

    def the_longest_ip(longest_ip, line_for_parsing):
        longest_ip.append(line_for_parsing)
        return sorted(longest_ip, key=operator.itemgetter("DURATION"), reverse=True)[:3]

    path_of_logs = dir + name_of_logs
    print(f"Open the log from here {path_of_logs}")
    regex = re.compile(
        r'(?P<IP>.*) - .* \[(?P<DATE_AND_TIME>.*)\] "(?P<METHOD>OPTIONS|GET|HEAD|POST|PUT|PATCH|DELETE|TRACE|CONNECT).*".*"(?P<URL>.*)" ".*" (?P<DURATION>[0-9]+)')
    items = {}
    methods = {}
    top_3_most_common_ip = []
    top_3_longest_ip = []
    count_of_lines = 0

    print("Starting to analyze the logs")
    top_3_fulling = False
    top_3_duration = False

    with open(path_of_logs, "r") as file:
        for line in file:
            parsed_line = regex.match(line).groupdict()
            parsed_line["DURATION"] = int(parsed_line["DURATION"])
            if parsed_line["IP"] not in items.keys():
                items[parsed_line["IP"]] = 1
            else:
                items[parsed_line["IP"]] += 1
            if parsed_line["METHOD"] not in methods.keys():
                methods[parsed_line["METHOD"]] = 1
            else:
                methods[parsed_line["METHOD"]] += 1
            if not top_3_fulling:
                top_3_most_common_ip = the_most_common_ip(top_3_most_common_ip, parsed_line["IP"],
                                                          items[parsed_line["IP"]])
                if len(top_3_most_common_ip) == 3:
                    top_3_fulling = True
            elif items[parsed_line["IP"]] > top_3_most_common_ip[2]["CASES"]:
                top_3_most_common_ip = the_most_common_ip(top_3_most_common_ip, parsed_line["IP"],
                                                          items[parsed_line["IP"]])
            if not top_3_duration:
                top_3_longest_ip = the_longest_ip(top_3_longest_ip, parsed_line)
                if len(top_3_longest_ip) == 3:
                    top_3_duration = True
            elif parsed_line["DURATION"] > top_3_longest_ip[2]["DURATION"]:
                top_3_longest_ip = the_longest_ip(top_3_longest_ip, parsed_line)
            count_of_lines += 1

    print("Ending to analyze the logs")
    print("Number of requests:", count_of_lines)
    print("Requests number by methods:")
    for key, value in methods.items():
        print(f"\t- {key}: {value}")
    print("Top 3 IP addresses with most requests number:")
    ip = top_3_most_common_ip[0]["IP"]
    print(f"\t- 1st. IP: {ip}")
    ip = top_3_most_common_ip[1]["IP"]
    print(f"\t- 2nd. IP: {ip}")
    ip = top_3_most_common_ip[2]["IP"]
    print(f"\t- 3rd. IP: {ip}")
    print("Top 3 longest duration requests:")
    ip = top_3_longest_ip[0]["IP"]
    date_and_time = top_3_longest_ip[0]["DATE_AND_TIME"]
    method = top_3_longest_ip[0]["METHOD"]
    url = top_3_longest_ip[0]["URL"]
    duration = top_3_longest_ip[0]["DURATION"]
    print(f"\t- 1st. IP: {ip} Date and time: {date_and_time} Method: {method} URL: {url} Duration: {duration}")
    ip = top_3_longest_ip[1]["IP"]
    date_and_time = top_3_longest_ip[1]["DATE_AND_TIME"]
    method = top_3_longest_ip[1]["METHOD"]
    url = top_3_longest_ip[1]["URL"]
    duration = top_3_longest_ip[1]["DURATION"]
    print(f"\t- 2nd. IP: {ip} Date and time: {date_and_time} Method: {method} URL: {url} Duration: {duration}")
    ip = top_3_longest_ip[2]["IP"]
    date_and_time = top_3_longest_ip[2]["DATE_AND_TIME"]
    method = top_3_longest_ip[2]["METHOD"]
    url = top_3_longest_ip[2]["URL"]
    duration = top_3_longest_ip[2]["DURATION"]
    print(f"\t- 3rd. IP: {ip} Date and time: {date_and_time} Method: {method} URL: {url} Duration: {duration}")
    data = {
        "TOTAL_REQUESTS": count_of_lines,
        "METHODS": methods,
        "TOP_3_MOST_FREQUENTLY_IPS": {
            "1ST": top_3_most_common_ip[0]["IP"],
            "2ND": top_3_most_common_ip[1]["IP"],
            "3RD": top_3_most_common_ip[2]["IP"]
        },
        "TOP_3_LONGEST_REQUESTS": {
            "1ST": top_3_longest_ip[0],
            "2ND": top_3_longest_ip[1],
            "3RD": top_3_longest_ip[2]
        }
    }
    path_of_json = dir + name_of_logs[:-4] + "_analysis.json"
    with open(file=path_of_json, mode='w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Generated json {path_of_json}")


if len(sys.argv) == 1:
    directory = os.path.dirname(__file__)
    file_names = [f for f in os.listdir(directory) if re.match(r".*\.log$", f)]
    for file_name in file_names:
        maker_parsing(directory + "\\", file_name)
else:
    argument = sys.argv[1]
    if len(argument) < 8:
        file_names = [f for f in os.listdir(argument) if re.match(r".*\.log$", f)]
        for file_name in file_names:
            maker_parsing(argument, file_name)
    elif re.match(r".*\.log$", argument):
        file_name = re.search(r".*\\(.*\.log)$", argument).group(1)
        maker_parsing(argument[:-len(file_name)], file_name)
    else:
        file_names = [f for f in os.listdir(argument) if re.match(r".*\.log$", f)]
        for file_name in file_names:
            maker_parsing(argument, file_name)
