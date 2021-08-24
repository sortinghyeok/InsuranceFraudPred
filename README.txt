Modeling_Analysis
--------------------
InsuranceData.csv에 대하여 세 가지 모델을 적용해보았을 때, 세가지 모델에 대하여 성능상에서는
큰 차이가 없었다. 그러나 LogisticRegression모델의 경우 y/n 결과값을 분류할 때에 해당 target일 확률을 구해주는
내장함수가 존재하고, 이번 프로젝트의 목적에 부합하다고 판단하였음
또한 샘플링 방법의 경우, target data에서 y와 n의 개수 차이가 심하다고 판단된 바 overfitting의 문제를 해결하기
위하여 오버샘플링, 언더샘플링의 여러 기법을 적용해보았음. 그 결과, SVMSmote 방식의 oversampling이 적합하다고
판단됨