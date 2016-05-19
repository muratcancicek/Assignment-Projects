import pandas as pd
import average_precision as ap
from sklearn.decomposition import PCA
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold
from itertools import chain
import random
import operator

# source:
# https://www.dataquest.io/blog/kaggle-tutorial/

################################  reading downsampled data  ###################

def readDownsampledDataAsPanda(trainName = 'selectedTrain.csv', testName = 'selectedTest.csv'):
    train = pd.read_csv(trainName)
    test = pd.read_csv(testName)
    print 'Downsampled data is read' 
    return train, test

################################  reading data  ###############################

def readDataAsPanda():
    #test = pd.read_csv("test.csv")
    train = pd.read_csv("train.csv")
    print 'Original data is read!' 
    return train

################################  getting downsampled data  ###################

def getDownsampledData(train, count = 10000):
    train["date_time"] = pd.to_datetime(train["date_time"])
    train["year"] = train["date_time"].dt.year
    train["month"] = train["date_time"].dt.month

    unique_users = train.user_id.unique()

    if count > len(unique_users): count = len(unique_users)
    sel_user_ids = [unique_users[i] for i in sorted(random.sample(range(len(unique_users)), count)) ]
    sel_train = train[train.user_id.isin(sel_user_ids)]

    newTrain = sel_train[((sel_train.year == 2013) | ((sel_train.year == 2014) & (sel_train.month < 8)))]
    newTest = sel_train[((sel_train.year == 2014) & (sel_train.month >= 8))]

    newTest = newTest[newTest.is_booking == True]
    print 'Downsampling process is done' 
    return newTrain, newTest
    
################################  saving downsampled data  ####################

def saveDownsampledData(newTrain, newTest, trainName = 'selectedTrain.csv', testName = 'selectedTest.csv'):
    newTrain.to_csv(trainName) 
    newTest.to_csv(testName) 
    print 'Downsampled data is saved' 
    
################################  doing downsampling  #########################

def doDownsampling(count = 10000, trainName = 'selectedTrain.csv', testName = 'selectedTest.csv'):
    train = readDataAsPanda();
    newTrain, newTest = getDownsampledData(train, count)
    saveDownsampledData(newTrain, newTest, trainName, testName)
    print 'Downsampling is done' 

################################  doing prediction with mean  #################

def predictWithMean():
    t1, t2 = KaggleTutorial.readDownsampledDataAsPanda()
    most_common_clusters = list(t1.hotel_cluster.value_counts().head().index)
    predictions = [most_common_clusters for i in range(t2.shape[0])]
    target = [[l] for l in t2["hotel_cluster"]]
    accuracy = ap.mapk(target, predictions, k=5) 
    return predictions, accuracy

################################  generating features from destinations  ######

def generateFeaturesFromDestinations():
    destinations = pd.read_csv("destinations.csv")
    pca = PCA(n_components=3)
    dest_small = pca.fit_transform(destinations[["d{0}".format(i + 1) for i in range(149)]])
    dest_small = pd.DataFrame(dest_small)
    dest_small["srch_destination_id"] = destinations["srch_destination_id"]
    return dest_small
    
################################  calculating fast features  ##################

def calc_fast_features(df):
    df["date_time"] = pd.to_datetime(df["date_time"])
    df["srch_ci"] = pd.to_datetime(df["srch_ci"], format='%Y-%m-%d', errors="coerce")
    df["srch_co"] = pd.to_datetime(df["srch_co"], format='%Y-%m-%d', errors="coerce")
    
    props = {}
    for prop in ["month", "day", "hour", "minute", "dayofweek", "quarter"]:
        props[prop] = getattr(df["date_time"].dt, prop)
    
    carryover = [p for p in df.columns if p not in ["date_time", "srch_ci", "srch_co"]]
    for prop in carryover:
        props[prop] = df[prop]
    
    date_props = ["month", "day", "dayofweek", "quarter"]
    for prop in date_props:
        props["ci_{0}".format(prop)] = getattr(df["srch_ci"].dt, prop)
        props["co_{0}".format(prop)] = getattr(df["srch_co"].dt, prop)
    props["stay_span"] = (df["srch_co"] - df["srch_ci"]).astype('timedelta64[h]')
        
    ret = pd.DataFrame(props)
    
    dest_small = generateFeaturesFromDestinations()
    
    #ret.fillna(-1, inplace=True) # WRONG
    #dest_small.fillna(-1, inplace=True) # WRONG
    ret = ret.join(dest_small, on="srch_destination_id", how='left', rsuffix="dest")
    ret = ret.drop("srch_destination_iddest", axis=1)
    return ret

#####################  doing prediction with Random Forest Classifier  ########

