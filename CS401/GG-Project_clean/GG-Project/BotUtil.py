
#BOT_REGEX = "bot|index|spider|crawl|wget|slurp|mediapartners|httpclient|" + \
#    "facebookexternalhit|nagios|pingdom|qualysguard|winhttp|twitterbot|httprequest|pinterest|appengine|internetseer"

#pattern = Pattern.compile(BOT_REGEX)

def isBotAgent(userAgent):
    if (userAgent != None):
        agent = userAgent.lower()
        return agent[:4] == "java" or agent[:3] == "php" # or pattern.matcher(agent).find()
    else:
        return False

#/**
#* Finds safe sessions by user agent
#*/
#def getUserAgentsBySession(sc: SparkContext, logs: RDD[Map[String, String]]): RDD[(String, String)] = {
#logs.filter(m => m.contains(KEY_MODULE) &&
#    m.contains(KEY_SESSION_ID) &&
#    m.contains(KEY_AGENT) &&
#    m(KEY_MODULE).equals(KEY_MODULE_NEWSESSION))
#    .map(m => (m(KEY_SESSION_ID), m(KEY_AGENT)))
#    .distinct()
#    .partitionBy(new HashPartitioner(60))
#}

#/**
#* Filters bot sessions
#*/
#def getSafeLogs(sc: SparkContext, logs: RDD[Map[String, String]]): RDD[Map[String, String]] = {
#val safeSessions = getUserAgentsBySession(sc, logs)

#logs.map(m => (m(KEY_SESSION_ID), m))
#    .partitionBy(new HashPartitioner(60))
#    .fullOuterJoin(safeSessions)
#    .map(x => x._2._1.get.updated(KEY_BOT, x._2._2.getOrElse(null)))
#    .filter(m => !isBotAgent(m(KEY_BOT)))
#}

#}