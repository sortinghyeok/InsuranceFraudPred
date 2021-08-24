# 보험사의 효율적인 운영을 위한 예측 모델 개발
데이터 청년 캠퍼스 프로젝트 1조

개발기간 : 2021/08/02 ~ 2021/08/27

Notion Link : https://nervous-stranger-60b.notion.site/Insurance-Fraud-Prediction-9a9d4408c8c64753afa16497aec26d60

## 보험 사기 현황 & 프로젝트 목적
금융감독원 자료에 따르면 2015년도 이후 보험사기 건수는 꾸준히 증가하였다. 

특히, 2020년도부터 코로나 바이러스 판데믹 이후에는 보험사기 금액이 급격히 증가하였음을 확인할 수 있었다.

이러한 상황에서 각종 증권사는 머신러닝 기술을 접목한 보험사기 예측 시스템을 개발하였으며, 대표적인 예로는 교보생명의 K-FDS, KB손해보험의 SMA 시스템 등이 있다.

그러나 기존 보험사의 예측 시스템에는 보험금을 받아야할 소비자를 사기자로 진단하는 등 시스템에 대한 신뢰도가 떨어지는 문제가 있다.

따라서 이번 프로젝트는 사기 여부에 대한 예측을 확률로 나타내어 보완하고, 보험사가 고객을 관리함에 있어 더 효율적인 운영을 할 수 있도록 예측모델을 구축하는 데에 개발 목적을 둔다.

## 데이터 소개
Raw_Data 폴더 내부의 4개의 데이터 셋 파일은 각각 보험사 가입 회원정보(CUST), 고객별 청구(CLAIM), 보험설계사 관련 데이터(FPINFO), 보험 계약 관련 데이터(CNTT)이다.

이들의 정제를 위하여 인코딩 방식을 UTF-8로 맞추고, CSV파일로 변환한 것이 Converted_Data 폴더 내부 컨텐츠이다. 폴더 내부 각 파일에 대응하는 내용은 RAW_DATA와 같다.

정제 과정에 있어 첫번째 목표는 분석에 가장 용이한 최적의 데이터 셋을 산출하는 것이었다. 모든 데이터셋의 컬럼을 합치게 되면 70개 이상의 컬럼이 존재하게 되고, 이렇게 과한 수의 컬럼은 데이터 분석을 용이하게 하지 못하는 문제를 야기하였다. 

때문에, 우리는 1. CNTT + CUST + FPINFO 병합본, 2. CUST + CLAIM 병합본, 3. 전 데이터 셋 병합본으로 나누어 정제를 진행하였다. (이들과 관련된 코드 및 전처리 후 CSV파일은 Data_Processing branch에서 확인할 수 있다.)

각 전처리된 데이터셋의 컬럼 정보와 유효 컬럼은 아래와 같다.

### Cust + Claim
----------------------------
CUST_ID : 고객의 고유 아이디이다. 병합의 PK로서 역할을 하며, 분석용 데이터 셋에서 고유하다.

SIU_CUST_YN : 보험사기자 여부이며, 분석 과정에 있어 Target Data가 된다. 1 : Y, 2 : N의 binary형태 데이터이며, 지도 학습에 있어 가장 중요한 역할을 하게 된다.

SEX : 고객의 성별. 1 : MALE, 2 : FEMALE

AGE : 고객의 나이

FP_CAREER : 고객의 보험설계사 이력 여부

MAX_PRM : 최대 보험료, 당사에 최대 규모 보험료를 납입한 월 보험료 수준으로, 10만 단위로 1씩 누계

RESL_CD1 : 보험 사고에 대한 결과 코드

ACCI_OCCP_GRP : 보험 청구자의 직업 코드

CHME_LICE_NO : 대표 담당의사면허번호

DMND_AMT : 사고보험금청구금액

PAYM_AMT : 실지급금액

NON_PAY_RATIO : 실손비급여비율

HEED_HOSP_YN : 유의병원여부

CLAIM_CNT : 보험 청구 건수

TOTAL_VLID_HOSP_OTDA : 유효입원 및 통원일수의 합

HOSP_VARIES : 보험 청구건에 대하여 다닌 병원의 갯수

HOSP_DVSN_VARIES : 보험 청구건에 대하여 다닌 병원의 종류 구분 누계

CHME_LICE_COUNT : 담당의사 면허 건수

-------------------------------------------

상관분석 결과
------------------------------------

