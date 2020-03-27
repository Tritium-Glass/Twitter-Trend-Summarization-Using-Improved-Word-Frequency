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
    print(matching_bigrams)

    try:
        precision = len(matching_bigrams)/len(reference_set)
        recall = len(matching_bigrams)/len(generated_set)
        f_measure = (2*precision*recall)/(precision+recall)
        return matching_bigrams,precision, recall, f_measure
    except Exception as e:
        print(e)
        return 0,0,0,0

    print(f_measure)

def main():
    reference_summary = "After bearing the brunt of jihadist dynamite and looting by thieves, the archaeological treasures of Afghanistan's Bamiyan province are facing a new and possibly more daunting threat: climate change/."
    generated_summary = "Many of the artefact’s pre-date the arrival of Islam to the region but despite the fact they come from another religion, the residents who spoke with AFP proudly defended the area's history as their own."
    rouge(reference_summary, generated_summary)

if __name__ == '__main__':
    main()
