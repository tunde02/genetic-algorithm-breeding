from data_loader import red_point_list


w_list = [0.2331, 0.2646, 0.1323, 0.2072, 0.1628]
dummy_Cz_list = [50, 25, 50, 10, 55] # TODO
alpha = 0.3 # TODO


def get_fitness(gene_data):
    total_fitness = 0
    has_calculated_list = [ [ False for _ in range(5) ] for _ in range(3000) ]

    for i in range(170):
        use_case = gene_data[i]

        if use_case == -1:
            continue

        for point_info in red_point_list[i].possible_point_list:
            bluePoint = point_info['bluePoint']
            distance = point_info['distance']
            expected_time = point_info['expected_time']

            # 파란점이 서비스 범위 밖이면 넘어감
            if distance > dummy_Cz_list[use_case]:
                continue

            # 현재 파란점이 이미 "use_case"시설에 대해 계산되었다면 넘어감
            if has_calculated_list[bluePoint.point_index - 1][use_case]:
                continue

            total_fitness += w_list[use_case] * (bluePoint.D_list[use_case] - expected_time * alpha)

            has_calculated_list[bluePoint.point_index - 1][use_case] = True

    return total_fitness / 100
