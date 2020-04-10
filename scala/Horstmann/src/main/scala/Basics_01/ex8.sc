import math.BigInt.probablePrime
import scala.util.Random

val x: BigInt = probablePrime(100, Random)

val y: String = x.toString(36)