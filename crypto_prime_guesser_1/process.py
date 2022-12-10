import re
regex = R"\w*[^[,\s\]]"

file = open('processed_data.txt', 'w')

pk1 = """295153,  318063,  721550,  125921,  481738,  223528,  574018,
        547467,  256646,  962751,  644366,  869489,  868868,  706108,
        450994,  825664,  870495,  538100,  567426,  512806,  430994,
        832042,  745727,  342709,  866747,  983023,   86920,  374583,
        545599,   36003,  857595,  981850,  938277, 1035846,  959352,
        592661,  179368,  757498,  142456,  288879,  578995,   22909,
        831574,  452067,  508905,    4717,  851791,  114752,  831498,
        857001,  802619,    8985,   63489,  681703,  690247,  755253,
         27693,  487639,  700663,  784510,  664167,  865831,  269974,
        756534"""

pk2 = """933562,  404502,  755458,  382077,  647395,  215219,  785923,
         12608,  687363,  132288,  468288, 1008616,  265713,  577978,
       1017268,  375286, 1015901,  463063,  791722,  195084,  710357,
         70173,  308240,  349347,   89492,  539002,  802219,  348837,
        907004,  976272,  456965,  660836,  166987,   51094,    6839,
        361013,  601012,  362817,  210168,  206540,  935826,  639068,
        839885,  560091,  555489,  927414,  479100,  961229,  880993,
       1005705,  909482,  566387,  752340,   81081,  639062,  613672,
         78853,  723744,  958315,  471187, 1013018,  828324,  511730,
        234033"""

sk = """0 0 1 1 0 0 0 1 1 1 0 1 0 0 0 0 0 1 0 1 1 1 1 1 0 1 0 1 0 0 1 0 1 0 0 0 0
 1 0 0 0 1 0 1 1 1 0 1 1 0 0 0 1 0 0 0 0 1 1 1 0 1 0 0"""

ct0 = """667610,31041,171161,303023,750048,753945,838913,537618,325755,578608,398466,912720,642587,242804,877094,152175,136101,511713,743438,997632,39103,360922,29456,361726,136382,85215,185896,918562,153974,301995,772377,1038340,196576,747717,181097,306875,274612,1019081,352025,1013620,56240,683489,83802,368410,692244,624846,556969,354298,1035558,910360,938230,310424,644108,436177,469068,177163,781684,922129,220170,484754,717648,365830,717218,176830"""
ct1 = """704458,875906,851725,295587,226517,396202,767292,766820,585332,809088,919595,624276,516125,683687,25593,850837,278074,960474,458371,59643,100060,270168,259519,357490,641263,620749,294256,485527,979297,809470,222625,200148,1034263,887474,3647,557866,1000522,464134,418303,95381,535689,472322,357643,479951,732627,770149,45838,44661,175932,146454,501815,608380,117720,917388,879010,376142,185298,740527,849674,387961,892869,706320,599212,845681"""

def process(varName, text):
    matches = re.findall(regex, text)
    num = [int(m) for m in matches]
    file.write(varName + "_proc = " + str(num) + "\n\n")


process("pk1", pk1)
process("pk2", pk2)
process("sk", sk)
process("ct0", ct0)
process("ct1", ct1)

file.close()