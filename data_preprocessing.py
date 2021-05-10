"""
This code preprocessing into head-tail token for head-tail tokenizer of Korean

For what is the head-tail in Korean, visit this site, https://cafe.naver.com/nlpk

This code depends on corupus type from https://github.com/bufsnlp2030/BUFS-JBNUCorpus2020


The Korean data format is as follows:

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
"""

#-*- coding: utf-8 -*-

from glob import glob
import os

ORI_DIR="ori_data/"
DES_DIR="des_data/"

# For Debugging option, increasing level enumerate log in detail
DEBUG_LEVEL = ["DEBUG_LEVEL_0", "DEBUG_LEVEL_1", "DEBUG_LEVEL_2"]
DEBUG = DEBUG_LEVEL[0]


# For lines, 
LINE_OPTS = ["# sent_id", "# file", "# text", ''] # "" means empty string

def read_raw_corpus(path):
    """Reading data line by line from a text file

    Arg:
      path(str): the path to a raw corpus to be read
    return:
      data(list): A list of lines in raw corpus like 
                  ["line1_str", "line2_str", ..., "line_n_str"]
    """

    assert isinstance(path, str), "The type of input is wrong 'read_raw_corpus' function: the type of path is {}, the value is {}".format(type(path), path)


    with open(path, "r") as wr:
        data = [val.strip() for val in wr.readlines()] # to strip the front and back from the text

    if DEBUG in DEBUG_LEVEL[0:]:
        print("\n===== Reading a file of {} =====".format(path))
        print("The number of lines: {}".format(len(data)))
        print("for top 5 of examples, \n{}".format(data[0:50]))

    return data

def separate_into_head_tail_token(word_line):
    """ split a word into a pair of head and tail. 

    format of word_line,  
       
        3\t대타협을\t대타협+을\tNOUN\tNNG+JKO\t_\t4\tNP_OBJ\t_\t_

    The delimeter between columns is 'tap charcter'
   
    Currently, we split the second columns and merge the third column into head-tail token.

    In addition to it, we have to do the same thing in the fifth columsn POS(part-of-speech) 

    Arg: 
       word_line(str): a line of input corpus like 

    Return: 
       new_line(str): new line with additional two column, head_tail token pair and POS according to the head_tail token pair    
    """

    # input data type check 
    assert isinstance(word_line, str), "The type of input is wrong 'separate_into_head_tail_token' function: the type of word_line is {}, the value is {}".format(type(word_line), word_line)

    # the format of input data check 
    assert word_line not in LINE_OPTS, "You data is wrong as input of 'separate_into_head_tail_token' function: the value of word_line is {}".format(word_line)

    list_of_word_line = word_line.split("\t")

    # For first column
    ori_word = list_of_word_line[1]
    len_of_ori_word = len(ori_word)

    # For third column
    temp_token = list_of_word_line[2].split("+")
    len_token = len(temp_token)

    # Head token is dependent of the length of first token
    len_head = len(temp_token[0])

    new_token = ""

    if len_head == len_of_ori_word:
       new_token = ori_word
    elif len_head < len_of_ori_word:
       new_token = "+".join([ori_word[:len_head], ori_word[len_head:]])
##    elif len_head > len_of_ori_word:
##       new_head = ori_word
    ### if more longer than original word, we need dictionary. 
    ### nn+nn+jk 
    elif ori_word in ["이뤄질", "이뤄진", "뭘", "이뤄져", "들춰낸", "나눠져", "뭔"]: # if more longer than original word, we need dictionary.  
       new_token = ori_word
    else:
       assert False, "The length of head morphem is wrong, check you data, the original word:  {}, and mopheme {}".format(ori_word, temp_token)

            
    # For fifth columns
    temp_pos = list_of_word_line[4].split("+")
    len_pos = len(temp_pos)

    new_pos = ""

    if len_pos == 1:
       new_pos = temp_pos[0]
    elif len_token == len_pos:
       if len_of_ori_word == len(new_token):
           new_pos = "_".join(temp_pos)
