import math,operator,numbers
#by _gloop / gloop#5445
class vec:
    def __init__(self, *components):
        if len(components):
            components_copy = []
            for c in components:
                if isinstance(c,(vec,vec2,vec3,list,tuple)):
                    components_copy += [i for i in c]
                else:
                    components_copy += [c]
            components = components_copy
            for c in components:
                if not isinstance(c,numbers.Real):
                    raise ValueError(f"\"{c}\" is non-numeric")
            self.components = list(components)
        else:
            raise ValueError("A vector must have at least one component")
    @classmethod
    def from_iterable(cls,iterable):
        return cls(*iterable)
    def __iter__(self):
        yield from self.components
    def __repr__(self):
        return f"vec{tuple(self.components)}"
    def __getitem__(self,items):
        return self.components[items]
    def __setitem__(self,items,values):
        self.components[items] = values
    def __delitem__(self,items):
        del self.components[items]
    def __hash__(self):
        return hash(tuple(self.components))
    def __contains__(self,val):
        return any(i==val for i in self.components)
    def __bool__(self):
        return any(self.components)
    def length(self):
        return math.sqrt(sum(x**2 for x in self.components))
    def lerp(self,other,t):
        lerped_vec = []
        for (i_self,i_other) in zip(self.components,other.components):
            lerped_vec+=[(1-t)*i_self+t*i_other]
        return vec(lerped_vec)
    def distance(self,other):
        return math.dist(self,other)
    def distance2(self,other):
        return sum((self-other)**2)
    def normalize(self):
        return self/self.length()
    def sign(self):
        sign_vec = [1 if i>0 else -1 if i<0 else 0 for i in self.components] 
        return vec(sign_vec)
    def in_box(self,minimum,maximum,inclusive=True):
        if inclusive:
            return all([i_min<i_self<i_max for i_min,i_self,i_max in zip(minimum,self,maximum)])
        else:
            return all([i_min<=i_self<=i_max for i_min,i_self,i_max in zip(minimum,self,maximum)])
        
    def clamp(self,min_,max_):
        clamped_vec = []
        for i_min,i_self,i_max in zip(min_,self,max_):
            clamped_vec.append(i_min if i_self<i_min else i_max if i_self>i_min else i_self)
        return vec(clamped_vec)    
    def __matmul__(self,other):
        n = 0
        for i_self in self:
            for i_other in other:
                n+=(i_self*i_other)
        return n
    def __len__(self):
        return len(self.components)
    def _equality_op(op):
        def _vec_op(a,b):
            if isinstance(b,(vec,vec2,vec3)):
                if len(b)==len(a):
                    return all([op(i_a,i_b) for i_a,i_b in zip(a,b)])
                else:
                    raise TypeError("Vectors must have the same number of components")
            if isinstance(b,(list,tuple)):
                return all([op(i,b[idx]) for idx,i in enumerate(a)])
            if isinstance(b,numbers.Real):
                return all([op(i,b) for i in a])
        return _vec_op
    def _dual_op(op):
        def _vec_op(a,b):
            if isinstance(b,(vec,vec2,vec3)):
                if len(b)==len(a):
                    new_vector = [op(i_a,i_b) for i_a,i_b in zip(a,b)]
                    return vec(new_vector)
                else:
                    raise TypeError("Vectors must have the same number of components")
            if isinstance(b,(list,tuple)):
                new_vector = [op(i,b[idx]) for idx,i in enumerate(a)]
                return vec(new_vector)
            if isinstance(b,numbers.Real):
                new_vector = [op(i,b) for i in a]
                return vec(new_vector)
        return _vec_op
    def _single_op(op):
        def _vec_op(a):
            new_vector = [op(i) for i in a]
            return vec(new_vector)
        return _vec_op
    __eq__ = _equality_op(operator.eq)
    __lt__ = _equality_op(operator.lt)
    __le__ = _equality_op(operator.le)
    __gt__ = _equality_op(operator.gt)
    __ge__ = _equality_op(operator.ge)
    __ne__ = _equality_op(operator.ne)

    __rmul__ = _dual_op(operator.mul)
    __radd__ = _dual_op(operator.add)
    __rsub__ = _dual_op(operator.sub)
    __rtruediv__ = _dual_op(operator.truediv)
    __rfloordiv__ = _dual_op(operator.floordiv)
    __rmod__ = _dual_op(operator.mod)
    __rpow__ = _dual_op(operator.pow)

    __mul__ = _dual_op(operator.mul)
    __add__ = _dual_op(operator.add)
    __sub__ = _dual_op(operator.sub)
    __truediv__ = _dual_op(operator.truediv)
    __floordiv__ = _dual_op(operator.floordiv)
    __mod__ = _dual_op(operator.mod)
    __pow__ = _dual_op(operator.pow)
    __floor__ = _single_op(math.floor) 
    __round__ = _single_op(round)
    __ceil__ = _single_op(math.ceil)
    __trunc__ = _single_op(math.trunc)
    __abs__ = _single_op(abs)
    __neg__ = _single_op(operator.neg)
    __pos__ = _single_op(operator.pos)

