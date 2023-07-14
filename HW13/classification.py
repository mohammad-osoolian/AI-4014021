import random 

def read_records(path):
    with open(path, 'r') as file:
        string_records = file.readlines()
    records = []
    for string_record in string_records:
        temp = string_record.strip().split(',')
        temp[0] = float(temp[0])
        temp[1] = float(temp[1])
        temp[2] = float(temp[2])
        temp[3] = float(temp[3])
        records.append(temp)
    return records

def round_records(records):
    rounded_records = []
    for record in records:
        rounded_record = []
        for value in record[:4]:
            rounded_record.append(round(value))
        rounded_record.append(record[4])
        rounded_records.append(rounded_record)
    return rounded_records

def find_classes(records):
    classes = []
    for record in records:
        if record[4] not in classes:
            classes.append(record[4])
    return classes

def group_by_classes(records):
    classes = find_classes(records)
    grouped_records = {}
    for i in range(len(classes)):
        grouped_records[classes[i]] = []
    for record in records:
        grouped_records[record[4]].append(record)
    return grouped_records

def count_features(grouped_records, rounded_records):
    feats = []
    for i in range(4):
        feats.append([])
        for j in range(10):
            feats[i].append([])
            feats[i][j] = {}
            for cl in grouped_records.keys():
                feats[i][j][cl] = 0
    for record in rounded_records:
        for i in range(4):
            feats[i][record[i]][record[4]] += 1/len(grouped_records[record[4]])
    return feats

def classify(feats, record):
    probs = {}
    for cl in feats[0][0].keys():
        probs[cl] = 1
        for i in range(4):
            probs[cl] *= feats[i][record[i]][cl]
    return max(probs, key=probs.get)

def test_classifier(feats, records):
    correct = 0
    for record in records:
        if classify(feats, record) == record[4]:
            correct += 1
    return correct, len(records)

records = read_records('iris.data')
rounded_records = round_records(records)
random.shuffle(rounded_records)
train_data = rounded_records[:len(rounded_records)//10*8]
test_data = rounded_records[len(rounded_records)//10*8:]
grouped_records = group_by_classes(train_data)
cpts = count_features(grouped_records, train_data)
correct, total = test_classifier(cpts, test_data)
print("train with rounded values:")
print('Correct: ', correct)
print('Total: ', total)

