from flask import Flask, render_template, request
from runcode import runcode
import os
app = Flask(__name__)


default_py_code = """

if __name__ == "__main__":
    print ("Hello Python World!!")
"""

default_rows = "15"
default_cols = "20"

testcases = list()
@app.route("/")
@app.route("/py")
@app.route("/runpy", methods=['POST', 'GET'])
def runpy():
    if request.method == 'POST':
        code = request.form['code']
        testcase = request.form['testcase']
        data, temp = os.pipe()

        os.write(temp, bytes(testcase, "utf-8"))
        os.close(temp)
        run = runcode.RunPyCode(code, data)
        rescompil, resrun = run.run_py_code()
        print(resrun, rescompil)
        if not resrun:
            resrun = 'No result!'
    else:
        code = default_py_code
        resrun = 'No result!'
        rescompil = "No compilation for Python"

    return render_template("main.html",
                           code=code,
                           target="runpy",
                           resrun=resrun,
                           rescomp=rescompil,  # "No compilation for Python",
                           rows=default_rows, cols=default_cols)


if __name__ == "__main__":
    app.run(debug=True)