![image](https://user-images.githubusercontent.com/80696846/130572167-9d5b6d11-7451-4dc8-b90c-d185fb829b8d.png)
상관분석 결과를 보면, SIU_CUST_YN과 CLAIM_CNT, TOTAL_VLID_HOSP_OTDA, HOSP_VARIES, HOSP_DVSN_VARIES, CHME_LICE_COUNT가 유효하게 관련있는 컬럼임을 확인할 수 있다.

다중회귀분석 결과
------------------------------------

![image](https://user-images.githubusercontent.com/80696846/130572245-944178e1-1a39-493a-aca9-c4a99a33f4d4.png)
다중회귀분석 결과를 보면, MINCRDT, CAUS_CODE, CLAIM_CNT, TOTAL_VLID_HOSP_OTDA, HOSP_VARIES, HOSP_DVSN_VARIES, CHME_LICE_COUNT 등이 유효한 컬럼임을 확인할 수 있다.

RandomForest 변수중요도 분석 결과
------------------------------------

![image](https://user-images.githubusercontent.com/80696846/130572377-f86ef01d-8387-45e3-a213-d4eace94b33f.png)
Random Forest의 변수중요도 분석 결과로부터 CLAIM_CNT, TOTAL_VLID_HOSP_OTDA, HOSP_VARIES, HOSP_DVSN_VARIES, CHME_LICE_COUNT, HEED_HOSP_YN, NON_PAY_RATIO 등이 유효한 컬럼임을 확인할 수 있다.

------------------------------------------------------------------------------------------------

위 결과를 종합한 경우, 아래와 같은 5개의 컬럼이 세 가지 분석법 모두에서 공통적으로 보험사기자 여부와 상대적으로 높은 관련성을 보였다.
1. CHME_LICE_COUNT
2. HOSP_DVSN_VARIES
3. HOSP_VARIES
4. TOTAL_VLID_HOSP_OTDA
5. CLAIM_CNT

### Cust + CNTT + FPINFO
----------------------------
CLLT_FP_PRNO : FP 사번

INCB_DVSN : 재직 구분

CUST_ID : 고객의 ID로, PK로서 고유한 값을 가진다.

DIVIDED_SET : 데이터 셋의 구분, TEST OR TRAIN SET이냐에 따라 구분되며, 분석시에 제거될 가능성 있음

SIU_CUST_YN : 보험사기 여부로, 분석시의 Target Data으로 binary형 데이터

SEX : 고객의 성별(1 : male, 2 : female)

AGE : 고객의 나이

FP_CAREER : FP경력 여부를 의미

OCCP_GRP : 직업 그룹코드

TOTALPREM : 현재까지 납입한 총 보험료

WEDD_YN : 결혼 여부

MAX_PAYM_YEAR : 최대 보험료를 납입한 연도

MAX_PAYM_MONTH : 최대 보험료를 납인한 월

MAX_PRM : 당사에 최대규모의 보험료를 납입했던 월보험료 수준

RGST_MONTH : 고객등록월

RGST_YEAR : 고객등록연도

MNTH_INCM_AMT_AVG : 청약서 소득 평균

MAIN_INSR_AMT_SUM : 주보험금 합계

SUM_ORIG_PREM_SUM : 계약(주계약 + 특약)의 전체 보험료

EXPR_SUM : 종신 보험료의 합계

CNTT_TERM_AVG : 평균 계약 소요일

WORK_YEARS_MAX : 최대근무연수

WORK_YEARS_MIN : 최소근무연수

EXPR_COUNT : 종신보험개수

-------------------------------------------

상관분석 결과
------------------------------------

![image](https://user-images.githubusercontent.com/80696846/130634594-eafc255d-ee5a-4d56-9dfc-1c4b5c4818cf.png)

상관분석 결과를 보면, SIU_CUST_YN과 유의미하다고 볼 수 있는 컬럼이 아예 존재하지 않는다.

다중회귀분석 결과
------------------------------------
### 설명력(0 < R-Squred < 1) 분석

R-squared	0.016	매우 약한 설명력

Adj. R-squared	0.015	매우 약한 설명력

F-statistic	14.3	

Prob (F-statistic)	3.53e-23	

Log-Likelihood	-1429.4	

AIC	2879	

BIC	2948	

### P-VALUE (0.05) 유의 컬럼

SEX	0.0244	3.37	0.001

AGE	0.0084	2.381	0.017

FP_CAREER	0.0444	3.664	0

OCCP_GRP	-0.0017	-2.979	0.003

TOTALPREM	-0.0031	-4.13	0

MAIN_INSR_AMT_SUM	1.02E-10	6.57	0

EXPR_SUM	1.167e-10	-4.521	0

WORK_YEARS_MIN	-0.0013	-2.581	0.01

EXPR_COUNT	0.0029	2.758	0.006

다중회귀분석 결과 위 9개 컬럼에 대해서 유의한 정도의 수치를 산출하였다.

RandomForest 변수중요도 분석 결과
------------------------------------

![image](https://user-images.githubusercontent.com/80696846/130635012-fa1e39df-81f2-4ec7-9ef6-9503ec8346d1.png)
Random Forest의 변수중요도 분석 결과로부터 EXPR_COUNT, WORK_YEARS_MIN, WORK_YEARS_MAX의 세 컬럼 정도가 0.1 이상의 중요도를 보였으나, 이같은 결과로는 Target Data와 깊은 관계가 있는 컬럼이 존재한다고 보기 어려웠다.

------------------------------------------------------------------------------------------------

위 결과를 종합하여, CNTT와 FPINFO 테이블에서는 CUST_ID 상의 SIU_CUST_YN을 구분해내기 어렵다는 결론을 도출하였다.


