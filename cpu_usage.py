"Functions for reading proc/stat, and finding total and core cpu usage"

# required imports

import time
import json

# Read in proc/stat, creating initial line search variable (probably should call per function)

stat_file = open('/proc/stat', 'r')

#line_number = stat_file.readlines()


# finds line for total cpu, always line 0

core_dict = {}


def total_cpu():
    stat_file = open('/proc/stat', 'r')
    line_number = stat_file.readlines()
    total_cpu_line = line_number[0].split()
    user, nice, system, idle, iowait = (total_cpu_line[1], total_cpu_line[2], total_cpu_line[3], total_cpu_line[4],
                                        total_cpu_line[5])
    return user, nice, system, idle, iowait


# searches through stat to find the correct core, returns processes executed



def cpu_core(n):
    stat_file = open('/proc/stat', 'r')
    line_number = stat_file.readlines()
    try:
        cpu_check = 0
        while line_number[cpu_check].find('cpu%s' % n) != 0:  # checking lines for correct cpu
            cpu_check += 1
        else:                                                   # returning processes if cpu'n' exists
            cpu_line = line_number[cpu_check].split()
            cpu, user, nice, system, idle, iowait = (cpu_line[0], (cpu_line[1]), cpu_line[2], cpu_line[3],
                                                          cpu_line[4], cpu_line[5])
            global core_dict
            # core_dict = {"cpu": cpu, 'user': user, 'nice': nice, 'system': system, 'idle': idle, 'iowait': iowait}
            return cpu, user, nice, system, idle, iowait
            # return core_dict
    except IndexError:                                      # catch if requesting core that does not exist
        return "There is no core %s on this system!" % n
    except:                                                 # other catch so function completes
        return "Something went wrong!"


def total_cpu_usage():
    user0, nice0, system0, idle0, iowait0 = total_cpu()
    total_used_processes0 = int(user0) + int(nice0) + int(system0)
    total_idle0 = int(idle0)

    time.sleep(1)

    user1, nice1, system1, idle1, iowait1 = total_cpu()
    total_used_processes1 = int(user1) + int(nice1) + int(system1)
    total_idle1 = int(idle1)
    used_process_diff = total_used_processes1 - total_used_processes0
    idle_diff = total_idle1 - total_idle0
    total_percentage = used_process_diff / idle_diff * 100     #TODO: NEEDS TO BE TOTAL USED OVER TOTAL (USED PLUS IDLE)
    return "{}%".format(total_percentage)


def cpu_core_usage(n):
    try:
        cpu0, user0, nice0, system0, idle0, iowait0 = cpu_core(n)
        total_used_processes0 = int(user0) + int(nice0) + int(system0)
        total_idle0 = int(idle0)
        #core_dict0 = cpu_core(n)
        #total_used_dict = core_dict0['user']
        #print(total_used_dict)

        time.sleep(1)

        cpu1, user1, nice1, system1, idle1, iowait1 = cpu_core(n)
        total_used_processes1 = int(user1) + int(nice1) + int(system1)
        total_idle1 = int(idle1)
        used_process_diff = total_used_processes1 - total_used_processes0
        idle_diff = total_idle1 - total_idle0
        core_percentage = used_process_diff / idle_diff * 100
        return "{}%".format(core_percentage)
    except ValueError:
        return "There is no core %s on this system!" % n


print(" single core", cpu_core_usage(5))

core_json = json.dumps(core_dict)

print(core_json)
