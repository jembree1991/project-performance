"""Functions for reading proc/stat, and finding total and individual core cpu usage"""

# required imports

import time

# finds line for total cpu, always line 0


def __total_cpu() -> (int, int, int, int, int):
    """
    returns usage for all cores
    :return: tuple of user, nice, system, idle, iowait
    """
    stat_file = open('/proc/stat', 'r')
    line_number = stat_file.readlines()
    total_cpu_line = line_number[0].split()
    user, nice, system, idle, iowait = (total_cpu_line[1], total_cpu_line[2], total_cpu_line[3], total_cpu_line[4],
                                        total_cpu_line[5])
    return int(user), int(nice), int(system), int(idle), int(iowait)


def __cpu_core(n: int) -> (str, int, int, int, int, int):
    """
    returns info for n core
    :param n: 0 indexed core to check
    :return: tuple of cpu name, user ticks, nice ticks, system ticks, idle ticks, iowait ticks
    """
    stat_file = open('/proc/stat', 'r')
    line_number = stat_file.readlines()
    cpu_check = 0
    while line_number[cpu_check].find('cpu%s' % n) != 0:  # checking lines for correct cpu
        cpu_check += 1
    else:                                                   # returning processes if cpu'n' exists
        cpu_line = line_number[cpu_check].split()
        cpu, user, nice, system, idle, iowait = (cpu_line[0], (cpu_line[1]), cpu_line[2], cpu_line[3],
                                                 cpu_line[4], cpu_line[5])
        return cpu, int(user), int(nice), int(system), int(idle), int(iowait)


def total_cpu_usage() -> float:
    """
    calculates core usage based on active and idle ticks
    :return: value within range of 0 - 100
    """
    user_initial, nice_initial, system_initial, idle_initial, iowait_initial = __total_cpu()
    total_active_processes_initial = user_initial + nice_initial + system_initial
    total_idle_initial = idle_initial + iowait_initial

    time.sleep(1)

    user_final, nice_final, system_final, idle_final, iowait_final = __total_cpu()
    total_active_processes_final = user_final + nice_final + system_final
    total_idle_final = idle_final + iowait_final

    active_diff = total_active_processes_final - total_active_processes_initial
    idle_diff = total_idle_final - total_idle_initial
    total_percentage = active_diff / (active_diff + idle_diff) * 100
    return total_percentage


def cpu_core_usage(n: int) -> float:          # cpu does not change, same variable for initial/ final
    """
    returns per core usage based on active and idle ticks
    :param n: 0 indexed core to check
    :return:
    """
    cpu, user_initial, nice_initial, system_initial, idle_initial, iowait_initial = __cpu_core(n)
    total_active_processes_initial = user_initial + nice_initial + system_initial
    total_idle_initial = idle_initial + iowait_initial

    time.sleep(1)

    cpu, user_final, nice_final, system_final, idle_final, iowait_final = __cpu_core(n)
    total_active_processes_final = user_final + nice_final  + system_final
    total_idle_final = idle_final + iowait_final

    active_diff = total_active_processes_final - total_active_processes_initial
    idle_diff = total_idle_final - total_idle_initial
    core_percentage = active_diff / (active_diff + idle_diff) * 100
    return core_percentage