def predictWithRandomForestClassifier():
    t1, t2 = readDownsampledDataAsPanda()
    df = calc_fast_features(t1)
    df.fillna(-1, inplace=True)
    predictors = [c for c in df.columns if c not in ["hotel_cluster"]]
    clf = RandomForestClassifier(n_estimators=10, min_weight_fraction_leaf=0.1)
    scores = cross_validation.cross_val_score(clf, df[predictors], df['hotel_cluster'], cv=3)
    return scores

#####################  doing prediction with Random Forest Classifier  ########

def predictWithRandomForestClassifier2():
    t1, t2 = readDownsampledDataAsPanda()
    df = calc_fast_features(t1)
    df.fillna(-1, inplace=True)
    all_probs = []
    unique_clusters = df["hotel_cluster"].unique()
    for cluster in unique_clusters:
        df["target"] = 1
        df["target"][df["hotel_cluster"] != cluster] = 0
        predictors = [col for col in df if col not in ['hotel_cluster', "target"]]
        probs = []
        cv = KFold(len(df["target"]), n_folds=2)
        clf = RandomForestClassifier(n_estimators=10, min_weight_fraction_leaf=0.1)
        for i, (tr, te) in enumerate(cv):
            clf.fit(df[predictors].iloc[tr], df["target"].iloc[tr])
            preds = clf.predict_proba(df[predictors].iloc[te])
            probs.append([p[1] for p in preds])
        full_probs = chain.from_iterable(probs)
        all_probs.append(list(full_probs))

    prediction_frame = pd.DataFrame(all_probs).T
    prediction_frame.columns = unique_clusters
    def find_top_5(row):
        return list(row.nlargest(5).index)

    preds = []
    for index, row in prediction_frame.iterrows():
        preds.append(find_top_5(row))

    return ap.mapk([[l] for l in t2.iloc["hotel_cluster"]], preds, k=5)

################################  making key  #################################

def make_key(items):
    return "_".join([str(i) for i in items])

#################### helper 1 for top clusters based on hotel_cluster  ########
    
def f5(seq, idfun=None): 
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

#################### helper 1 for top clusters based on hotel_cluster  ########
    
def generate_exact_matches(row, match_cols):
    index = tuple([row[t] for t in match_cols])
    try:
        group = groups.get_group(index)
    except Exception:
        return []
    clus = list(set(group.hotel_cluster))
    return clus

################################  top clusters based on hotel_cluster  ########

def predictBasedOnTopClusters():
    match_cols = ["srch_destination_id"]
    cluster_cols = match_cols + ['hotel_cluster']
    t1, t2 = readDownsampledDataAsPanda(testName = 'test.csv')
    groups = t1.groupby(cluster_cols)
    top_clusters = {}
    for name, group in groups:
        clicks = len(group.is_booking[group.is_booking == False])
        bookings = len(group.is_booking[group.is_booking == True])
    
        score = bookings + .15 * clicks
    
        clus_name = make_key(name[:len(match_cols)])
        if clus_name not in top_clusters:
            top_clusters[clus_name] = {}
        top_clusters[clus_name][name[-1]] = score
        cluster_dict = {}
    for n in top_clusters:
        tc = top_clusters[n]
        top = [l[0] for l in sorted(tc.items(), key=operator.itemgetter(1), reverse=True)[:5]]
        cluster_dict[n] = top

    preds = []
    for index, row in t2.iterrows():
        key = make_key([row[m] for m in match_cols])
        if key in cluster_dict:
            preds.append(cluster_dict[key])
        else:
            preds.append([])

    match_cols = ['user_location_country', 'user_location_region', 'user_location_city', 'hotel_market', 'orig_destination_distance']

    groups = t1.groupby(match_cols)
    exact_matches = []
    for i in range(t2.shape[0]):
        exact_matches.append(generate_exact_matches(t2.iloc[i], match_cols))
    
    most_common_clusters = list(t1.hotel_cluster.value_counts().head().index)

    full_preds = [f5(exact_matches[p] + preds[p] + most_common_clusters)[:5] for p in range(len(preds))]
    accuracy = ap.mapk([[l] for l in t2["hotel_cluster"]], full_preds, k=5)
    print 'Predictions are generated' 
    return accuracy, t2, full_preds

    
################################  Making a Kaggle submission file  ############

def makeAKaggleSubmissionFile(t2, full_preds):
    write_p = [" ".join([str(l) for l in p]) for p in full_preds]
    write_frame = ["{0},{1}".format(t2["id"][i], write_p[i]) for i in range(len(full_preds))]
    write_frame = ["id,hotel_cluster"] + write_frame
    with open("predictions.csv", "w+") as f:
        f.write("\n".join(write_frame))
    print 'Predictions are saved' 