import math


class Union:
    def __init__(self, pre_node, val):
        self.val = val
        self.pre_node = pre_node


class GraphNode:
    def __init__(self, next_node, weight):
        self.next_node = next_node
        self.weight = weight


str_seq = "经常有意见分歧"
probability_dictionary = {"经常": 0.1,
                          "经": 0.05,
                          "有": 0.1,
                          '有意见': 0.1,
                          '意见': 0.2,
                          "分歧": 0.2,
                          "见": 0.05,
                          "意": 0.05,
                          "见分歧": 0.05,
                          "分": 0.1}

for k, v in probability_dictionary.items():
    probability_dictionary[k] = round(-math.log(v, math.e), 1)
graph = {}
key_max_len = max([len(key) for key in probability_dictionary.keys()])

for step in range(1, key_max_len + 1):
    for pos in range(0, len(str_seq) - step + 1):
        if str_seq[pos:pos + step] in probability_dictionary.keys():
            if str(pos + 1) not in graph.keys():
                graph[str(pos + 1)] = [
                    GraphNode(str(pos + step + 1), probability_dictionary[str_seq[pos:pos + step]])]
            else:
                graph[str(pos + 1)].append(
                    GraphNode(str(pos + step + 1), probability_dictionary[str_seq[pos:pos + step]]))
        else:
            if step == 1:
                if str(pos + 1) not in graph.keys():
                    graph[str(pos + 1)] = [GraphNode(str(pos + 1 + 1), 20)]
                else:
                    graph[str(pos + 1)].append(GraphNode(str(pos + 1 + 1), 20))

graph[str(len(str_seq) + 1)] = []


def viterbi():
    node_list = []
    union_list = [Union(0, 0)]
    paths_list = []
    for i in list(graph.keys())[1:]:
        for key, value_list in graph.items():
            for j in value_list:
                if j.next_node == i:
                    node_list.append(key)
                    paths_list.append(union_list[int(key) - 1].val + j.weight)
                    break
        union_list.append(Union(node_list[paths_list.index(min(paths_list))], min(paths_list)))
        node_list.clear()
        paths_list.clear()
    union_list.append(Union(str(len(graph)), -1))
    return union_list


if __name__ == '__main__':
    res_list = viterbi()
    path_list = []
    node = res_list[-1].pre_node
    while node != 0:
        path_list.append(node)
        node = res_list[int(node) - 1].pre_node
    path_list.reverse()
    print("切词方式：", end=' ')
    [print(i, end=' ') for i in path_list]
    res = ""
    i = path_list[0]
    for i in range(len(path_list) - 1):
        res += str_seq[int(path_list[i]) - 1:int(path_list[i + 1]) - 1]
        res += "//"
    print("\n切词结果：", res)
