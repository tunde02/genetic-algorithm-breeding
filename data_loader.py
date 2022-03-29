import pickle, time


TOTAL_POINT_NUM = 3000
RED_POINT_NUM = 170

point_list = []
red_point_list = []


class Point:
    def __init__(self, point_index, x, y, isRoad, D_list, distance_list):
        self.point_index = point_index
        self.x = x
        self.y = y
        self.isRoad = isRoad
        self.D_list = D_list
        self.distance_list = distance_list

    def __str__(self) -> str:
        return "====================\n" \
            f"point_index : {self.point_index}\n" \
            f"position : {(self.x, self.y)}\n" \
            f"isRoad : {self.isRoad}\n" \
            f"D_list : {self.D_list}"


class RedPoint(Point):
    def __init__(self, point_index, x, y, isRoad, D_list, distance_list, possible_point_list):
        super().__init__(point_index, x, y, isRoad, D_list, distance_list)
        # self.red_point_index = red_point_index
        self.possible_point_list = possible_point_list


def load_data():
    start = time.time()

    with open('./point_list.p', 'rb') as f:
        for _ in range(TOTAL_POINT_NUM):
            point_list.append(pickle.load(f))

    print(f"> Complete Load \"point_list\" ({round(time.time() - start, 2)} sec)")

    with open('./red_point_list.p', 'rb') as f:
        for _ in range(RED_POINT_NUM):
            red_point_list.append(pickle.load(f))

    print(f"> Complete Load \"red_point_list\" ({round(time.time() - start, 2)} sec)")


if __name__ == "__main__":
    load_data()
    print("hello")