class vec3:
    def __init__(self, *components):
        if len(components):
            components_copy = []
            for c in components:
                
                if isinstance(c,(vec,vec2,vec3,list,tuple)):
                    components_copy += [i for i in c]
                else:
                    components_copy += [c]
            components = components_copy[:3]
            if not len(components)>2:
                raise ValueError("Vec3 requires three components")
        else:
            raise ValueError("Vec3 requires at least one component")
        for c in components:
            if not isinstance(c,numbers.Real):
                raise ValueError(f"\"{c}\" is non-numeric")
        self.x, self.y, self.z = components
    
    @classmethod
    def from_iterable(cls,iterable):
        return cls(*iterable)
    def __iter__(self):
        yield from (self.x,self.y,self.z)
    def __repr__(self):
        return f"vec3({self.x}, {self.y}, {self.z})"
    def __getitem__(self,items):
        return list(self)[items]
    def __setitem__(self,items,values):
        components = list(self)
        components[items] = values
        self.x,self.y,self.z = components
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def __contains__(self,val):
        return bool(self.x == val or self.y == val or self.z == val)
    def __bool__(self):
        return bool(self.x or self.y or self.z)
    def length(self):
        return math.hypot(self.x,self.y,self.y)
    def lerp(self,other,t):
        return vec3(
            (1-t)*self.x+t*other.x,
            (1-t)*self.y+t*other.y,
            (1-t)*self.z+t*other.z
            )
    def distance(self,other):
        return math.dist(self,other)
    def distance2(self,other):
        return sum((self-other)**2)
    def normalize(self):
        return self/self.length()
    def sign(self):
        return vec3(
        1 if self.x>0 else -1 if self.x<0 else 0,
        1 if self.y>0 else -1 if self.y<0 else 0,
        1 if self.z>0 else -1 if self.z<0 else 0
        )
    def in_box(self,minimum,maximum,inclusive=True):
        min_x,min_y,min_z = minimum
        max_x,max_y,max_z = maximum
        if inclusive:
            return min_x<=self.x<=max_x and min_y<=self.y<=max_y and min_z<=self.z<=max_z
        else:
            return min_x<self.x<max_x and min_y<self.y<max_y and min_z<self.y<max_z
    def clamp(self,min_,max_):
        clamped_vec = []
        for i_min,i_self,i_max in zip(min_,self,max_):
            clamped_vec.append(i_min if i_self<i_min else i_max if i_self>i_min else i_self)
        return vec(clamped_vec)
    def __matmul__(self,other):
        n = 0
        for i_self in self:
            for i_other in other:
                n+=(i_self*i_other)
        return n
    def cross(self,other):
        return vec3(
            self.y*other.z - self.z*other.y,
            self.z*other.x - self.x*other.z,
            self.x*other.y - self.y*other.x
        )
    def __len__(self):
        return 3
    def _equality_op(op):
        def _vec_op(a,b):
            if isinstance(b,vec3):
                return op(a.x,b.x) and op(a.y,b.y) and op(a.z,b.z)
            if isinstance(b,(list,tuple,vec)) and len(b)>2:
                return op(a.x,b[0]) and op(a.y,b[1]) and op(a.z,b[2])
            if isinstance(b,numbers.Real):
                return op(a.x,b) and op(a.y,b) and op(a.z,b)
        return _vec_op
    def _dual_op(op):
        def _vec_op(a,b):
            if isinstance(b,vec3):
                return vec3(op(a.x,b.x), op(a.y,b.y), op(a.z,b.z))
            if isinstance(b,(list,tuple,vec)) and len(b)>2:
                return vec3(op(a.x,b[0]), op(a.y,b[1]), op(a.z,b[2]))
            if isinstance(b,numbers.Real):
                return vec3(op(a.x,b), op(a.y,b), op(a.z,b))
        return _vec_op
    def _single_op(op):
        def _vec_op(a):
            return vec3(op(a.x), op(a.y), op(a.z))
        return _vec_op
    __eq__ = _equality_op(operator.eq)
    __lt__ = _equality_op(operator.lt)
    __le__ = _equality_op(operator.le)
    __gt__ = _equality_op(operator.gt)
    __ge__ = _equality_op(operator.ge)
    __ne__ = _equality_op(operator.ne)

    __rmul__ = _dual_op(operator.mul)
    __radd__ = _dual_op(operator.add)
    __rsub__ = _dual_op(operator.sub)
    __rtruediv__ = _dual_op(operator.truediv)
    __rfloordiv__ = _dual_op(operator.floordiv)
    __rmod__ = _dual_op(operator.mod)
    __rpow__ = _dual_op(operator.pow)

    __mul__ = _dual_op(operator.mul)
    __add__ = _dual_op(operator.add)
    __sub__ = _dual_op(operator.sub)
    __truediv__ = _dual_op(operator.truediv)
    __floordiv__ = _dual_op(operator.floordiv)
    __mod__ = _dual_op(operator.mod)
    __pow__ = _dual_op(operator.pow)
    __floor__ = _single_op(math.floor) 
    __round__ = _single_op(round)
    __ceil__ = _single_op(math.ceil)
    __trunc__ = _single_op(math.trunc)
    __abs__ = _single_op(abs)
    __neg__ = _single_op(operator.neg)
    __pos__ = _single_op(operator.pos)

