package Structures_02

object ex5 extends App {
  def countdown(n: Int): Unit = {
    for (i <- n to 0 by -1) println(i)
  }

  countdown(10)
}
