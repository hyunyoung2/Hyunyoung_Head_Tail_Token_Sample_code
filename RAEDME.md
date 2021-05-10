## Head-tail Tokenization for Korean

This code preprocessing into head-tail token for head-tail tokenizer of Korean

For what is the head-tail in Korean, visit this site, https://cafe.naver.com/nlpk

This code depends on corupus type from https://github.com/bufsnlp2030/BUFS-JBNUCorpus2020

The Korean data format is as follows:

```
# sent_id = 1
# file = 00000
# text = 현재 사회적 대타협을 통해서 노동시장 구조를 개선하기 위해 노사정이 머리를 맞대고 노력하고 있는데 3월 말까지 좋은 합의안을 만들어 주실 것이라고 기대하고 있다 .
1	현재	현재	ADV	MAG	_	4	AP	_	_
2	사회적	사회적	DET	MM	_	3	NP	_	_
3	대타협을	대타협+을	NOUN	NNG+JKO	_	4	NP_OBJ	_	_
4	통해서	통하+어서	VERB	VV+EC	_	7	VP	_	_
5	노동시장	노동시장	NOUN	NNG	_	6	NP	_	_
6	구조를	구조+를	NOUN	NNG+JKO	_	7	NP_OBJ	_	_
7	개선하기	개선하+기	VERB	VV+ETN	_	8	VP_OBJ	_	_
8	위해	위하+어	VERB	VV+EC	_	11	VP	_	_
9	노사정이	노사정+이	NOUN	NNG+JKS	_	11	NP_SBJ	_	_
10	머리를	머리+를	NOUN	NNG+JKO	_	11	NP_OBJ	_	_
11	맞대고	맞대+고	VERB	VV+EC	_	12	VP	_	_
12	노력하고	노력하+고	VERB	VV+EC	_	13	VP	_	_
13	있는데	있+는데	AUX	VX+EC	_	18	VP	_	_
14	3월	3+월	NUM	SN+NNB	_	15	NP	_	_
15	말까지	말+까지	NOUN	NNB+JX	_	18	NP_AJT	_	_
16	좋은	좋+은	ADJ	VA+ETM	_	17	VP_MOD	_	_
17	합의안을	합의안+을	NOUN	NNG+JKO	_	18	NP_OBJ	_	_
18	만들어	만들+어	VERB	VV+EC	_	19	VP	_	_
19	주실	주+시+ㄹ	AUX	VX+EP+ETM	_	20	VP_MOD	_	_
20	것이라고	것+이+라고	VERB	NNB+VCP+EC	_	21	VNP_CMP	_	_
21	기대하고	기대하+고	VERB	VV+EC	_	22	VP	_	_
22	있다	있+다	AUX	VX+EF	_	23	VP	_	_
23	.	.	PUNC	SF	_	0	NP	_	_
```

if you want to implement run, run as follows:

```
python3 data_preprocessing.py
```

The result will generate under des_data directory
