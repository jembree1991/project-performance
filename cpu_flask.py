from flask import Flask, jsonify, abort

from cpu_usage import *

app = Flask(__name__)


@app.route('/cpu/')
def cpu():
    cpu_dict = {}
    cpu_dict["cpu_usage"] = total_cpu_usage()
    return jsonify(cpu_dict)


@app.route('/cpu/core/<core_number>/')
def core_value(core_number):
    try:
        core_dict = {}
        core_dict["core_usage"] = cpu_core_usage(core_number)
        return jsonify(core_dict)
    except IndexError:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
