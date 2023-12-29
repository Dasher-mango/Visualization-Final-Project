from utils import *
from Problem1 import PROBELM_1
from Problem2 import PROBLEM_2
from Problem3 import PROBLEM_3
from Problem4 import PROBLEM_4


def black_bar():
    print("-----------------------------------------------")
    path = './data'
    data_swjl, data_wb = read_csv(path)
    print("-----------------------------------------------")
    print("Data wb and swjl have already been read!")
    print("-----------------------------------------------")
    data_swjl, data_wb = data_clean(data_swjl, data_wb)
    print("Data wb and swjl have already been cleaned!")
    print("-----------------------------------------------")
    process_areaid()

    # PROBLEM 1
    illegal_bar, illegal_adult, illegal_minor = PROBELM_1(data_swjl, data_wb)
    save_as_csv(illegal_adult, "./output_csv/adult.csv")
    save_as_csv(illegal_minor, "./output_csv/minor.csv")
    save_as_csv(illegal_bar, "./output_csv/bar.csv")

    # PROBLEM 2
    float_population = PROBLEM_2(data_swjl)
    save_as_csv(float_population, "./output_csv/float.csv")

    # PROBLEM 3
    weighted_graph = PROBLEM_3(data_swjl, data_wb)
    save_as_csv(weighted_graph, "./output_csv/weighted_graph.csv")

    # PROBLEM 4
    all_data_info = PROBLEM_4(data_swjl, data_wb)
    save_as_csv(all_data_info, "./output_csv/all_info.csv")

if __name__ == "__main__":
    black_bar()
    print("All output data have been successfully generated!")
    print("-----------------------------------------------")