package Arrays_03

object ex4 extends App {
  def swap(x: Array[Int]): Array[Int] = x.filter(_ > 0) ++ x.filter(_ < 0) ++ x.filter(_ == 0)

  assert(swap(Array(3, 4, 2, -5, 1, 0, -7)).mkString(",") == "3,4,2,1,-5,-7,0")
}
