"""
유전 알고리즘을 이용해 가장 적합한 시설물 배치 리스트를 구하는 프로그램

실행은 python breeding.py

TODO:
1. fitness.py의 dummy_Cz_list 및 alpha 값 갱신
2. D 값들이 현재 무작위 값으로 저장되었으므로, 실제 D 값들을 구하여 데이터를 다시 저장
"""

import time
from matplotlib.pyplot import plot, show, xlim, ylim, xlabel, ylabel, figure, axes
from matplotlib.animation import FuncAnimation
from collections import deque
from numpy import mean
from random import uniform

import data_loader
from fitness import get_fitness


class Generation:
    cnt = -1

    def __init__(self, dna_list):
        Generation.cnt += 1
        self.generation_level = Generation.cnt
        self.DNA_list = dna_list
        self.select_list = self.make_select_list()

    def make_select_list(self):
        """
        dna fitness 만큼의 갯수를 가지는 dna 리스트
        dna1.fitness = 2,
        dna2.fitness = 3, then

        return [dna1, dna1, dna2, dna2, dna2]
        """

        tmp_list = list()

        for dna in self.DNA_list:
            tmp_list += [ dna for _ in range(int(dna.fitness)) ]

        return tmp_list

    def make_child(self):
        """
        2점 교차 방식을 이용해 자식을 만드는 함수
        """

        # 무작위 확률로 돌연변이 발생
        if rand(0, self.mean_fitness * MUTATION_PROBABILITY) == 0:
            return DNA()

        # select_list를 이용해 부모를 선택 (부모로 선출될 확률은 fitness 과 비례)
        parents = [ self.select_list[rand(0, len(self.select_list))] for _ in range(2) ]

        # 각 교차 포인트를 정한다
        switch_point = (rand(1, CANDIDATE // 2), rand(CANDIDATE // 2, CANDIDATE))

        # 교배된 자식 유전자
        bred_gene_data = list()

        # 교차 포인트에 다다르면 다른 parent의 유전자 정보를 받아온다
        bred_gene_data += parents[0].gene_data[0:switch_point[0]]
        bred_gene_data += parents[1].gene_data[switch_point[0]:switch_point[1]]
        bred_gene_data += parents[0].gene_data[switch_point[1]:]

        return DNA(bred_gene_data)

    def evolution(self):
        print(f"   Start Evolution... (From Generation {self.generation_level})")

        sorted_dna_list = sorted(self.DNA_list, key=lambda x: x.fitness, reverse=True)
        new_dna_list = list()

        if EVOLUTION_MODE == 0:
            new_dna_list = [ sorted_dna_list[0] for _ in range(GOOD_DNA_CNT) ]
        else:
            new_dna_list = sorted_dna_list[0:GOOD_DNA_CNT]

        startq = time.time()
        new_dna_list += [ self.make_child() for _ in range(CANDIDATE - GOOD_DNA_CNT) ]
        endq = time.time()
        # print(f"   Evolution Spent {round(endq - startq, 1)} sec") # 3초정도 걸림

        return Generation(new_dna_list)

    @property
    def mean_fitness(self):
        # 세대 객체의 평균 적합도
        return round(mean([dna.fitness for dna in self.DNA_list]), 2)

    @property
    def best_dna(self):
        return sorted(self.DNA_list, key=lambda x: x.fitness, reverse=True)[0]


class DNA:
    def __init__(self, gene_data=None):
        # 유전자 정보
        if gene_data is None:
            # -1: 시설을 짓지 않음 / 0 ~ 4: 인덱스에 해당하는 시설을 지음
            self.gene_data = [ rand(-2, USE_CASE_NUM) for _ in range(CANDIDATE) ]
        else:
            self.gene_data = gene_data

        self.fitness = get_fitness(self.gene_data)

    def __repr__(self):
        return f"[Gene {round(self.fitness, 2)} | ({', '.join(str(self.gene_data[i]) for i in range(10))} ...)]"


# def visualization(generations):
#     # TODO: 얘 사용하는 함수인지 확인

#     fitness_list = [generation.fitness for generation in generations]

#     # 최대 적합도를 그래프에 나타냄
#     # max_fitness = DNA.max_fitness()
#     # plot([max_fitness for _ in range(len(generations))])

#     xlim([0, len(generations)])

#     # TODO: 축의 lim 값을 데이터 보다 높게 잡아줌으로써, 그래프의 가독성을 높임
#     ylim([int(min(fitness_list)), (1000 * 1.2)])

#     xlabel('Generation')
#     ylabel('Fitness Score')

#     # 각 세대의 (평균) 적합도를 이용해 그래프에 나타냄
#     plot([generation.fitness for generation in generations])

#     show()


USE_CASE_NUM         = 5    # 시설 종류 개수
CANDIDATE            = 170  # 시설 설치 후보지 개수
GOOD_DNA_CNT         = 5    # 우월 유전자 보존 갯수
MUTATION_PROBABILITY = 0.1  # 돌연변이 확률 / fitness가 높을수록 돌연변이 확률이 적어짐
BREED_CNT            = 50   # 교배 반복 횟수
GRAPH_WIDTH          = 10000
GRAPH_HEIGHT         = 400  # TODO: Graph Height 정하기

# 진화 모드
# 0: 우월 유전자 보존시 최고 적합도 유전자를 5개 복사하여 보존
# 1: 우월 유전자 보존시 적합도 상위 5개의 유전자를 보존
EVOLUTION_MODE = 1

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
    data_loader.load_data()

    # 조상을 세대 리스트에 추가
    GENERATION_LIST.append(Generation([ DNA() for _ in range(100) ]))

    fig = figure()

    l1, = axes(xlim=(0, GRAPH_WIDTH), ylim=(200, GRAPH_HEIGHT)).plot([], [])
    ani = FuncAnimation(fig, go_next_generation, fargs=(l1,), interval=50)

    show()
