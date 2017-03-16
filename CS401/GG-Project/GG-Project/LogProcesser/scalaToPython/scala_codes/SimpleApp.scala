import com.mongodb.casbah.Imports._
import org.apache.spark.sql.SparkSession
import java.io._

object SimpleApp {
  val categoryCodes : List[String] = List("edc", "gu", "mskb", "mff", "1dg", "mbf", "iib", "kfz", "mskc", "cz", "jna", "1de", "kfk", "ash", "tz", "rg1bl", "la", "rgz", "rg1bd", "bnj", "bnh", "bsb", "pk", "rg1bs", "tc", "bpa", "phda", "ckdg", "bib", "bic", "1fd", "knm", "fosf", "bnb", "ha", "kld", "phdb", "bpb", "fde", "cun", "k3z", "bph", "cih", "klh", "rg1af", "bona", "rg1ak", "klz", "rg1ao", "iz", "knb", "fdag", "ef", "taz", "taf", "ez", "ia", "kha", "tucc", "3fb", "kdb", "3fa", "fot", "aba", "mfyy", "tah", "paa", "pac", "phbb", "kn5", "blc", "bd", "be", "ba", "bmo", "kjz", "fj", "jok", "kvz", "knt", "bz", "krz", "zye", "knj", "tucf", "ilm", "rg1cf", "tuca", "kna", "knz", "ekc", "1cd", "idf", "kz", "bob", "knu", "cky", "pdb", "k3k", "kgd")
  //val categoryCodes : List[String] = List("bpb", "bpa", "kn5", "bnh", "taf", "bnb", "bnj", "ckdg", "rgz", "kdb", "knz", "mskb", "bona", "rg1af", "krz", "pdb", "bic", "kz", "bph", "mskc", "kfz", "cih", "kgd", "la", "phbb", "aba", "tah", "kjz", "cun", "kfk", "paa", "ash", "pac", "knu", "phda", "mff", "k3z", "rg1bd", "iz", "tucf", "3fb", "tucc", "kvz", "rg1cf", "rg1ak", "mbf", "kha", "1dg", "ilm", "ia", "knb", "ekc", "knt", "fdag", "klh", "mfyy", "bib", "iib", "k3k", "fot", "1fd", "3fa", "bob", "tuca", "bmo", "1cd", "rg1bs", "kld", "1de", "phdb", "rg1ao", "bsb", "knm", "knj", "rg1bl", "kna", "fosf", "klz")
  //  val categoryCodes : List[String] = List("t", "h", "k", "he", "bi", "kn", "kj", "kf", "pa","ge","mh","mf", "eg", "ac", "kk", "gc", "za", "bf", "eb", "j", "i", "cn", "eh", "tu","ee","m","f", "rdo", "kl", "ke", "epn", "rgd", "bc", "p", "x", "el", "fb", "ud", "ca", "tb","rdb", "th", "e", "r", "ec", "ez", "b", "c", "a", "v", "l", "rf", "eb","rg","cc","cb", "ipa", "kc", "ta", "bn", "z", "bs", "zb", "be", "rde", "cnn", "rd", "o", "bb", "ck","gl","gk", "ya", "g", "y", "u")
 // val categoryCodes : List[String] = List("t", "tc", "tz", "taz", "h", "k", "he", "bi", "kn", "kj", "kf", "pk", "pa","ge","mh","mf", "eg", "ac", "fj", "kk", "gc", "za", "bf", "be", "eb", "fde", "j", "i", "cz", "cn", "bd", "eh", "tu","ee","m","f", "rdo", "kl", "ke", "epn", "ha", "rgd", "bc", "bd", "p", "x", "ez", "el", "fb", "ud", "ca", "zye", "bz","tb","rdb","cky", "th", "e", "r", "ec", "ez", "edc", "jna", "jok", "b", "c", "a", "blc", "rc", "v", "l", "rf", "eb","rg","cc","cb", "ipa", "idf", "kc", "ta", "bn", "z", "bs", "zb", "be", "rde", "cnn", "rd", "o", "ba", "bb", "gu", "ck","gl","gk","ef", "ya", "g", "y", "u")
 // val categoryCodes : List[String] = List ("tc", "cnmie", "cnmi", "ich", "foy", "ffg", "he", "bi", "kn", "kj", "kf", "pk", "pa","msz","mh","mf", "acg", "ac", "fj", "fbea", "jbbc", "faf", "bf", "be", "bha", "fde", "j", "i", "cz", "cn", "bd", "rhadc", "rhaff","rhanu","rhage","rdj", "rdo", "rekf", "relo", "epn", "epnb", "jnbj", "jadm", "jnp", "jaed", "vbpc", "jafj", "bcfd", "bmfr", "bpm", "zkh", "zye", "zbv","cnmif","cnn","cky", "cnnf", "rg2df", "cnog", "cnol", "vbt", "ebuae", "jna", "jok", "b", "c", "a", "blc", "ybd", "ebcx", "cnmx", "rdbb", "fref","eeb","eha","egb", "ipa", "idf", "iok", "cknbc", "jryc", "imce", "imb", "ifz", "rdf", "rde", "rdb", "rd", "jus", "jrb", "jgb", "gu", "eei","gl","gk","gfc", "gek", "geb", "gck", "tab")
 // val categoryCodes : List[String] = List("tc", "foy")
  var productCounts : scala.collection.mutable.Map[String, Int] = scala.collection.mutable.Map()
  val productsPerCategory = 10
  var totalCount = 0
  var pCount : Long = 0

  def isMyCategory (code : String) : Boolean = {
    categoryCodes.contains(code)
  }

  def initialiseProductCounts() : Unit = {
    for  (code <- categoryCodes) {
      productCounts += (code -> 0)
    }
  }

  def isMyProduct(product: DBObject, bw: BufferedWriter) : Boolean = {
    pCount += 1
    val code = product.getAs[MongoDBObject]("category").get("code").toString
    if (isMyCategory(code) && productCounts(code) < productsPerCategory) {
//      productCounts.update(code, productCounts(code) + 1)
      productCounts(code) += 1
      totalCount += 1
      bw.write(product.toString + " ,\n")
      println(totalCount + ". product in total, " + productCounts(code) + ". product in category: " + code + ", " + pCount + ". in DB")
      println()
      return totalCount < categoryCodes.size * productsPerCategory
    }
    if(pCount % 100000 == 0) println("Running... " + pCount + ". product checked.")
    true
  }
  def main (args :Array[String]): Unit ={

//    val spark = SparkSession.builder()
//      .appName("The swankiest Spark app ever")
//      .master("local[*]")
//      .getOrCreate()
//
//    val uri = MongoClientURI("mongodb://ozyegin:123456@OSLDEVPTST01.host.gittigidiyor.net:27017/?authSource=document_store&authMechanism=SCRAM-SHA-1")
//    val mongoClient = MongoClient(uri)
//    val db = mongoClient("document_store")
//    // print(db.collectionNames())
//
//    val product_01 = db.apply("product_01")
//    val file = new File("C:\\Users\\miek\\Desktop\\products.bson")
//    val bw = new BufferedWriter(new FileWriter(file))
//    bw.write("[\n")
//    println("\n#########")
//    println(categoryCodes.length)
//    initialiseProductCounts()
//    print(productCounts)
//
//    println(product_01.size)
//    product_01.foreach(i => if (!isMyProduct(i, bw)) {println("\n#################################### DONE ####################################\n"); bw.write("]"); bw.close(); return})
//   }

}
