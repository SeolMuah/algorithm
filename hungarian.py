#입력 : 정방행렬 n x n 
#출력 : 비용이 적게 드는 (1:1) 대응 출력

import numpy as np
adj_matrix = np.array([
    [3, 8, 9, 3],
    [4, 12, 7, 6],
    [4, 8, 5, 9],
    [8, 4, 3, 12]
])

adj_matrix = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 9],
    [1, 3, 10, 5],
    [5, 8, 7, 6],
    [3, 6, 8, 1]

])

# adj_matrix = np.array([
#     [1, 2, 3, 4],
#     [5, 6, 7, 9],
#     [1, 3, 10, 5],
# ])
cost_matrix = adj_matrix.copy()


if cost_matrix.shape[0] != cost_matrix.shape[1] : 
    if cost_matrix.shape[0] > cost_matrix.shape[1] :
        cost_matrix = np.c_[adj_matrix, np.zeros(cost_matrix.shape[0], dtype=np.int32)]
    else :
        cost_matrix = np.r_[adj_matrix, np.zeros((1, cost_matrix.shape[1]), dtype=np.int32)]

        
N = len(cost_matrix)
print(cost_matrix)

#1) 모든 행에 대해서, 각 행의 가장 작은 값 빼기
for row in cost_matrix:
    row -= row.min()
print(cost_matrix)
#2) 모든 열에 대해서, 각 열의 가장 작은 값 빼기
for col in cost_matrix.T:
    col -= col.min()
print(cost_matrix)
    
#3) 0을 많이 포함하는 행, 열 라인 얻기
#   - 0을 가장 많이 포함하는 행 또는 열을 하나씩 추가한다.
#   - 0이 Line으로 포함 안된 개수로 비교하되 행과 열중 가장 많은 0을 포함된 행 또는 열을 선택한다., 
#     갯수가 같은 경우, 0이 Line으로 포함된 갯수 까지 같이 비교한다.
while True :
    rLines = []
    cLines = []
    while True :
        row_zeroNums = [(-1,-1)]
        col_zeroNums = [(-1,-1)]
        for i in range(N) :
            if i not in rLines :
                total_zero_num = (cost_matrix[i]==0).sum()
                line_zero_num = (cost_matrix[i][cLines]==0).sum()
                if total_zero_num-line_zero_num > 0 :
                    row_zeroNums.append((i, total_zero_num-line_zero_num, total_zero_num))
            
            if i not in cLines :
                total_zero_num = (cost_matrix.T[i]==0).sum()
                line_zero_num = (cost_matrix.T[i][rLines]==0).sum()
                if total_zero_num-line_zero_num > 0 :
                    col_zeroNums.append((i, total_zero_num-line_zero_num, total_zero_num))
        
        if len(row_zeroNums)==1 and len(col_zeroNums)==1 :
            #0을 다 마킹한 경우 반복문 빠져나오기
            break
        
        row_zeroNums.sort(key=lambda x: x[1], reverse=True)
        col_zeroNums.sort(key=lambda x: x[1], reverse=True)

        if row_zeroNums[0][1] > col_zeroNums[0][1] :
            rLines.append(row_zeroNums[0][0])
        elif row_zeroNums[0][1] == col_zeroNums[0][1] :
            if row_zeroNums[0][2] >= col_zeroNums[0][2] :
                rLines.append(row_zeroNums[0][0])
            else :
                cLines.append(col_zeroNums[0][0])
        else :
            cLines.append(col_zeroNums[0][0])

    #4) Line 개수가 N이 될때까지 아래 사항 반복
    #Line 개수가 N 보다 같거나 크면 매칭
    if len(rLines) + len(cLines) >= N :
        break
    #   - Line이 아닌 요소들의 최솟값을 구해 Line이 아닌 행 또는 열에 뺀다
    min_num = np.array([cost_matrix[i][j] for j in range(N) if j not in cLines for i in range(N) if i not in rLines ]).min()

    if len(rLines) >= len(cLines):
        not_lines = [i for i in range(N) if i not in rLines]
        cost_matrix[not_lines] -= min_num
        #Line 열 중 음수를 갖는 값 만큼 더하기
        for c in cLines :
            for r in not_lines :
                if cost_matrix[r][c] < 0 :
                    cost_matrix[:,c] -= cost_matrix[r][c]
                    break
    else :
        not_lines = [i for i in range(N) if i not in cLines]
        cost_matrix[:, not_lines] -= min_num
        #Line 열 중 음수를 갖는 값 만큼 더하기
        for r in rLines :
            for c in not_lines :
                if cost_matrix[r][c] < 0 :
                    cost_matrix[r, :] -= cost_matrix[r][c]
                    break

print(adj_matrix)
print(cost_matrix)
print(rLines)
print(cLines)

#5) 매칭 인덱스 구하기
#작업 중 (열 기준), 할당된 작업자가 적은 것 부터 할당함
job_infos = [(i, set(np.where(cost_matrix[:, i]==0)[0])) for i in range(N)]

result = dict()
allocated_worker = set()
job_infos
while job_infos :
    job_infos = [(i, workers-allocated_worker) for i, workers in job_infos]
    job_infos.sort(key=lambda x:len(x[1]))
    
    job_info = job_infos.pop(0)
    job_idx = job_info[0]
    worker = job_info[1].pop()
    result[worker] = job_idx
    allocated_worker.add(worker)
 
    
print(adj_matrix)
print(cost_matrix)
print(result)

    
#정방행렬이 아닌 경우 해당 데이터 삭제
if adj_matrix.shape != cost_matrix.shape :
    if adj_matrix.shape[0] < cost_matrix.shape[0] :
        del result[cost_matrix.shape[0]-1]
    else :
        for k, v in result.items():
            if v == cost_matrix.shape[1]-1 :
                del result[k]
                break
