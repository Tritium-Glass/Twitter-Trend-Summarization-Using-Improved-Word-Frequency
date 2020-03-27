import csv
import pandas as pd
import numpy as np
from timeit import default_timer as timer
from nltk.tokenize import sent_tokenize
import summary_evaluation as sumeval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

def lsa_summarise(text):

    #break into sentences
    doc =  sent_tokenize(text)
    print(len(doc))

    # Converting each document into an vector
    vectorizer = CountVectorizer()
    bag_of_words = vectorizer.fit_transform(doc)
    print(bag_of_words.todense())

    #Singular value decomposition

    #This process encodes our original data into topic encoded data
    #n_components = number of topics
    svd = TruncatedSVD(n_components = 1)
    lsa = svd.fit_transform(bag_of_words)
    print(len(lsa))

    #Using pandas to look at the output of lsa
    topic_encoded_df = pd.DataFrame(lsa, columns=["topic1"])
    topic_encoded_df["doc"]= doc
    topic_encoded_df['abs_topic1']=np.abs(topic_encoded_df["topic1"])
    print(topic_encoded_df[["doc","abs_topic1"]])

    final_matrix=topic_encoded_df.sort_values('abs_topic1',ascending=False)
    # print(final_matrix)
    sorted_sen = list(final_matrix['doc'])
    # print(sorted_sen)

    final_summary = ""
    while True and len(sorted_sen)>0:
        summ = sorted_sen.pop(0)
        if (len(final_summary)+len(summ))<280:
            final_summary += (summ + ". ")
        else:
            if len(final_summary)<1 and len(sorted_sen)>0:
                sorted_sen.pop(0)
                continue
            else:
                break

    return final_summary

def lsa_sum(human_summary, text):
    ref_sum = human_summary
    lsa_start = timer()
    lsa_sum = lsa_summarise(text)
    lsa_end = timer()
    lsa_time = lsa_end - lsa_start
    matching_bigrams, lsa_precision, lsa_recall, lsa_f_measure = sumeval.rouge(ref_sum, lsa_sum)
    # print("TF-IDF: Time:",tf_time,"precision: ",tf_precision,"recall:"\
    # ,tf_recall,"f_measure:",tf_f_measure)

    with open('results_m2_sem8_lsa.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([str(lsa_time),str(lsa_f_measure)])

def main():
    # with open('doc_sum_2.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     i = 0
    #     for row in csv_reader:
    #         i+=1
    #         lsa_sum(row[1].lower(), row[0].lower())

    text = '''
    New Delhi: Petrol prices slipped below Rs 71-mark for the first time in eight months on Monday as India looks set to reap windfall from a price war among oil producers leading to international crude prices crashing by their biggest margin since the 1991 Gulf war.International oil prices crashed by close to 31 percent, the second-largest margin on record, after the disintegration of the OPEC+ alliance triggered an all-out price war between Saudi Arabia and Russia.Brent futures plummeted to about $31 a barrel on Monday as Goldman Sachs warned prices could drop to near $20.For India, which imports over 84 percent of its oil needs, the slump would lead to lower import bill and a cut in retail prices but will harm already stressed upstream firms such as ONGC.Lower oil prices will also help economy from its 11-year low growth rate by way of reducing input cost for a lot of sectors.In Delhi, petrol prices dropped to Rs 70.59 a litre, the lowest since early July 2019, and diesel rate were cut to Rs 63.26, according to a price notification of state-owned firms. Petrol price falls below Rs 71, first time in eight months; India to gain from Saudi Arabia, Russia oil price warRepresentational image. Fuel prices have been on the decline since 27 February on international trends. Petrol prices have in all fallen by Rs 1.42 a litre since then and diesel rates have dropped by Rs 1.44 per litre.But the only dampener in the entire scheme of things is rupee which settled 23 paise down at 74.10 against the US dollar. A weaker rupee means India pays more for buying the same amount of commodity from overseas. It will also help lower inflation rate.According to the oil ministry's petroleum planning and analysis cell, India is likely to pay $105.58 billion or Rs 7.43 lakh crore on import of 225 million tonnes of crude oil in the fiscal year 2019-20, which ends this month. This compares to $111.9 billion (Rs 7.83 lakh crore) paid for import of 226.5 million tonnes of oil in 2018-19.The 2019-20 projection is based on average price of $66 per barrel for the basket of crude oil India imports and average exchange rate of 71 to a US dollar.Oil company officials said the import bill will fall in the next fiscal beginning April but an estimation cannot be made given the extreme volatility in the oil and currency market.It certainly will translate into lower retail prices of petrol and diesel in the coming days as the current rates do not reflect the slump in international prices, they said.Retail prices of the day are based on average price of benchmark international fuel of the preceeding fortnight. And the drop in prices to $31 will get reflected in retail prices over the next 7-10 days.The moving average helps narrow the extreme volatility in the prices, they said.On the negative side, lower oil prices mean they become more competitive versus renewable energy and delay switchover to cleaner fuels in fight against climate change.Industry association Assocham said the fall in crude prices will help India recover as low prices of crude can be a demand driver while also taming the inflation.However, Morgan Stanley believes that the drop in oil prices may not be good news for the economy as the gains will remain capped due to the overall weakness in the economy given the coronavirus-related health scare.The decline in oil prices, it said, will negatively impact the capex outlook for oil related sectors as well as oil producing countries.The fall in oil prices comes at a time when the global economy is already reeling under the impact of coronavirus, which has dented demand across sectors and economies.
    '''

    hs = '''
    International oil prices crashed by close to 31 percent, the second-largest margin on record, after the disintegration of the OPEC+ alliance triggered an all-out price war between Saudi Arabia and Russia Brent futures plummeted to about $31 a barrel on Monday as Goldman Sachs warned prices could drop to near $20 Saudi Arabia slashed its oil prices over the weekend by most in at least 20 years and pledged to increase production after Russia refused to join the OPEC in a production cut as the spread of coronavirus continues to slow the global economy and oil demand
    '''

    lsa_sum(hs, text)

if __name__ == '__main__':
    main()
