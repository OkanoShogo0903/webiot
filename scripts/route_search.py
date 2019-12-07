# -*- coding: utf-8 -*-
import copy
import numpy as np

class RouteController():

    # 初期化
    def __init__(self):
        self.pre_env = []
        self.transition_matrix = []
        self.y_act = {'u':-1, 'd':1, 'r':0, 'l':0 }
        self.x_act = {'u':0,  'd':0, 'r':1, 'l':-1}

    '''
    遷移行列に従い次の座標を指定

    actions :{"u":"up","d":"down","r":"right","l":"left"}
    '''
    def act(self, now_state):
        action = self.transition_matrix[now_state[0]][now_state[1]]
        # np.arrayは[y][x]で指定するので，[x][y]に並び替えて返す
        return [now_state[1]+self.x_act[action],now_state[0]+self.y_act[action]]

    '''
    最短経路探索(幅優先探索)

        : 遷移行列の更新を行う
    '''

    def search(self,goal_position):
        queue = [goal_position]
        self.transition_matrix[goal_position[0]][goal_position[1]] = 'g'

        while True:

            # 上ブロックの確認
            if self.transition_matrix[queue[0][0]+1][queue[0][1]] == '0':
                self.transition_matrix[queue[0][0]+1][queue[0][1]] = 'u'
                queue.append([queue[0][0]+1,queue[0][1]])

            # 右ブロックの確認
            if self.transition_matrix[queue[0][0]][queue[0][1]+1] == '0':
                self.transition_matrix[queue[0][0]][queue[0][1]+1] = 'l'
                queue.append([queue[0][0],queue[0][1]+1])

            # 左ブロックの確認
            if self.transition_matrix[queue[0][0]][queue[0][1]-1] == '0':
                self.transition_matrix[queue[0][0]][queue[0][1]-1] = 'r'
                queue.append([queue[0][0],queue[0][1]-1])

            # 右ブロックの確認
            if self.transition_matrix[queue[0][0]-1][queue[0][1]] == '0':
                self.transition_matrix[queue[0][0]-1][queue[0][1]] = 'd'
                queue.append([queue[0][0]-1,queue[0][1]])

            queue.pop(0)
            if queue == []:
                break
    '''
    受け取るもの
    env           :{"道":0,"障害物":1}の要素を持つ２次元のnp.array配列

                    np.array([[1,1,1,1,1],
                              [1,0,0,0,1],...])

    now_position  :現在いる座標の値 [y, x]
    goal_position :ゴールの座標の値 [y, x]

    '''
    def predict(self, env, now_position, goal_position):
        if env != self.pre_env:
            self.pre_env = env
            self.transition_matrix = copy.deepcopy(env).astype(np.int).astype(np.unicode)
            self.search(goal_position)
        return self.act(now_position)

    def show_matrix(self):
        return (self.transition_matrix)
