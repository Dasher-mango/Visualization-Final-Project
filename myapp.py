from flask import Flask
from flask import render_template
from utils import *
from Problem1 import PROBELM_1
from Problem2 import PROBLEM_2
from Problem4 import PROBLEM_4

app = Flask(__name__)
@app.route('/')

def black_bar():

    path = './data'
    data_swjl, data_wb = read_csv(path)
    print("--------------------------------")
    print("The data have already been read!")
    print("--------------------------------")
    data_swjl, data_wb = data_clean(data_swjl, data_wb)
    print("The data have already been cleaned!")
    print("--------------------------------")
    process_areaid()
    print("AreaID---AreaName converter generated!")
    print("--------------------------------")

    # PROBLEM 1
    illegal_bar, illegal_adult, illegal_minor = PROBELM_1(data_swjl, data_wb)
    save_as_csv(illegal_adult, "./output_csv/adult.csv")
    save_as_csv(illegal_minor, "./output_csv/minor.csv")
    save_as_csv(illegal_bar, "./output_csv/bar.csv")

    # PROBLEM 2
    float_population = PROBLEM_2(data_swjl)
    save_as_csv(float_population, "./output_csv/float.csv")

    # PROBLEM 3

    # PROBLEM 4
    all_data_info = PROBLEM_4(data_swjl, data_wb)
    save_as_csv(all_data_info, "./output_csv/all_info.csv")

    return render_template('main.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True, port = 80)
