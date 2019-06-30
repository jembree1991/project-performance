from flask import Flask, render_template, jsonify

from cpu_usage import *

app = Flask(__name__)


@app.route('/cpu')
def cpu():
    return render_template('total_cpu.html', cpu=total_cpu_usage())


@app.route('/cpu/core/<corenumber>')
def core_value(corenumber):
    return render_template('cpu_core.html', number=corenumber, core=cpu_core_usage(corenumber))


@app.route('/cputest')
def cputest():
    return jsonify(totalcpuusage=total_cpu_usage())  #TODO: RETURN KEY AS STRING, NUMBER AS FLOAT


if __name__ == '__main__':
    app.run(debug=True)

