package Arrays_03

import scala.collection.mutable.ArrayBuffer

object ex6 extends App {
  def sortDescArray(x: Array[Int]): Array[Int] = x.sorted.reverse

  def sortDescBuffArray(x: ArrayBuffer[Int]): ArrayBuffer[Int] = x.sorted.reverse

  assert(sortDescArray(Array(1, 5, 3, 2, 4, 1)).mkString(",") == "5,4,3,2,1,1")
  assert(sortDescBuffArray(ArrayBuffer(1, 5, 3, 2, 4, 1)).mkString(",") == "5,4,3,2,1,1")
}
