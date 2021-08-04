# terminal : !pip3 install pandas

import pandas as pd

custDF = pd.read_csv("customer_data.csv",  sep=',', encoding = 'utf-8', error_bad_lines=False, engine = 'python', header = None, names=['CUST_ID', 'DIVIDED_SET', 'SIU_CUST_YN', 'SEX', 'AGE', 'RESI_COST', 'RESI_TYPE_CODE', 'FP_CAREER', 'CUST_RGST', 'OCCP_GRP', 'TOTALPREM', 'WEDD_YN', 'MATE_OCCP_GRP', 'CHLD_CNT', 'LTBN_CHLD_AGE', 'MAX_PAYM_YM', 'MAX_PRM'])
#쉼표 구분이므로 구분자 ',', encoding방식 utf-8 고정, 라인 에러시 무시, 파이썬 엔진 사용으로 파싱, 헤더 미지정(컬럼명 별도 입력)
#csv파일 로딩시 별 문제 없으면 columns명 지정 필요 없이 첫 행을 columns로 바꾸면 됨 ex)df2 = df1.rename(columns=df1.iloc[0])
#알 수 없는 이유로 인해 첫 행이 단 하나의 value로 고정되고 나머지 17개의 데이터가 1개의 컬럼에 의해 종속되는 상황이 발생하여 개별 컬럼명 입력으로 컬럼 분할

#첫번째 행 (cust_id, divided_set, ....) 등이 컬럼 하나로 압축되어 cust_id하나만 등록되는 문제 발생. 컬럼 명을 위에서 수동 기입 후 삭제
custDF = custDF.drop(custDF.index[0])

#결측치 개수 확인
custDF.isnull().sum()

#AGE columns 내부 values를 몇십대인가의 기준으로 정수형 값 변환 함수. ex) 15 -> 10, 26 -> 20
custDF['AGE'] = (custDF['AGE']/10).astype(int)
#float값에서 10으로 나눈 후 정수형으로 바꿔주어 소숫점 제거
custDF['AGE']

#-------------------------------------------------------------

#중앙값으로 RESI_COST 컬럼 결측치 대체 가능(결측치 없으므로 실행 안함)
#custDF['RESI_COST'].fillna(custDF['RESI_COST'].median)

#-------------------------------------------------------------

#456개의 CUST_RGST 컬럼에 대해 ROW 제거로 결측치 제거
#dropna는 동일 주소를 이용하는 것이 아니므로 초기화 필요
#inplace = True란 결측치 제거와 동시에 오리지널 데이터에 적용해주는 boolean param
custDF.dropna(subset = ['CUST_RGST'], inplace= True)

#결측치 개수 확인
#CUST_RGST 결측치 제거 확인
custDF.isnull().sum()

#Year는 기존 6자리 수에서 100을 나눠 4자리 수 float으로 만든 다음 정수형 형변환으로 소수점 삭제
Year = (custDF['CUST_RGST']/100).astype(int)
#Month는 적절한 산술 적용으로 달만 분리
Month = (custDF['CUST_RGST']-Year*100).astype(int)
#String 사용해서 index기준 parsing도 가능할 것

#-------------- 직업별 정수형 라벨링 ---------------------------
# 결측치 포함 행 삭제
#사무직 1
#자영업 2
#주부 3
#교사 4
#예체능계 종사자 5
#운전직 6
#1차산업 종사자 7
#2차산업 종사자 8
#3차산업 종사자 9
#공무원 10
#고위 공무원 11
#단순 노무직 12
#기업/단체 임원 13
#고소득의료직 14
#전문직 15
#종교인/역술인 16
#대학교수/강사 17
#단순 사무직 18
#교육관련직 19
#학자/연구직 20
#학생 21
#법무직 종사자 22
#고소득 전문직 23
#의료직 종사자 24
#기타 25

