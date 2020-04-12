package Structures_02

object ex6 extends App {
  var multiply: Long = 1
  for (chr <- "Hello") multiply *= chr.toInt
  assert(multiply == 9415087488L)
}
