package Arrays_03

import collection.mutable.ArrayBuffer

object ex1 extends App {
  def append(n: Int) = {
    var x = ArrayBuffer[Int]()
    for (i <- 0 until n) x += i
    x
  }

  assert(append(5).mkString(",") == "0,1,2,3,4")
}
