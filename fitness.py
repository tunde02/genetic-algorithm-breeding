from statistics import mean
from data_loader import red_point_list


w_list = [0.2331, 0.2646, 0.1323, 0.2072, 0.1628]
Cz_list = [45, 130, 37, 11, 45]
ALPHA = 0.0005 # TODO
BUS_WEIGHT = 2.3 # TODO


def get_fitness(gene_data, time_type):
    total_fitness = 0
    is_calculated_list = [ [ False for _ in range(5) ] for _ in range(3000) ]

    for i in range(170):
        use_case = gene_data[i]
        bus_weight = 1

        if use_case == -1:
            continue

        point_info_list = red_point_list[i].possible_point_list[:]
        if use_case == 1: # 버스일 경우 far_point_list 추가
            point_info_list += red_point_list[i].far_point_list[:]
            bus_weight = BUS_WEIGHT

        total_D = 0
        car_expected_time_list = []
        walk_expected_time_list = []
        for point_info in point_info_list:
            index = point_info['point_index'] - 1
            isRoad = point_info['isRoad']
            D_list = point_info['D_list']
            distance = point_info['distance']
            expected_time = point_info['expected_time']

            # 파란점이 서비스 범위 밖이면 넘어감
            if distance > Cz_list[use_case] + 1: # 오차범위 1m
                continue

            if expected_time != -1: # use_case가 1일 경우 소요시간 무시
                if isRoad:
                    car_expected_time_list.append(expected_time)
                else:
                    walk_expected_time_list.append(expected_time)

            # use_case에 대해 계산된 적 없는 파란점일 때만 total_D에 추가
            if not is_calculated_list[index][use_case]:
                total_D += D_list[time_type][use_case]

                is_calculated_list[index][use_case] = True

        A = mean(car_expected_time_list) * mean(walk_expected_time_list) * ALPHA * bus_weight
        total_fitness += w_list[use_case] * (total_D - A)

    return total_fitness
