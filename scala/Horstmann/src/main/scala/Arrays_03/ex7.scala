package Arrays_03

object ex7 extends App {
  def unique(x: Array[Int]): Array[Int] = x.distinct

  assert(unique(Array(1, 3, 5, 7, 1, 5)).mkString(",") == "1,3,5,7")
}
