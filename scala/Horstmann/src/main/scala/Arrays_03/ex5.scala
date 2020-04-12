package Arrays_03

object ex5 extends App {
  def meanArray(x: Array[Double]): Double = x.sum / x.length

  assert(meanArray(Array(2.5, 2.1, 12, 3.6, 34)) == 10.84D)
}
