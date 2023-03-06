# "돼지고기 등급 분류 모델 구현"

진행 기간 : 2022. 11. 21 ~ 2022. 12. 03

주제 : 도축된 돼지고기의 이미지를 통해 등급을 분류하는 최적의 모델을 찾는다. 

## 진행 순서

1. 데이터 수집
(AIHub "축산물 품질(QC) 이미지" 데이터 : 
https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=116&topMenu=100&aihubDataSe=ty&dataSetSn=158)

2. 전처리 (및 증강)

3. 모델링 (CNN 모델 적용)
* epoch 변경 비교
* 데이터 증강 정도에 따른 비교
* 데이터셋 크기에 따른 비교

4. 결과 분석 및 정리
* 결과를 Complex Matrix로 제시(1+, 1, 2 Label)
* log-loss (cross-entropy) 그래프 제시
* 평가지표 그래프 제시 (Accuracy or ROC curve)
* 어려웠던 점, 개선사항 제시

5. ppt 작성, 발표 스크립트 작성 후 발표



## 레이블 (돼지고기 등급)
* 1+
* 1
* 2

## 사용한 딥러닝 모델
* ResNet 50 / 101 / 152
* EfficientNet V2L / V2S
* Sequential (테스트 모델로 사용)



## 참고문헌
* 한준희, 정성훈, 박경수 and 유태선. (2021). 딥러닝 이미지 인식 기술을 활용한 소고기 등심 세부 부위 분류. 한국산업경영시스템학회지, 44(3), 1-9.

* [축산물 등급판정 세부기준 [시행 2020. 12. 29.] [농림축산식품부고시 제2020-112호, 2020. 12. 29., 일부개정] 농림축산식품부(축산정책과)](https://www.law.go.kr/%ED%96%89%EC%A0%95%EA%B7%9C%EC%B9%99/%EC%B6%95%EC%82%B0%EB%AC%BC%20%EB%93%B1%EA%B8%89%ED%8C%90%EC%A0%95%20%EC%84%B8%EB%B6%80%EA%B8%B0%EC%A4%80)
* [“돼지고기 등급기준 개선” 한목소리. 농민신문 박하늘 기자. 입력 : 2021-04-16 00:00 수정 : 2021-04-15 16:01](https://www.nongmin.com/news/NEWS/ECO/COW/336724/view)
* [고기의 등급 - 한돈의 등급체계 (네이버 블로그)](https://m.blog.naver.com/mornifarm/221386184976)
