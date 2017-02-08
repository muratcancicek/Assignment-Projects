package util

/**
  * Created by miek on 07.12.2016.
  */

  import java.net.URLDecoder
  import LumberjackConstants._

  object LumberjackParser {

    def isMobile(m: Map[String, String]) = {
      m.contains(KEY_TYPE) && (m(KEY_TYPE) == KEY_TYPE_MOBILE_SITE || m(KEY_TYPE) == KEY_TYPE_MOBILE_DEVICE)
    }

    def isBotAgent(m: Map[String, String]) = {
      !isMobile(m) && m.contains(KEY_AGENT) && BotUtil.isBotAgent(m(KEY_AGENT))
    }

    def parse(input: String): Map[String, String] = {
      val str = input.replace('\t', ' ').split(' ')
      val map = str(1).split('&').map { str =>
        val pair = str.split('=')
        if (pair.length > 1) {
          val keyword = URLDecoder.decode(StringUtil.getFixedEncodingValue(pair(1)), "utf-8")
          (pair(0) -> keyword)
        } else {
          (pair(0) -> "")
        }
      }.toMap

      val memberId = {
        if (map.contains(KEY_USER_ID))
          map(KEY_USER_ID)
        else if (map.contains(KEY_USER_ID_FROM_COOKIE)) {
          if (map(KEY_USER_ID_FROM_COOKIE).contains(",")) {
            val values = map(KEY_USER_ID_FROM_COOKIE).split(",")
            if (values.length == 2) {
              values(1)
            } else {
              "0"
            }
          }
          else
            map(KEY_USER_ID_FROM_COOKIE)
        } else "0"
      }

      map.updated(KEY_TIMESTAMP, str(0))
        .updated(KEY_USER_ID_FOUND, memberId)
    }
  }


