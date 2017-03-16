package util

/**
  * Created by miek on 07.12.2016.
  */
import java.util.regex._
import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD
import util.LumberjackConstants._
import org.apache.spark.HashPartitioner

object BotUtil {

  val BOT_REGEX: String = "bot|index|spider|crawl|wget|slurp|mediapartners|httpclient|" +
    "facebookexternalhit|nagios|pingdom|qualysguard|winhttp|twitterbot|httprequest|pinterest|appengine|internetseer"

  val pattern = Pattern.compile(BOT_REGEX)

  def isBotAgent(userAgent: String): Boolean = {
    if (userAgent != null) {
      val agent = userAgent.toLowerCase.trim
      return pattern.matcher(agent).find() ||
        agent.startsWith("java") ||
        agent.startsWith("php")
    }
    false
  }

  /**
    * Finds safe sessions by user agent
    */
  def getUserAgentsBySession(sc: SparkContext, logs: RDD[Map[String, String]]): RDD[(String, String)] = {
    logs.filter(m => m.contains(KEY_MODULE) &&
      m.contains(KEY_SESSION_ID) &&
      m.contains(KEY_AGENT) &&
      m(KEY_MODULE).equals(KEY_MODULE_NEWSESSION))
      .map(m => (m(KEY_SESSION_ID), m(KEY_AGENT)))
      .distinct()
      .partitionBy(new HashPartitioner(60))
  }

  /**
    * Filters bot sessions
    */
  def getSafeLogs(sc: SparkContext, logs: RDD[Map[String, String]]): RDD[Map[String, String]] = {
    val safeSessions = getUserAgentsBySession(sc, logs)

    logs.map(m => (m(KEY_SESSION_ID), m))
      .partitionBy(new HashPartitioner(60))
      .fullOuterJoin(safeSessions)
      .map(x => x._2._1.get.updated(KEY_BOT, x._2._2.getOrElse(null)))
      .filter(m => !isBotAgent(m(KEY_BOT)))
  }

}