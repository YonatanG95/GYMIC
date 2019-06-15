import pandas
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
import numpy

#le = None

def minerMLMode_createModel():

    print "Creating model"
    # Read DataFrame file - processes from ELK
    df = pandas.read_pickle(r"D:\Projects\GYMIC\GYMIC-Server\ML_Files\ProcDataFrame")

    # Use label encoder to transform processes names to integers
    le = preprocessing.LabelEncoder()
    le.fit(df['ProcessName'])
    procNameList = le.transform(df['ProcessName'])

    # Use label encoder to transform users to integers
    le2 = preprocessing.LabelEncoder()
    le2.fit(df['User'])
    userList = le2.transform(df['User'])

    # Get CPU usage
    procCpuList = df['CPU'].to_list()

    # Get network usage (is communicating?)
    netList = df['Network'].to_list()

    # Get classification
    classList = df['Class'].to_list()

    # Prepare features for model
    features = list(zip(procNameList, procCpuList, userList, netList))

    # Use KNN model
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(features, classList)

    return (model, le, le2)


def minerMLMode_inspect(model, le, le2,  process, commValue):

    # Use label encoder to transform processes names & users to integers
    procName = le.transform([process[2]])[0]
    procUser = le2.transform([process[3]])[0]

    # Get cpu and network usage
    procCpu = process[1]

    # Use the model for new data (inspected process)
    predicted = model.predict([[procName, procCpu, procUser, commValue]])

    # Returns 0 for normal and 1 for abnormal (potential miner)
    return predicted
