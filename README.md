# gloop_vector_class
A simple vector class for python

  This module contains 3 classes, a 'vec2' class, a 'vec3' class, and a 'vec' class.
All of the vector types are mostly the same except their dimension; vec2 - as you might expect from the name - is a 2-dimensional vector, vec3 is 3, and vec is arbitrary.
To answer the obvious question of 'why not just have the 'vec' class', I wrote vec2 and vec3 first, and removing them would likely break a lot of the code I've written.
Additionally, I also suspect vec2 and vec3 to be faster, though that's complete conjecture.

  The usage of the vectors is fairly simple, they are like lists, but with operators such as '+', '*', '-', etc.
As an example, vec2(10,2)*vec2(1,5) returns vec2(10,10) whereas vec2(10,2)+vec2(1,5) returns vec2(11, 7)

  Note that you may only use operators on vectors (or a vector and a list or tuple) of the same length; a vec2 and vec3 cannot be multiplied.
However you may use an operator on any vector by an integer, float or Decimal to operate on every component by that value; for instance vec3(1,5,10)*5 returns vec3(5, 25, 50).

Also, there are functions beyond base operators, listed here:
  •the '@' operator - Dot product
  
  •'from_iterable' - a class method to create a vector from an iterable (such as a list or tuple)
  
  •'length' - the magnitude of the vector, or its distance from the origin (0,0,...)
  
  •'lerp' - linear interpolation between two vectors, syntax is 'a.lerp(b,factor)' where factor is a number from 0-1
  
  •'distance' - distance between two vectors, syntax is 'a.distance(b)'
  
  •'sign' - returns a vector with each component being the sign of the original (the sign being the 'positive-ness' of a number, -1 if it's negative, 0 if it's 0, and 1 if it's positive)
  
  •'in_box' - returns True if a vector is within the bounds defined by two vectors 'minimum' and 'maximum' with a flag to switch inclusivity (<= vs <).
      syntax is a.in_box(min,max,inclusive),inclusive is set by default to be 'True'.
      
  •'clamp' - returns a vector that is kept within the limits 'minimum' and 'maximum', syntax is 'a.clamp(min,max)'.
  
  •'len' - returns the length of the vector, for vec2 and vec3 this is always 2 or 3, respectively.
  
  •'cross' (only for vec2 and vec3) - returns the cross product of the vector.
