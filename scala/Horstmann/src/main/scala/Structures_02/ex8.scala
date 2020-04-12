package Structures_02

object ex8 extends App {
  def product(s: String) = {
    var result: Long = 1
    for (chr <- s) result *= chr.toInt
    result
  }

  assert(product("Hello") == 9415087488L)
}
