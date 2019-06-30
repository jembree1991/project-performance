from flask import Flask, jsonify

from cpu_usage import *

app = Flask(__name__)


@app.route('/cpu')
def cpu():
    return jsonify(cpu=total_cpu_usage())


@app.route('/cpu/core/<corenumber>')
def core_value(corenumber):
    return jsonify(coreusage=cpu_core_usage(corenumber))


@app.route('/cputest')
def cputest():
    return jsonify(totalcpuusage=total_cpu_usage())  #TODO: RETURN KEY AS STRING, NUMBER AS FLOAT


if __name__ == '__main__':
    app.run(debug=True)

