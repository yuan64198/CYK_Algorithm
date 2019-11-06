import numpy as np
import copy
import sys
import logging

class CKYParser:
    def __init__(this, grammars):
        this.grammars = {}
        this.parse_rules(grammars.split("\n"))
        this.log = []
        
    def parse_rules(this, rules):
        arr = []
        for line in rules:
            tmp = line.split()
            arr.append(tmp)
        for e in arr:
            if(len(e)==4):
                if(e[1] not in this.grammars): 
                    this.grammars[e[1]] = {}
                if(e[2] not in this.grammars[e[1]]): 
                    this.grammars[e[1]][e[2]] = []
                this.grammars[e[1]][e[2]].append(e[0])
                this.grammars[e[1]][e[2]].append(float(e[3]))
            if(len(e)==3):
                if(e[1] not in this.grammars): 
                    this.grammars[e[1]] = {}
                this.grammars[e[1]][e[0]] = float(e[2])
    
    def parse_sentence(this, sent):
        words = sent.split()
        ret = []
        this.log.append("PROCESSINGS SENTENCE "+sent)
        tmp_ret, tmp_log = this.copy_first(words)
        ret.append(tmp_ret)
        this.log.append(tmp_log)
        
        for i in range(1, len(words)):
            tmp_ret = []
            tmp_log = []
            for j in range(len(words)-i):
                ret_g = {}
                log_g = {}
                for k in range(i):
                    ret_g, log_g = this.cal_grammars(ret[k][j][1], ret[i-k-1][j+1+k][1], ret_g, log_g, j)
                str1 = ' '.join(str(e) for e in words[j:j+i+1])
                
                
                tmp_ret.append([str1, ret_g])
                tmp_log.append(["SPAN: "+str1, list(log_g.values())])
                
            ret.append(tmp_ret)
            this.log.append(tmp_log)
        return ret
    
    def copy_first(this, words):
        ret = []
        log = []
        for w in words:
            ret.append([w, this.grammars[w]])
            a = this.write_SPAN_log(w)
            log.append(["SPAN: "+w, a])
        return ret, log
    
    def write_SPAN_log(this, w):
        log = []
        for g in this.grammars[w]:
            log.append("P("+g+") = "+str(this.grammars[w][g]))
        return log
    
    def cal_grammars(this, dic1, dic2, ret, log, j):
        for g1 in dic1:
            for g2 in dic2:
                result = 0.0
                if g1 in this.grammars and g2 in this.grammars[g1]:
                    if(this.grammars[g1][g2][0] not in ret):
                        ret[this.grammars[g1][g2][0]] = 0.0
                    result = dic1[g1]*dic2[g2]*this.grammars[g1][g2][1]
                    result = float(format(result, '.2g'))
                    
                    if(result > ret[this.grammars[g1][g2][0]]):
                        ret[this.grammars[g1][g2][0]] = result
                        log[this.grammars[g1][g2][0]] = "P("+str(this.grammars[g1][g2][0])+") = "+str(result)+\
                        " (BackPointer = ("+str(j+1)+","+g1+","+g2+"))"
        return ret, log
    
    def write_log_to_file(this, file_name):
        f = open(file_name, "w")
        for line in this.log:
            if type(line) is str:
                f.write(line+"\n")
            else:
                for e in line:
                    if type(e) is str:
                        f.write(line+"\n")
                    else:
                        for g in e:
                            if type(g) is str:
                                f.write(g+"\n")
                            else:
                                for gg in g:
                                    f.write(gg+"\n")
                    f.write("\n")
            #f.write("\n")
        f.close()


#class bcolors:
#    HEADER = '\033[95m'
#    OKBLUE = '\033[94m'
#    OKGREEN = '\033[92m'
#    WARNING = '\033[93m'
#    FAIL = '\033[91m'
#    ENDC = '\033[0m'
#    BOLD = '\033[1m'
#    UNDERLINE = '\033[4m'

def read_file(file_name):
    try:
        f = open( file_name,"r+")
        ret = f.read()
        f.close()
        #logging.info("Read File ",file_name," Successfully!")
        return ret
    except:
        print("Cannot read file successfully")


def main():
    if(len(sys.argv) != 4):
        print(len(sys.argv))
        print("PLEASE ENTER INPUT FILES: GRAMMAR_RULES, SENTENCES, OUTPUT_FILE")
    else:
        rules = read_file(sys.argv[1])
        sents = read_file(sys.argv[2])
        parser = CKYParser(rules)
        sents_list = sents.split("\n")

        for s in sents_list:
            parser.parse_sentence(s)
        parser.write_log_to_file(sys.argv[3])
        #logging.info("=====Done Parsing Sentences using CYK Algorithm=====")
    return


if __name__== "__main__":
    main()