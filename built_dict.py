def build_dict():
    ref_dict = {}
    syn_dict = {}
    with open('syn1.txt') as f:
        for line in f:
            word = line.split("#", 1)[0]
            ref = line.split("#", 1)[1]
            ref = ref.split('\n', 1)[0]
            ref = ref.replace(';', ',')
            if ref.startswith(','):
                ref = ref.split(' ', 1)[1]
                ref_dict[word] = word
                ##syn_dict[word] = [x.strip() for x in ref.split(',')]
                syns = [x.strip() for x in ref.split(',')]
                if (len(syns) > 5):
                    syn_dict[word] = [x.strip() for x in ref.split(',')]
            else:
                ref = ref.split(',', 1)[0]
                ref_dict[word] = ref
    return syn_dict
