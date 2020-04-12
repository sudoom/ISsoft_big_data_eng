package Arrays_03

object ex3 extends App {
  def change(x: Array[Int]) = {
    for (i <- x.indices) yield
      if (i % 2 == 0 && i + 1 == x.length) x(i)
      else if (i % 2 == 0) x(i + 1)
      else x(i - 1)

  }.toArray

  assert(change(Array(1, 2, 3, 4, 5)).mkString(",") == "2,1,4,3,5")
  assert(change(Array(1, 2, 3, 4)).mkString(",") == "2,1,4,3")

}