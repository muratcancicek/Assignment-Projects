import java.net.URLDecoder
import java.text.SimpleDateFormat

import org.apache.spark.sql.{Row, SaveMode, SparkSession}
import org.apache.spark.{SparkConf, SparkContext}
import util.LumberjackParser

/**
  * Created by ykurtulus on 27/07/16.
  */
object SimpleApp {

  def main (args :Array[String]): Unit ={

    val spark = SparkSession.builder()
      .appName("The swankiest Spark app ever")
      .master("local[*]")
      .getOrCreate()

   // val lines = scala.io.Source.fromFile("C:\\Users\\miek\\Desktop\\Test\\TestCase2.txt").mkString.split("\n")
    //  C:\Users\miek\Downloads\session\session\2016-09-27

    val lines = spark.sparkContext.textFile("C:\\Users\\miek\\Desktop\\Test\\TestCase2.txt").map(line => line.toString)
     .map(line => LumberjackParser.parse(line))
    println(lines.first())
    println(lines.first().get("_bot"))
    val f = lines.filter(m => (m.get("_bot").get.equals("0")))
    println(f.count())


    println("Started!")
   // val lines = spark.read.text("C:\\Users\\miek\\Downloads\\session\\session\\2016-09-27\\part-r-00000")
   // val lines = spark.read.option("header" , "true").text("C:\\Users\\miek\\Downloads\\session\\session\\2016-09-27")
   // val lines = spark.read.option("header" , "true").text("C:\\Users\\miek\\Downloads\\session\\session\\2016-09-27\\part-r-00000").map(line => LumberjackParser.parse(line))

    //lines.map(line => LumberjackParser.parse(line))


   // lines.show()
     // val distinctLines = lines.distinct
    //println("Count2 = " + distinctLines.count())

     //distinctLines.write.mode(SaveMode.Append).text("C:\\Users\\miek\\Downloads\\session\\output.txt");
     // parser



    //val distincLinesRDD = distinctLines.rdd



    //distincLinesRDD.map(line => LumberjackParser.parse(line))

   // distincLinesRDD.coalesce(1).saveAsTextFile("C:\\Users\\miek\\Downloads\\session\\output1")

    //val checkData = spark.read.option("header" , "true").text("C:\\Users\\miek\\Downloads\\session\\output\\part-00000")
    //println("Count3 = " + checkData.count())


    //val f = (lines.filter(distinctLines.sqlContext))

    //f.show

    //         val t = lines.map(x  => x.substring(x.indexOfSlice("sid=")).substring(4, x.substring(x.indexOfSlice("sid=")).indexOfSlice("&")))
    //
    //         println(t(2))
    //         println(t.length)
    //         val p = t.distinct
    //         println(p.length)

    //       val s = lines.map(x.slice(x.indexOfSlice("sid=") + 4, x.indexOfSlice("&")) => x)



  }

}
