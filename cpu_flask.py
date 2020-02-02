from flask import Flask, jsonify, abort

from cpu_usage import *
from memory_usage import *

app = Flask(__name__)


@app.route('/v1/cpu/')
def cpu():
    cpu_usage = {}
    cores = {}
    core_list = core_read()
    cores["cores"] = core_list
    cpu_usage["cpu_usage"] = total_cpu_usage()
    print(cpu_usage, cores)
    return jsonify(cpu_usage, cores)


@app.route('/v1/cpu/core/<core_number>/')
def core_value(core_number):
    try:
        core_dict = {}
        core_dict["core_usage"] = cpu_core_usage(core_number)
        return jsonify(core_dict)
    except IndexError:
        abort(404)


@app.route('/v1/cpu/process/')
def process_list():
    process_id, comm = process_dirs()
    processes_list = []
    for i in range(len(process_id)):
        temp_process = {}
        temp_process['id'] = process_id[i]
        temp_process['name'] = comm[i]
        processes_list.append(temp_process)
    all_processes = {'Processes': processes_list}
    return jsonify(all_processes)


@app.route('/v1/cpu/process/<pid>/')
def process(pid):
    process_dict = {}
    process_dict[pid] = per_process_usage(pid)
    return jsonify(process_dict)


@app.route('/v1/memory/')
def total_memory():
    memory = {}
    mem_percentage = total_mem_usage()
    memory['memory_usage'] = mem_percentage
    return jsonify(memory)


@app.route('/v1/memory/<pid>/')
def mem_per_process(pid):
    mem_process = {}
    process_percentage = mem_process_usage(pid)
    mem_process[pid] = process_percentage
    return jsonify(mem_process)


if __name__ == '__main__':
    app.run(debug=True)
