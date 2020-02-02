"""Functions for reading proc/stat, and finding total, individual core, and per process cpu usage"""

# required imports

import time
import os

# finds line for total cpu, always line 0

print("this ran")


def __total_cpu() -> (int, int, int, int, int):
    """
    returns info for all cores
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
        return str(cpu), int(user), int(nice), int(system), int(idle), int(iowait)


def __per_process(pid: int) -> (int, int, int, int):
    """
    returns info for pid process
    :param pid: process id number
    :return: tuple of process uptime, kernel time, and children time
    """
    process_file = open('/proc/%s/stat' % pid, 'r')
    process_read = process_file.readline().split()
    comm, utime, stime, cutime, cstime = (process_read[1], process_read[13], process_read[14], process_read[15],
                                               process_read[16])
    return str(comm), int(utime), int(stime), int(cutime), int(cstime)


def core_read():
    """
    checks for number of cores in system, and appends cores to list
    :return: list of cores "cpu0" to "cpui"
    """
    cores = []
    stat_file = open('/proc/stat', 'r')
    line_number = stat_file.readlines()
    for i in range(len(line_number) - 1):
        if 'cpu' in line_number[i + 1]:
            cpu_line = line_number[i + 1].split()
            cores.append(cpu_line[0])
    return cores


def process_dirs():
    """
    tests if directory is a pid, returns all pids
    :return: dict of int: string -> key: value
    """
    process_id = []
    comm = []
    with os.scandir('/proc/') as entries:
        for entry in entries:
            try:
                process_id_test = int(entry.name)
                process_id.append(process_id_test)
                comm.append(__per_process(process_id_test)[0])
            except ValueError:
                pass
    return process_id, comm


def total_cpu_usage() -> float:
    """
    calculates core usage based on active and idle ticks
    :return: float within range of 0 - 100
    """
    user_initial, nice_initial, system_initial, idle_initial, iowait_initial = __total_cpu()
    total_active_processes_initial = user_initial + nice_initial + system_initial
    total_idle_initial = idle_initial + iowait_initial

    time.sleep(1)       # TODO: May not want to include iowait in idle time (inaccurate)

    user_final, nice_final, system_final, idle_final, iowait_final = __total_cpu()
    total_active_processes_final = user_final + nice_final + system_final
    total_idle_final = idle_final + iowait_final

    active_diff = total_active_processes_final - total_active_processes_initial
    idle_diff = total_idle_final - total_idle_initial
    total_percentage = active_diff / (active_diff + idle_diff) * 100
    return total_percentage


def cpu_core_usage(n: int) -> float:          # cpu does not change, same variable for initial/ final
    """
    calulcates per core usage based on active and idle ticks
    :param n: 0 indexed core to check
    :return: float cpu core usage within range 0-100
    """
    cpu, user_initial, nice_initial, system_initial, idle_initial, iowait_initial = __cpu_core(n)
    total_active_processes_initial = user_initial + nice_initial + system_initial
    total_idle_initial = idle_initial + iowait_initial

    time.sleep(1)

    cpu, user_final, nice_final, system_final, idle_final, iowait_final = __cpu_core(n)
    total_active_processes_final = user_final + nice_final + system_final
    total_idle_final = idle_final + iowait_final

    active_diff = total_active_processes_final - total_active_processes_initial
    idle_diff = total_idle_final - total_idle_initial
    core_percentage = active_diff / (active_diff + idle_diff) * 100
    return core_percentage


def per_process_usage(pid: int) -> float:
    """
    calculates cpu usage per process from /proc/[pid]
    :param pid: process id number
    :return: float cpu usage of process id pid within range 0-100
    """
    comm, utime_initial, stime_initial, cutime_initial, cstime_initial = __per_process(pid)
    user_initial, nice_initial, system_initial, idle_initial, iowait_initial = __total_cpu()
    total_process_initial = utime_initial + stime_initial + cutime_initial + cstime_initial
    total_other_initial = user_initial + nice_initial + system_initial + idle_initial + iowait_initial

    time.sleep(1)

    comm, utime_final, stime_final, cutime_final, cstime_final = __per_process(pid)
    user_final, nice_final, system_final, idle_final, iowait_final = __total_cpu()
    total_process_final = utime_final + stime_final + cutime_final + cstime_final
    total_other_final = user_final + nice_final + system_final + idle_final + iowait_final

    process_diff = total_process_final - total_process_initial
    other_diff = total_other_final - total_other_initial
    process_percentage = process_diff / (process_diff + other_diff) * 100
    return process_percentage

