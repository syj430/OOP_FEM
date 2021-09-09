from PRE_rev2 import *
from assembly import *

data = INPUT().read_file("Q4_250.inp")  # inp파일 데이터 불러오기
# data = INPUT().read_file("tens.inp")  # inp파일 데이터 불러오기
enriched_data = PRE().categorize(data)  # 불러온 데이터 가공
print(enriched_data)

assem = ASSEMBLY()
solve = SOLVE()
output = OUTPUT()

assem.getNode(enriched_data)
assem.getElement(enriched_data)
assem.getBoundary(enriched_data)
assem.getLoad(enriched_data)
assem.showSparseMatrix(enriched_data)

solve.displacement(enriched_data)
solve.stress(enriched_data)

output.visual(enriched_data)



# assem.assembleGlobalStiff(enriched_data)






