package Structures_02

object ex1 extends App {
  def sgn(x: Int) = {
    if (x > 0) 1
    else if (x < 0) -1
    else 0
  }

  assert(sgn(5) == 1)
  assert(sgn(-5) == -1)
  assert(sgn(0) == 0)
}
