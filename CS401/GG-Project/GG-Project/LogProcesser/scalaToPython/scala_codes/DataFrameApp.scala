import org.apache.spark.sql.SparkSession

/**
  * Created by ykurtulus on 27/07/16.
  */
object DataFrameApp {

  def main (args :Array[String]): Unit ={

    val spark = SparkSession
      .builder()
      .appName("Spark SQL basic example")
      .config("spark.some.config.option", "some-value")
      .getOrCreate()


  }

}