#직업 추출에 사용된 출력문
#개선된 변수 확인 알고리즘 아이디어 있으신 분은 알려주시길(혹은 액셀 함수라도)
#for i in custDF['OCCP_GRP']:
  #if i != '의료직 종사자' and i != '고소득 전문직' and i != '사무직' and i != None and i!='자영업' and i!='주부' and i!='교사' and i!='예체능계 종사자' and i!='운전직' and i!='1차산업 종사자' and i!='2차산업 종사자' and i!='3차산업 종사자' and i!='공무원' and i!='고위 공무원' and i!='단순 노무직' and i!='기업/단체 임원' and i!='고소득의료직' and i!='전문직' and i!='종교인/역술인' and i!='대학교수/강사' and i!='단순 사무직' and i!='교육관련직' and i!='학자/연구직' and i!='학생' and i!='법무직 종사자' and i!='기타' :
    #print(i)

#위 주석과 대응하는 정수형 라벨링(이 단계에서는 type casting 아직 안함)
custDF['OCCP_GRP'].replace('사무직', 1, inplace = True)
custDF['MATE_OCCP_GRP'].replace('사무직', 1, inplace = True)

custDF['OCCP_GRP'].replace('자영업', 2, inplace = True)
custDF['MATE_OCCP_GRP'].replace('자영업', 2, inplace = True)

custDF['OCCP_GRP'].replace('주부', 3, inplace = True)
custDF['MATE_OCCP_GRP'].replace('주부', 3, inplace = True)

custDF['OCCP_GRP'].replace('교사', 4, inplace = True)
custDF['MATE_OCCP_GRP'].replace('교사', 4, inplace = True)

custDF['OCCP_GRP'].replace('예체능계 종사자', 5, inplace = True)
custDF['MATE_OCCP_GRP'].replace('예체능계 종사자', 5, inplace = True)

custDF['OCCP_GRP'].replace('운전직', 6, inplace = True)
custDF['MATE_OCCP_GRP'].replace('운전직', 6, inplace = True)

custDF['OCCP_GRP'].replace('1차산업 종사자', 7, inplace = True)
custDF['MATE_OCCP_GRP'].replace('1차산업 종사자', 7, inplace = True)

custDF['OCCP_GRP'].replace('2차산업 종사자', 8, inplace = True)
custDF['MATE_OCCP_GRP'].replace('2차산업 종사자', 8, inplace = True)

custDF['OCCP_GRP'].replace('3차산업 종사자', 9, inplace = True)
custDF['MATE_OCCP_GRP'].replace('3차산업 종사자', 9, inplace = True)

custDF['OCCP_GRP'].replace('공무원', 10, inplace = True)
custDF['MATE_OCCP_GRP'].replace('공무원', 10, inplace = True)

custDF['OCCP_GRP'].replace('고위 공무원', 11, inplace = True)
custDF['MATE_OCCP_GRP'].replace('고위 공무원', 11, inplace = True)

custDF['OCCP_GRP'].replace('단순 노무직', 12, inplace = True)
custDF['MATE_OCCP_GRP'].replace('단순 노무직', 12, inplace = True)

custDF['OCCP_GRP'].replace('기업/단체 임원', 13, inplace = True)
custDF['MATE_OCCP_GRP'].replace('기업/단체 임원', 13, inplace = True)

custDF['OCCP_GRP'].replace('고소득의료직', 14, inplace = True)
custDF['MATE_OCCP_GRP'].replace('고소득의료직', 14, inplace = True)

custDF['OCCP_GRP'].replace('전문직', 15, inplace = True)
custDF['MATE_OCCP_GRP'].replace('전문직', 15, inplace = True)

custDF['OCCP_GRP'].replace('종교인/역술인', 16, inplace = True)
custDF['MATE_OCCP_GRP'].replace('종교인/역술인', 16, inplace = True)

custDF['OCCP_GRP'].replace('대학교수/강사', 17, inplace = True)
custDF['MATE_OCCP_GRP'].replace('대학교수/강사', 17, inplace = True)