##       if (temp_token[-1] == "ㄴ" or temp_token[-1] == "ㄹ") and temp_pos[-1] == "ETM":
##           new_pos = "_".join(temp_pos)
       else:
           new_pos = "+".join([temp_pos[0], "_".join(temp_pos[1:])])
    else: 
       assert len_token == len_pos, "The number of POS and Morphem tokens is wrong, check it\n Morpheme: {}\n POS: {}".format(len_token, len_pos)


    assert len(new_token.split("+")) == len(new_pos.split("+")), "The length between new_token and new_pos is wrong, check it\n new token: {}\n new pos{}".format(new_token, new_pos)

    
    temp_out = list_of_word_line[:2] + [new_token] + list_of_word_line[2:4] + [new_pos] + list_of_word_line[4:5] 
    
    ### Test code 
    ###temp_out = list_of_word_line[:2] + [new_token] + list_of_word_line[2:4] + list_of_word_line[4:5]
 
    output = "\t".join(temp_out)

    if DEBUG in DEBUG_LEVEL[2:]:
        print("\n===== head-tail token =====")
        print("The input: {}\n{}".format(type(list_of_word_line), list_of_word_line))
        print("The temp ouput: {}\n{}".format(type(temp_out), temp_out))
        print("The output: {}\n{}".format(type(output), output))

    return output

## sample version
def data_driven_head_tail(data):
    
    new_data = []

    for idx, val in enumerate(data):
        if LINE_OPTS[0] in val:
            new_data.append(val)
        elif LINE_OPTS[1] in val:
            new_data.append(val)
        elif LINE_OPTS[2] in val:
            new_data.append(val)
        elif LINE_OPTS[3] == val:
            new_data.append(val)
        else:
            new_data.append(separate_into_head_tail_token(val))

        ###if idx % 10 == 0:
        ###    input()
        ###    print("\n===== new start =====")
   
    return new_data  

### Sample version
def write_file(path, data):
    
    before_symbol = "# before_text = "
    mid_symbol = "# mid_text = "
    after_symbol = "# after_text = "
    
    new_word = []
    new_pos = []
    with open(path, "w") as fw:
        for idx, val in enumerate(data):
            if LINE_OPTS[0] in val:
                fw.write(val+"\n")
            elif LINE_OPTS[1] in val:
                fw.write(val+"\n")
            elif LINE_OPTS[2] in val:
                txt = val.split()
                fw.write(before_symbol+" ".join(txt[3:])+"\n")
            elif LINE_OPTS[3] == val:
                fw.write(mid_symbol+" ".join(new_word)+"\n")
                mixed_token = []
                assert len(new_word) == len(new_pos), "The length between word and pos split is wrong, check it \nnew word: {}\nnew_pos: {}".format(new_word, new_pos)
                for word_idx in range(len(new_word)):
                    temp_word = new_word[word_idx].split("+")
                    temp_pos = new_pos[word_idx].split("+")

                    tagged_token = list(zip(temp_word, temp_pos))
                    temp_tagged = []
                    for tagged_val in tagged_token:
                        temp_tagged.append("/".join(tagged_val))

                    mixed_token.append("+".join(temp_tagged))

                fw.write(after_symbol+" ".join(mixed_token)+"\n")
                fw.write("''\n")
                new_word = []
                new_pos = []
            else:
                txt = val.split()
                new_word.append(txt[2])
                new_pos.append(txt[-2])
                   
                
              
if __name__ == "__main__":

   list_of_files = glob(ORI_DIR+"*")
      
   if DEBUG in DEBUG_LEVEL[0:]:
       print("\n===== a list of files to be read =====")
       print("The number of files: {}".format(len(list_of_files)))
       print("for top 5 of examples, \n{}".format(list_of_files[0:5]))

   print(type(list_of_files[0]))

   for val in list_of_files:
       raw_data = read_raw_corpus(val)

       temp_raw_data = data_driven_head_tail(raw_data)

       temp = val.split("/")

       write_file(DES_DIR+"/"+temp[1], temp_raw_data)

       ##input() 

"""
   separate_into_head_tail_token(data[3])
   separate_into_head_tail_token(data[4])
   separate_into_head_tail_token(data[5])
   separate_into_head_tail_token(data[6])
   separate_into_head_tail_token(data[7])
   separate_into_head_tail_token(data[8])
   separate_into_head_tail_token(data[9])
   separate_into_head_tail_token(data[10])
   separate_into_head_tail_token(data[11])
   separate_into_head_tail_token(data[12])
   separate_into_head_tail_token(data[13])
   separate_into_head_tail_token(data[14])


   separate_into_head_tail_token(data[15])
   separate_into_head_tail_token(data[16])
   separate_into_head_tail_token(data[17])
   separate_into_head_tail_token(data[18])
   separate_into_head_tail_token(data[19])
   separate_into_head_tail_token(data[20])
   separate_into_head_tail_token(data[21])
   separate_into_head_tail_token(data[22])
   separate_into_head_tail_token(data[23])
   separate_into_head_tail_token(data[24])
   separate_into_head_tail_token(data[25])
   separate_into_head_tail_token(data[26])
"""
