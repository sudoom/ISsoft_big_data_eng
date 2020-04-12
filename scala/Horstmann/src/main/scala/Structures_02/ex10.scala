package Structures_02

import math.pow

object ex10 extends App {
  def powers(x: Double, n: Int): Double = {
    if (n < 0) 1 / pow(x, -n)
    else if (n > 0 && n % 2 == 0) pow(pow(x, n / 2), 2)
    else if (n > 0 && n % 2 == 1) x * pow(x, n - 1)
    else 1

  }

  assert(powers(2, 10) == 1024D)
  assert(powers(2, 5) == 32D)
  assert(powers(2, 0) == 1D)
  assert(powers(2, -8) == 0.00390625)
}
