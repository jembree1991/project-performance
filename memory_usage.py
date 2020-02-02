"""Calculating memory usage"""


def __mem_usage() -> (int, int):
    mem_file = open('/proc/meminfo', 'r')
    mem_read = mem_file.readlines()
    mem_total, mem_available = (mem_read[0].split()[1], mem_read[2].split()[1])
    return int(mem_total), int(mem_available)


def __mem_per_process(pid: int) -> int:
    """
    returns info for pid process
    :param pid: process id number
    :return: tuple of process uptime, kernel time, and children time
    """
    mem_file = open('/proc/%s/status' % pid, 'r')
    mem_read = mem_file.readlines()
    vm_rss = mem_read[21].split()[1]
    return int(vm_rss)


def total_mem_usage():
    mem_total, mem_available = __mem_usage()
    mem_used = mem_total - mem_available
    mem_percentage = mem_used / mem_total
    return mem_percentage


def mem_process_usage(pid):
    mem_total = __mem_usage()[0]
    vm_rss = __mem_per_process(pid)
    process_percentage = vm_rss / mem_total
    return process_percentage