class vec2:
    def __init__(self, *components):
        if len(components):
            components_copy = []
            for c in components:
                if isinstance(c,(vec,vec2,vec3,list,tuple)):
                    components_copy += [i for i in c]
                else:
                    components_copy += [c]
            components = components_copy[:2]
            if not len(components)>1:
                raise ValueError("Vec2 requires two components")
        else:
            raise ValueError("Vec2 requires at least one component")
        components = components[:2]
        for i in components:
            if not isinstance(i,numbers.Real):
                raise ValueError(f"\"{i}\" is non-numeric")
        self.x, self.y = components

    @classmethod
    def from_iterable(cls,iterable):
        return cls(*iterable)
    def __iter__(self):
        yield from (self.x,self.y)
    def __repr__(self):
        return f"vec2({self.x}, {self.y})"
    def __getitem__(self,items):
        return list(self)[items]
    def __setitem__(self,items,values):
        components = list(self)
        components[items] = values
        self.x,self.y = components
    def __hash__(self):
        return hash((self.x, self.y))
    def __contains__(self,val):
        return bool(self.x == val or self.y == val)
    def __bool__(self):
        return bool(self.x or self.y)
    def length(self):
        return math.hypot(self.x,self.y)
    def lerp(self,other,t):
        return vec2((1-t)*self.x+t*other.x,(1-t)*self.y+t*other.y)
    def distance(self,other):
        return math.dist(self,other)
    def distance2(self,other):
        return sum((self-other)**2)
    def sign(self):
        return vec2(
        1 if self.x>0 else -1 if self.x<0 else 0,
        1 if self.y>0 else -1 if self.y<0 else 0
        )
    def in_box(self,minimum,maximum,inclusive=True):
        min_x,min_y = minimum
        max_x,max_y = maximum
        if inclusive:
            return min_x<=self.x<=max_x and min_y<=self.y<=max_y
        else:
            return min_x<self.x<max_x and min_y<self.y<max_y

    def clamp(self,min_,max_):
        clamped_vec = []
        for i_min,i_self,i_max in zip(min_,self,max_):
            clamped_vec.append(i_min if i_self<i_min else i_max if i_self>i_min else i_self)
        return vec(clamped_vec)

    def __matmul__(self,other):
        n = 0
        for i_self in self:
            for i_other in other:
                n+=(i_self*i_other)
        return n
    
    def cross(self,other):
        return (self.x*other.y)-(self.y*other.x)
    def __len__(self):
        return 2
    def _equality_op(op):
        def _vec_op(a,b):
            if isinstance(b,vec2):
                return op(a.x,b.x) and op(a.y,b.y)
            if isinstance(b,(list,tuple,vec)) and len(b)>1:
                return op(a.x,b[0]) and op(a.y,b[1])
            if isinstance(b,numbers.Real):
                return op(a.x,b) and op(a.y,b)
        return _vec_op
    def _dual_op(op):
        def _vec_op(a,b):
            if isinstance(b,vec2):
                return vec2(op(a.x,b.x), op(a.y,b.y))
            if isinstance(b,(list,tuple,vec)) and len(b)>1:
                return vec2(op(a.x,b[0]), op(a.y,b[1]))
            if isinstance(b,numbers.Real):
                return vec2(op(a.x,b), op(a.y,b))
        return _vec_op
    def _single_op(op):
        def _vec_op(a):
            return vec2(op(a.x), op(a.y))
        return _vec_op
    __eq__ = _equality_op(operator.eq)
    __lt__ = _equality_op(operator.lt)
    __le__ = _equality_op(operator.le)
    __gt__ = _equality_op(operator.gt)
    __ge__ = _equality_op(operator.ge)
    __ne__ = _equality_op(operator.ne)

    __rmul__ = _dual_op(operator.mul)
    __radd__ = _dual_op(operator.add)
    __rsub__ = _dual_op(operator.sub)
    __rtruediv__ = _dual_op(operator.truediv)
    __rfloordiv__ = _dual_op(operator.floordiv)
    __rmod__ = _dual_op(operator.mod)
    __rpow__ = _dual_op(operator.pow)

    __mul__ = _dual_op(operator.mul)
    __add__ = _dual_op(operator.add)
    __sub__ = _dual_op(operator.sub)
    __truediv__ = _dual_op(operator.truediv)
    __floordiv__ = _dual_op(operator.floordiv)
    __mod__ = _dual_op(operator.mod)
    __pow__ = _dual_op(operator.pow)
    __floor__ = _single_op(math.floor) 
    __round__ = _single_op(round)
    __ceil__ = _single_op(math.ceil)
    __trunc__ = _single_op(math.trunc)
    __abs__ = _single_op(abs)
    __neg__ = _single_op(operator.neg)
    __pos__ = _single_op(operator.pos)

vector = vec | vec2 | vec3 

