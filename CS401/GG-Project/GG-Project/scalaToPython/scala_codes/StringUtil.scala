package util

/**
  * Created by miek on 07.12.2016.
  */
object StringUtil {

  /* original title data stored as hex encoding to avoid invalid chars
        this method decodes hex encoded strings */
  def unhex(hexStr: String) = {
    new String(javax.xml.bind.DatatypeConverter.parseHexBinary(hexStr), "ISO-8859-9")
  }

  def normalizeKeyword(keyword: String): String = {
    if (keyword == null) return ""
    keyword.replaceAll("  ", " ")
      .toLowerCase()
      .trim
  }

  def getFixedEncodingValue(encoded: String): String = {
    if (encoded == null) return null
    encoded
      .replaceAll("%C3%84%C2%9E", "%C4%9E") // Ğ
      .replaceAll("%C3%84%C2%9F", "%C4%9F") // ğ
      .replaceAll("%C3%83%C2%87", "%C3%87") // Ç
      .replaceAll("%C3%83%C2%A7", "%C3%A7") // ç
      .replaceAll("%C3%83%C2%96", "%C3%96") // Ö
      .replaceAll("%C3%83%C2%B6", "%C3%B6") // ö
      .replaceAll("%C3%83%C2%9C", "%C3%9C") // Ü
      .replaceAll("%C3%83%C2%BC", "%C3%BC") // ü
      .replaceAll("%C3%84%C2%B0", "%C4%B0") // İ
      .replaceAll("%C3%84%C2%B1", "%C4%B1") // ı
      .replaceAll("%C3%85%C2%9E", "%C5%9E") // Ş
      .replaceAll("%C3%85%C2%9F", "%C5%9F") // ş
      .replaceAll("%C3%AF%C2%BF%C2%BD", "%C5%9F") // ş?
  }

  def convertTrChars(str: String): String = {
    if (str == null) return null
    str
      .replaceAll("\u00FC", "u")
      .replaceAll("\u00DC", "U")
      .replaceAll("\u00D6", "O")
      .replaceAll("\u00F6", "o")
      .replaceAll("\u015E", "S")
      .replaceAll("\u015F", "s")
      .replaceAll("\u011E", "G")
      .replaceAll("\u011F", "g")
      .replaceAll("\u0131", "i")
      .replaceAll("\u0130", "I")
      .replaceAll("\u00E7", "c")
      .replaceAll("\u00C7", "C")
  }

  def cleanUpAlpha(str: String): String = {
    str.replaceAll("[^\\p{L}0-9]+", " ").trim
  }

  def convertAscii(str: String): String = {
    convertTrChars(str).toLowerCase.replaceAll("[^a-z0-9]+", "")
  }

  def convertAsciiWithoutTrChars(str: String): String = {
    str.toLowerCase.replaceAll("[^a-z0-9]+", "")
  }

  def convertAsciiWithTrChars(str: String): String = {
    str.toLowerCase.trim.replaceAll("[^a-zöçşığü0-9 ]+", " ")
  }

  def removeVowels(str: String): String = {
    convertTrChars(str).replaceAll("[aeiuoAEIOU]+", "")
  }

}