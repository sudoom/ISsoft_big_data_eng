package Arrays_03

object ex2 extends App {
  def change(x: Array[Int]): Array[Int] = {
    for (i <- 1 until x.length by 2) {
      var tmp = x(i)
      x(i) = x(i - 1)
      x(i - 1) = tmp
    }
    x
  }

  assert(change(Array(1, 2, 3, 4, 5)).mkString(",") == "2,1,4,3,5")
  assert(change(Array(1, 2, 3, 4)).mkString(",") == "2,1,4,3")

}
