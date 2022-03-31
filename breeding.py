"""
유전 알고리즘을 이용해 가장 적합한 시설물 배치 리스트를 구하는 프로그램

실행은 python breeding.py

TODO:
1. fitness.py의 alpha 값 결정
"""

import time

from matplotlib.pyplot import plot, show, xlim, ylim, xlabel, ylabel, figure, axes
from matplotlib.animation import FuncAnimation
from collections import deque
from numpy import mean
from random import uniform

from data_loader import load_data
from fitness import get_fitness


class Generation:
    cnt = -1

    def __init__(self, dna_list):
        Generation.cnt += 1
        self.generation_level = Generation.cnt
        self.DNA_list = dna_list

        self.make_select_list()

    def make_select_list(self):
        """
        dna fitness 만큼의 갯수를 가지는 dna 리스트
        dna1.fitness = 2,
        dna2.fitness = 3, then

        return [dna1, dna1, dna2, dna2, dna2]
        """

        self.select_list = []

        while True:
            for dna in self.DNA_list:
                self.select_list += [ dna for _ in range(int(dna.fitness)) ]

            if len(self.select_list) > 1: # 부모로 선택될 염색체가 최소 1개는 있어야됨
                break

            print("망한 세대라 다시 생성")
            self.DNA_list = [ DNA() for _ in range(DNA_NUM) ]

    def make_child(self):
        """
        지정된 교배 방식을 이용해 자식을 만드는 함수
        """

        # 일정 확률로 돌연변이 발생
        if rand(0, MUTATION_PROBABILITY ** -1) == 77:
            return DNA()

        # select_list를 이용해 부모를 선택 (부모로 선출될 확률은 fitness에 비례)
        parents = [ self.select_list[rand(0, len(self.select_list))] for _ in range(2) ]

        # 교배된 자식 유전자
        bred_gene_data = []

        if CROSS_MODE == 0:
            # 각 교차 포인트를 정한다
            switch_point = (rand(1, CANDIDATE // 2), rand(CANDIDATE // 2, CANDIDATE))

            # 교차 포인트에 다다르면 다른 parent의 유전자 정보를 받아온다
            bred_gene_data += parents[0].gene_data[0:switch_point[0]]
            bred_gene_data += parents[1].gene_data[switch_point[0]:switch_point[1]]
            bred_gene_data += parents[0].gene_data[switch_point[1]:]
        elif CROSS_MODE == 1:
            for i in range(CANDIDATE):
                bred_gene_data.append(parents[rand(0, 2)].gene_data[i])

        return DNA(bred_gene_data)

    def evolution(self):
        print(f"   Start Evolution... (From Generation {self.generation_level})")
        start = time.time()

        sorted_dna_list = sorted(self.DNA_list, key=lambda x: x.fitness, reverse=True)
        new_dna_list = list()

        if EVOLUTION_MODE == 0:
            new_dna_list = [ sorted_dna_list[0] for _ in range(GOOD_DNA_CNT) ]
        else:
            new_dna_list = sorted_dna_list[0:GOOD_DNA_CNT]

        new_dna_list += [ self.make_child() for _ in range(DNA_NUM - GOOD_DNA_CNT) ]

        end = time.time()
        print(f"   Evolution Spent {round(end - start, 2)} sec")

        return Generation(new_dna_list)

    @property
    def mean_fitness(self):
        # 세대 객체의 평균 적합도
        return round(mean([dna.fitness for dna in self.DNA_list]), 2)

    @property
    def best_dna(self):
        return sorted(self.DNA_list, key=lambda x: x.fitness, reverse=True)[0]

    @property
    def fitness_list(self):
        return sorted([round(dna.fitness, 2) for dna in self.DNA_list], key=lambda x: x, reverse=True)


class DNA:
    def __init__(self, gene_data=None):
        # 유전자 정보
        if gene_data is None:
            # -1: 시설을 짓지 않음 / 0 ~ 4: 인덱스에 해당하는 시설을 지음
            self.gene_data = [ rand(-2, USE_CASE_NUM) for _ in range(CANDIDATE) ]
        else:
            self.gene_data = gene_data

        self.fitness = get_fitness(self.gene_data, TIME_TYPE)

    def __repr__(self):
        return f"[Gene {round(self.fitness, 2)} | ({', '.join(str(self.gene_data[i]) for i in range(10))} ...)]"


USE_CASE_NUM         = 5    # 시설 종류 개수
TIME_TYPE            = 0    # 시간대 / 0: 새벽, 1: 출근, 2: 점심, 3: 오후, 4: 퇴근, 5: 심야
CANDIDATE            = 170  # 시설 설치 후보지 개수
DNA_NUM              = 50   # 유전자 개수
GOOD_DNA_CNT         = 5    # 우월 유전자 보존 갯수
MUTATION_PROBABILITY = 0.01 # 돌연변이 확률
BREED_CNT            = 50   # 교배 반복 횟수
GRAPH_WIDTH          = 10000
GRAPH_HEIGHT         = 200  # TODO: Graph Height 정하기

# 진화 방식
# 0: 우월 유전자 보존시 최고 적합도 유전자를 5개 복사하여 보존
# 1: 우월 유전자 보존시 적합도 상위 5개의 유전자를 보존
EVOLUTION_MODE = 1

# 교배 방식
# 0: 2점 교차
# 1: 균등 교차
CROSS_MODE = 1

# 가장 우월한 DNA
MAX_FITNESS = -1
SUPERIOR_DNA = []

# 세대 리스트
GENERATION_LIST = list()

# 기본 라인
line = deque([0], maxlen=GRAPH_WIDTH)

def rand(x, y):
    # x, y 사이의 랜덤값을 int로 리턴
    return int(uniform(x, y))

def go_next_generation(_, l2d):
    global BREED_CNT, MAX_FITNESS, SUPERIOR_DNA

    BREED_CNT -= 1

    # 세대 리스트에서 가장 마지막 세대를 진화시키고, 그 세대를 next_generation 에 저장
    next_generation = GENERATION_LIST[-1].evolution()

    # 세대 리스트에 진화된 세대 저장
    GENERATION_LIST.append(next_generation)

    # 안내 출력
    print(f"\n==[Generation {next_generation.generation_level}]================================================================================\n" \
            f"  mean fitness : {next_generation.mean_fitness}  |  best fitness : {next_generation.best_dna}\n" \
            # f"{next_generation.fitness_list}" \
            "================================================================================================\n")

    # 그리는 라인(리스트) 에 다음 세대 적합도 추가
    line.append(next_generation.best_dna.fitness)

    xlim([0, len(GENERATION_LIST)])

    # 최대 적합도 그래프에 그림
    # plot([MAX_FITNESS] * MAX_X, color='red')

    # 다음 세대 적합도가 저장된 라인 그리기
    l2d.set_data(range(0, len(line)), line)

    # 가장 우월한 DNA 갱신
    if MAX_FITNESS < next_generation.best_dna.fitness:
        SUPERIOR_DNA = next_generation.best_dna
        MAX_FITNESS = next_generation.best_dna.fitness

    # 교배 횟수 만큼 반복하면 종료
    if BREED_CNT <= 0:
        print(f"> Superior DNA ({MAX_FITNESS}) : {SUPERIOR_DNA}")
        ani.event_source.stop()


if __name__ == '__main__':
    # 필요한 데이터 로드
    load_data()

    # 조상을 세대 리스트에 추가
    GENERATION_LIST.append(Generation([ DNA() for _ in range(DNA_NUM) ]))

    fig = figure()

    l1, = axes(xlim=(0, GRAPH_WIDTH), ylim=(0, GRAPH_HEIGHT)).plot([], [])
    ani = FuncAnimation(fig, go_next_generation, fargs=(l1,), interval=50)

    show()
