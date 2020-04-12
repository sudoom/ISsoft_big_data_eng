package Structures_02

object ex9 extends App {
  def product(s: String): Long = {
    if (s.tail != "") s.head.toLong * product(s.tail)
    else s.head.toLong
  }

  assert(product("Hello") == 9415087488L)
}
