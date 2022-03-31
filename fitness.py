from statistics import mean
from data_loader import red_point_list


w_list = [0.2331, 0.2646, 0.1323, 0.2072, 0.1628]
Cz_list = [45, 130, 37, 11, 45]
alpha = 0.05 # TODO


def get_fitness(gene_data, time_type):
    total_fitness = 0
    is_calculated_list = [ [ False for _ in range(5) ] for _ in range(3000) ]

    for i in range(170):
        use_case = gene_data[i]

        if use_case == -1:
            continue

        total_D = 0
        expected_time_list = []
        for point_info in red_point_list[i].possible_point_list:
            point_object = point_info['point_object']
            distance = point_info['distance']
            expected_time = point_info['expected_time']

            # 파란점이 서비스 범위 밖이면 넘어감
            if distance > Cz_list[use_case] + 1: # 오차범위 1m
                continue

            # 현재 파란점이 이미 "use_case"시설에 대해 계산되었다면 넘어감
            if is_calculated_list[point_object.point_index - 1][use_case]:
                continue

            total_D += point_object.D_list[time_type][use_case]
            if expected_time != -1:
                expected_time_list.append(expected_time)

            is_calculated_list[point_object.point_index - 1][use_case] = True

        total_fitness += w_list[use_case] * (total_D - mean(expected_time_list) * alpha)

    return total_fitness
