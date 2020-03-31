/*
Напишите программу, которая считывает построчно два целых числа и считает их разницу.
Подсказка: для считывания целого числа из строки во входном потоке можно воспользоваться методом readInt() объекта StdIn.

Sample Input:
8
11

Sample Output:
-3

 */


import scala.io.StdIn.readInt

object test extends App {
  val x = readInt()
  val y = readInt()
  println(x - y)
}