import pandas
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing

def minerMLMode_createModel():
    print "Creating model"
    # Read DataFrame file - processes from ELK
    df = pandas.read_pickle(r"D:\Projects\dataFrame")

    # User lable encoder to transform processes names to integers
    le = preprocessing.LabelEncoder()
    procNameList = le.fit_transform(df[u'UserProcesses.ProcessName'])
    print procNameList[:10]
    # Get cpu an classification lists from DF
    procCpuList = df[u'UserProcesses.CPU'].to_list()
    print procCpuList [:10]
    classList = df['class'].to_list()
    print classList[:10]

    # Prepare features for model
    features = list(zip(procNameList, procCpuList))

    # Use KNN model
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(features, classList)

    return model


def minerMLMode_inspect(model, process):
    le = preprocessing.LabelEncoder()
    procName = le.transform([process[2]])[0]
    procCpu = process[1]

    # Use the model for new data (inspected process)
    predicted = model.predict([[procName, procCpu]])

    # Returns 0 for normal and 1 for abnormal (potential miner)
    print predicted
    return predicted

# def main():
#
#     model = minerMLMode_createModel()


if __name__ == '__main__':
    main()
