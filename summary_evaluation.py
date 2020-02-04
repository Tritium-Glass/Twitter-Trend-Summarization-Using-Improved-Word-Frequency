#Summary Evaluation Techniques

def rouge(reference_summary,generated_summary):

    reference_summary = reference_summary.split(' ')
    generated_summary = generated_summary.split(' ')

    reference_set = set()
    generated_set = set()

    for i in range(len(reference_summary)-1):
        reference_set.add(reference_summary[i]+' '+reference_summary[i+1])

    for i in range(len(generated_summary)-1):
        generated_set.add(generated_summary[i]+' '+generated_summary[i+1])

    matching_bigrams = reference_set.intersection(generated_set)
    print(len(matching_bigrams))
    # print(matching_bigrams)

    try:
        precision = len(matching_bigrams)/len(reference_set)
        recall = len(matching_bigrams)/len(generated_set)
        f_measure = (2*precision*recall)/(precision+recall)
        return matching_bigrams,precision, recall, f_measure
    except Exception as e:
        print(e)
        return 0,0,0,0

    #print(f_measure)

# def main():
#     reference_summary = "Microsoft held talks in the past few weeks to acquire software developer platform GitHub, Business Insider reports. The privately held company has more than 23 million individual users in more than 1.5 million organizations."
#     generated_summary = "The privately held company has more than 23 million individual users in more than 1.5 million organizations. Microsoft could also use data from GitHub to improve its artificial intelligence producs. Microsoft declined to comment on the report. GitHub did not immediately return a request for comment."
#     rouge(reference_summary,generated_summary)
#
# if __name__ == '__main__':
#     main()
