from heapq import nlargest
from operator import itemgetter
from collections import defaultdict
from CommonTools import *

class model_based(object):
    def __init__(self, *args, **kwargs):
        self.best_hotels_od_ulc = defaultdict(lambda: defaultdict(int))
        self.best_hotels_search_dest = defaultdict(lambda: defaultdict(int))
        self.best_hotels_search_dest1 = defaultdict(lambda: defaultdict(int))
        self.best_hotel_country = defaultdict(lambda: defaultdict(int))
        self.popular_hotel_cluster = defaultdict(int)
        self.columnNames = getColumnNames() 
        self.getColumnDict()

    def getColumnNames():
        return ['date_time', 'site_name', 'posa_continent', 'user_location_country', 'user_location_region', 'user_location_city',\
        'orig_destination_distance', 'user_id', 'is_mobile', 'is_package', 'channel', 'srch_ci', 'srch_co', 'srch_adults_cnt',\
        'srch_children_cnt', 'srch_rm_cnt', 'srch_destination_id', 'srch_destination_type_id', 'hotel_continent', 'hotel_country',\
        'hotel_market', 'is_booking', 'cnt', 'hotel_cluster']

    def getColumnDict(self):
        self.colIndict = {}
        for columnIndex, column in enumerate(self.columnNames):
            self.colIndict[column] = columnIndex

    def train(self, fileName):
        iterateRows(self.readTrainRow, fileName)

    def readTrainRow(self, row):
        book_year = int(row[0][:4])
        user_location_region = row[4]
        user_location_city = row[5]
        orig_destination_distance = row[6]
        srch_destination_id = row[16]
        is_booking = int(row[18])
        hotel_country = row[21]
        hotel_market = row[22]
        hotel_cluster = row[23]

        append_1 = 3 + 17*is_booking
        append_2 = 1 + 5*is_booking

        if orig_destination_distance != '':
            self.best_hotels_od_ulc[(user_location_city, orig_destination_distance)][hotel_cluster] += 1

        if book_year == 2014:
            self.best_hotels_search_dest[(srch_destination_id, hotel_country, hotel_market)][hotel_cluster] += append_1
#        
        self.best_hotels_search_dest1[srch_destination_id][hotel_cluster] += append_1
                
        self.best_hotel_country[hotel_country][hotel_cluster] += append_2
        
        self.popular_hotel_cluster[hotel_cluster] += 1

    def predict(self, fileName):
        print('Generate submission...')
        now = datetime.datetime.now()
        path = 'submission_' + str(now.strftime("%Y-%m-%d-%H-%M")) + '.csv'
        self.submissionFile = open(path, "w")
        self.submissionFile.write("id,hotel_cluster\n")
        self.topclasters = nlargest(5, sorted(self.popular_hotel_cluster.items()), key=itemgetter(1))
        self.predictions = []
        iterateRows(self.readTestRow, fileName)
        self.submissionFile.close()
        return self.predictions
         
    def readTestRow(self, row):
        id = row[0]
        user_location_city, orig_destination_distance = row[6], row[7]
        srch_destination_id, hotel_country, hotel_market = row[17], row[20], row[21]

        self.submissionFile.write(str(id) + ',')
        self.rankingsForCurrentRow = []
        
        self.pickRankings((user_location_city, orig_destination_distance), self.destDis_uCity)
        self.pickRankings((srch_destination_id, hotel_country, hotel_market), self.best_hotels_search_dest)
        self.pickRankings(srch_destination_id, self.best_hotels_search_dest1)
        self.pickRankings(hotel_country, self.best_hotel_country)
        self.getTopItems(self.topclasters)
        self.submissionFile.write("\n")
        self.predictions.append(filled)

    def pickRankings(self, rowKey, dictionary):
        if rowKey in dictionary:
            self.getTopItems(nlargest(5, sorted(dictionary[rowKey].items()), key=itemgetter(1)))

    def getTopItems(self, topitems):
        for i in range(len(topitems)):
            if topitems[i][0] in self.rankingsForCurrentRow:
                continue
            if len(self.rankingsForCurrentRow) == 5:
                break
            self.submissionFile.write(' ' + topitems[i][0])
            self.rankingsForCurrentRow.append(topitems[i][0])