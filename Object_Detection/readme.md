프로젝트 진행기간 : 2022. 12. 07 ~ 2022. 12. 16

## 개요 및 주제 선정 배경

카페에서 사용하는 일회용품 인식 모델 구현


#### 주제 선정 배경 : 

[환경부 일회용품 규제 (2022.11.24)](http://me.go.kr/home/web/board/read.do?boardMasterId=1&boardId=1557410&menuId=10525)

[일회용품의 종류에 따른 주별 평균 사용량](https://scienceon.kisti.re.kr/srch/selectPORSrchReport.do?cn=TRKO201900000681)을 바탕으로 가장 빈번하게 사용되는 카페의 일회용 컵을 아이템으로 선정.
카페 매장 내에서 사용되는 플라스틱/종이 일회용 컵과 빨대를 인식함으로써 본 규제가 잘 시행되는지 확인하는 데 도움이 되는 프로그램을 구현하고자 함.

### 구현 예시

![](https://velog.velcdn.com/images/deepshadow/post/789aa901-c695-49df-ae74-62fbb9133f95/image.png)

Image Detection 방식을 이용하여 위와 같이 컵과 빨대를 인식할 수 있게끔 설정.
카페 매장 내 cctv에 찍힌 이미지 데이터를 프로그램에 넣으면 매장 내 일회용품 여부를 확인할 수 있게 함.


### 사용한 모델
* YOLOv4 custom (darknet)



## 데이터 수집 및 전처리

### 데이터 수집

1차 : roboflow의 [TACO 데이터셋](https://universe.roboflow.com/mohamed-traore-2ekkp/taco-trash-annotations-in-context)을 참조하여 데이터를 수집하고 라벨링하기로 함.

데이터 수집 방법 : 
상기된 roboflow TACO 데이터셋을 비롯한 roboflow 데이터셋 활용
또는 Google Chrome의 [크롤링 도구](https://chrome.google.com/webstore/detail/fatkun-batch-download-ima/nnjjahlikiabnchcpehcpkdeckfgnohf?hl=ko) [확장 프로그램](https://chrome.google.com/webstore/detail/zzllrr-imager-lite/bedbigoemkinkepgmcmgnapjcahnedmn?hl=ko) 활용.
키워드 검색* 을 통해서 Naver, Google, GettyImages, Pinterest, iClickart 등 각종 사이트의 이미지를 크롤링.

\* *한글 키워드 '카페 일회용품 규제', '카페 테이크아웃 컵', '카페 플라스틱 컵' 등...*
\* *알파벳(영어) 키워드 'cafe high angle', 'cafe ice cup', 'plastic straw' 등...*

2차 : 라벨을 일회용품 규제대상(플라스틱 컵, 종이컵, 플라스틱 빨대)와 비교군(유리컵, 머그컵, 텀블러, 종이 빨대)로 나누어 설정하고, 관련된 데이터를 수집 
한 라벨당 최소 500개 이상의 Bounding Box 생성을 목표로 함.

3차 : 라벨을 정한 뒤, 수집한 데이터를 roboflow workspace에 업로드. 업로드한 이미지 각각의 객체에 직접 Bounding Box를 지정.

**Bounding Example**

![](https://velog.velcdn.com/images/deepshadow/post/b421c9b7-5ada-4f3d-9773-7464cd26ced8/image.png)
![](https://velog.velcdn.com/images/deepshadow/post/9ccc3ad7-3f9f-471e-9f40-78b9dbaad5dc/image.png)



4차 : 데이터를 학습시킨 뒤 모델을 시험하여 mAP (Mean Average Precision)을 기준으로 모델의 성능 평가.
데이터셋을 분석하여 라벨링 수정, 이미지 수집 기준 강화, 이미지 사이즈 조절, 이미지 종류 변경* 으로 인한 이미지 재수집 등의 데이터 정제 과정을 시행

\* *컵/빨대가 크게 찍힌(큰 객체, 좁은 이미지)에서 cctv 사진(넓은 이미지, 작은 객체)로 변경하여 이미지 재수집.*

5차 : 위 과정을 성능(mAP 기준)이 최대한 향상되도록 반복하여 시행



#### 최종 데이터셋 : 이미지 1,867장 
일회용품 규제대상 : 플라스틱 컵 702개, 종이컵 1,016개, 빨대 775개 
일회용품 비교군 : 유리컵 748개, 머그컵 777개


#### Label 분류

초기 레이블 (from TACO Dataset)
- 11 Disposable plastic cup
- 33 Other plastic cup
- 34 Other plastic wrapper
- 36 Paper cup
- 37 Paper straw
- 42 Plastic lid
- 43 Plastic straw
- 45 Polypropylene bag

최종 레이블
- cup_plastic
- cup_glass
- cup_paper
- cup_mug
- straw


## 모델 시행 과정
![](https://velog.velcdn.com/images/deepshadow/post/d6067c44-a258-477b-b311-6d8684a68874/image.jpg)

총 14차 시행.

#### 1차, 2차 시행 

* 1차시행  
![](https://velog.velcdn.com/images/deepshadow/post/94c5e841-5d0e-4c4a-b425-e6d37b23320a/image.png)
* 2차시행
![](https://velog.velcdn.com/images/deepshadow/post/0ce2355d-3869-4a4e-99bb-eb94f58c3dcb/image.png)
컵과 빨대를 잘 Detection할 수 있는지에 초점을 맞춤.

일회용 컵과 빨대 종류를 확인.

2차시행 : rotation augmentation 추가실행, 이미지 사이즈 증가
* 문제점 및 해결방안 
 모든 컵을 종류불문 Disposable로 인식 - 비교군 설정으로 해결
 빨대 종류 구별이 어려움 - 빨대 라벨은 한종류로 통일, 빨대 객체 사이즈 키우기
 2차시행시 mAP가 대폭 하락 : 불필요한 증강 및 데이터셋의 정제가 온전치 않았음. 
- 증강을 하지 않고, 기본적인 데이터 핸들링에 집중하기로 함.
 
 
#### 3차 시행

![](https://velog.velcdn.com/images/deepshadow/post/c4fde389-2f50-4401-8c73-33e87d5280bc/image.png)
* 빨대 라벨 하나로 합침. 
* 컵을 일회용품(paper, plastic)과 비교군(glass, tumbler, mug)으로 나누고, 컵 라벨을 5가지로 세분화.
* 문제점 및 해결방안
텀블러의 AP가 유독 낮았음 - 이미지에서 쉽게 판독 가능, 라벨이 지나치게 많다고 판단하여 텀블러 라벨 삭제
객체가 클수록 인식 성능 오름 - cctv 이미지에서도 성능을 좋게 하기 위해 이미지 사이즈를 늘려야 할 것으로 정함.

#### 4차, 5차 시행
* 4차시행 ![](https://velog.velcdn.com/images/deepshadow/post/52b09cb2-6a1b-4297-a196-ad33b6b84266/image.png)
* 5차시행 ![](https://velog.velcdn.com/images/deepshadow/post/b86cfa57-2bee-4c97-bfca-cb1e94458295/image.png)텀블러 라벨 삭제, 약간의 데이터 핸들링을 거친 후, 이미지 사이즈를 608 x 608, 416 x 416 으로 나누어 비교하기로 함.
* 문제점 및 해결방안
mAP는 개선되었으나, 실제 test 결과 배경에 객체가 있는 것으로 인식하거나 인식하지 못함 - **test 사이즈를 학습시킨 이미지 사이즈와 같게 맞춰주지 않았음.**
빨대(straw)의 AP가 다른 라벨들에 비해 유독 낮음 - 빨대 객체의 Bounding Box 형태가 크게 차이나는 것 때문으로 파악. 빨대 라벨을 제거하고 진행해 보기로 함.

#### 6, 7, 8 차 시행 
: 라벨 이진분류 test(disposable vs reusable)
라벨분류와 데이터셋 정제를 위한 단순 test 분류임.

#### 9차, 11차 시행
* 9차시행 ![](https://velog.velcdn.com/images/deepshadow/post/ac886000-34aa-4d99-bf46-ac64efeddcd2/image.png)
* 11차시행 ![](https://velog.velcdn.com/images/deepshadow/post/1c10044c-3bfd-4f1a-aa7d-d2d7df3ab9b8/image.png)

라벨 이진분류 test, 데이터 재수집 및 핸들링 진행
이미지 size가 416 x 416일 때보다 608 x 608일 때 mAP가 향상됨을 확인 - 이미지 size는 608 x 608로 정함.

#### 10차, 12차 시행
* 10차시행 ![](https://velog.velcdn.com/images/deepshadow/post/6e7cebd2-79c7-4266-a592-1e70c85b474b/image.png)9차시행과 동일한 데이터로 수행. 
프로젝트 목적에 좀 더 부합한 데이터셋을 구축하기 위해 라벨을 4가지로 세분화시키고 모델을 구동시킴.
* 12차시행 ![](https://velog.velcdn.com/images/deepshadow/post/605016d7-b1f3-4745-ac2b-dc82404c9712/image.png)
프로젝트 목적에 맞도록 빨대 라벨 다시 추가
빨대 라벨의 AP가 여전히 낮음 - 빨대 라벨 데이터를 비롯해 전반적인 데이터의 양을 늘리기로 함.

#### 13차 시행
![](https://velog.velcdn.com/images/deepshadow/post/b02fc553-f69b-4d6a-9e2e-da3f9830f402/image.png)라벨별 객체 개수를 라벨당 최소 700개로 잡음. - 라벨별 AP가 대체로 향상되는 것 확인.

#### 14차 (최종) 시행
![](https://velog.velcdn.com/images/deepshadow/post/9b5a57af-69ae-4bcb-beff-1bf56a82196f/image.png)
* 이미지 데이터, 라벨 별 객체 개수 추가
* Mosaic Augmentation 수행 (from roboflow)
mAP를 상용화 수준(over 80%)까지 끌어올릴 수 있었음.
* 14차 시행의 loss-mAP 그래프 ![](https://velog.velcdn.com/images/deepshadow/post/4d4e3b75-3440-4b31-8c15-e66ebeaf04e5/image.png)
* 14차 시행 실제 test 적용 결과 ![](https://velog.velcdn.com/images/deepshadow/post/cd5d60d4-9457-410d-85a1-f12974c189e3/image.png)

### 남은 문제점 및 해결방안
* 빨대의 종류, 유리컵과 플라스틱컵을 혼동하기 쉽다 - 추가 테스트 및 실제 상용화를 거쳐 데이터를 지속적으로 추가 수집하며 성능 개선을 할 수 있을 것으로 기대.
* 실제 이미지로 test한 결과가 (아래 그림과 같이) 예상보다 부정확함 
* ![](https://velog.velcdn.com/images/deepshadow/post/f40fd169-9fad-4c4b-90ce-247da350b24b/image.png) 
  - 객체의 질감 요소 등 추가 정보를 주어 데이터를 개선할 수 있을 것으로 판단.

## 활용 계획 및 기대 효과

### 활용 계획
1. cctv 영상 1200 frame 단위로 나누어 이미지 저장
2. 1시간 당 3장, 12시간 영업시 36장 -> 한달 1,000장 이상
3. 본 프로젝트에서 구축한 프로그램을 사용하여 매장 내 일회용품 사용량을 계산 후 분류, 실제 단속 시 참조

### 기대 효과
1. 현장 감독 인원을 최소화하여 노동력의 낭비를 막음.
2. 이를 바탕으로 단속의 효율을 높여 일회용품 쓰레기 배출량 감소 촉진, 제도의 실효성을 확대시킬 수 있음.
3. 상용화를 통한 프로그램의 검증으로 다른 업종에도 적용하거나 프로그램을 해외에 수출하여 추가 수익을 얻을 수 있을 것으로도 기대됨.
4. 지속적인 학습으로 프로그램을 꾸준히 개선하여, 2024년 [UN 플라스틱 규제 협약안](https://wedocs.unep.org/bitstream/handle/20.500.11822/38522/k2200647_-_unep-ea-5-l-23-rev-1_-_advance.pdf?sequence=1&isAllowed=y)에 제안 가능