custDF['OCCP_GRP'].replace('단순 사무직', 18, inplace = True)
custDF['MATE_OCCP_GRP'].replace('단순 사무직', 18, inplace = True)

custDF['OCCP_GRP'].replace('교육관련직', 19, inplace = True)
custDF['MATE_OCCP_GRP'].replace('교육관련직', 19, inplace = True)

custDF['OCCP_GRP'].replace('학자/연구직', 20, inplace = True)
custDF['MATE_OCCP_GRP'].replace('학자/연구직', 20, inplace = True)

custDF['OCCP_GRP'].replace('학생', 21, inplace = True)
custDF['MATE_OCCP_GRP'].replace('학생', 21, inplace = True)

custDF['OCCP_GRP'].replace('법무직 종사자', 22, inplace = True)
custDF['MATE_OCCP_GRP'].replace('법무직 종사자', 22, inplace = True)

custDF['OCCP_GRP'].replace('고소득 전문직', 23, inplace = True)
custDF['MATE_OCCP_GRP'].replace('고소득 전문직', 23, inplace = True)

custDF['OCCP_GRP'].replace('의료직 종사자', 24, inplace = True)
custDF['MATE_OCCP_GRP'].replace('의료직 종사자', 24, inplace = True)

custDF['OCCP_GRP'].replace('기타', 25, inplace = True)
custDF['MATE_OCCP_GRP'].replace('기타', 25, inplace = True)

#직업 관련 2개 컬럼 결측치 제거
custDF.dropna(subset = ['OCCP_GRP', 'MATE_OCCP_GRP'], inplace= True)

#직업 관련 2개 컬럼 type casting
custDF['OCCP_GRP'] = custDF['OCCP_GRP'].astype(int)
custDF['MATE_OCCP_GRP'] = custDF['MATE_OCCP_GRP'].astype(int)

#결측치 제거 완료 확인
custDF.isnull().sum()

#1000만단위 라벨링 (ex)176만 -> 0, 1700만 -> 1, 3억 -> 30 ...)
custDF.dropna(subset = ['TOTALPREM'], inplace = True)
custDF['TOTALPREM'] = (custDF['TOTALPREM']/10000000).astype(int)

#WEDD_YN, RESI_TYPE_CODE에 대하여 결측치 삭제
custDF.dropna(subset = ['WEDD_YN'], inplace = True)
custDF.dropna(subset = ['RESI_TYPE_CODE'], inplace = True)

#결측치 제거 완료 확인
custDF.isnull().sum()

#MAX_PAYM_YM 결측치 ROW제거
custDF.dropna(subset = ['MAX_PAYM_YM'], inplace = True)

#MAX_PAYM_YM에 관한 최대 보험료 연월을 2개 컬럼으로 분리
#분리 방법은 위 연월 분리 메소드와 동일
Year = (custDF['MAX_PAYM_YM']/100).astype(int)
Month = (custDF['MAX_PAYM_YM']-Year*100).astype(int)

#새 컬럼 추가 후 데이터 삽입
custDF['MAX_PAYM_YEAR'] =  Year
custDF['MAX_PAYM_MONTH'] = Month

#컬럼 분리 완료했으므로 오리지널 컬럼 삭제
custDF.drop(['MAX_PAYM_YM'], axis=1, inplace = True)

custDF.isnull().sum()

#월 최대 납입 보험료는 결측치 없는 것으로 확인됨

#월 최대 납입 보험료 10만단위 라벨링, 메소드는 위 범위 기반 라벨링 코드와 동일
custDF['MAX_PRM'] = (custDF['MAX_PRM']/100000).astype(int)

#Test, train set으로 분리할 SIU_CUST_YN 제외 모든 결측치 제거된 것 최종 확인
custDF.isnull().sum()

#csv파일로 변환
custDF.to_csv('ProcessedCustData.csv')