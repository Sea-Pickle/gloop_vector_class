import math,operator,numbers
#by _gloop / gloop#5445
class vec:
    def __init__(self, *components):
        if len(components):
            components_copy = []
            for c in components:

                if isinstance(c,(vector,list,tuple)):

                    components_copy += [i for i in c]
                elif isinstance(c,complex):
                    components_copy += [c.real,c.imag]
                else:
                    components_copy += [c]
            components = list(components_copy)
            print(components)
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
            clamped_vec.append(i_min if i_self<i_min else i_max if i_self>i_max else i_self)
        return vec(clamped_vec)    
    def __reversed__(self):
        return vec(self[::-1])
    def __complex__(self):
        return complex(self[0],self[1])
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
            if isinstance(b,vector):
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
            if isinstance(b,vector):
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

    sin = _single_op(math.sin)
    cos = _single_op(math.cos)
    tan = _single_op(math.tan)

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

class vec2(vec):
    def __repr__(self):
        return f"vec2{tuple(self.components)}"
    def __getattr__(self, attr):
        if attr in ["x","X"]:
            return self.components[0]
        if attr in ["y","Y"]:
            return self.components[1]
        
    def __setattr__(self,attr,value):
        if attr in ["x","X"]:
            if not isinstance(value,numbers.Real):
                raise ValueError(f"\"{value}\" is non-numeric")
            else:
                self.components[0]=value
        if attr in ["y","Y"]:
            if not isinstance(value,numbers.Real):
                raise ValueError(f"\"{value}\" is non-numeric")
            else:
                self.components[1]=value
        else:
            self.__dict__[attr] = value
    def cross(self,other):
        return (self.x*other[1])-(self[1]*other.x)
    def __len__(self):
        return 2
    def clamp(self,min_,max_):
        clamped_vec = []
        for i_min,i_self,i_max in zip(min_,self,max_):
            clamped_vec.append(i_min if i_self<i_min else i_max if i_self>i_max else i_self)
        return vec2(clamped_vec) 
    def __reversed__(self):
        return vec2(self[::-1])
    def _dual_op(op):
        def _vec_op(a,b):
            if isinstance(b,vector):
                if len(b)==len(a):
                    new_vector = [op(i_a,i_b) for i_a,i_b in zip(a,b)]
                    return vec2(new_vector)
                else:
                    raise TypeError("Vectors must have the same number of components")
            if isinstance(b,(list,tuple)):
                new_vector = [op(i,b[idx]) for idx,i in enumerate(a)]
                return vec2(new_vector)
            if isinstance(b,numbers.Real):
                new_vector = [op(i,b) for i in a]
                return vec2(new_vector)
        return _vec_op
    def _single_op(op):
        def _vec_op(a):
            new_vector = [op(i) for i in a]
            return vec2(new_vector)
        return _vec_op
    __rmul__ = _dual_op(operator.mul)
    __radd__ = _dual_op(operator.add)
    __rsub__ = _dual_op(operator.sub)
    __rtruediv__ = _dual_op(operator.truediv)
    __rfloordiv__ = _dual_op(operator.floordiv)
    __rmod__ = _dual_op(operator.mod)
    __rpow__ = _dual_op(operator.pow)

    sin = _single_op(math.sin)
    cos = _single_op(math.cos)
    tan = _single_op(math.tan)

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

class vec3(vec):
    def __repr__(self):
        return f"vec3{tuple(self.components)}"
    def __getattr__(self, attr):
        if attr in ["x","X"]:
            return self.components[0]
        if attr in ["y","Y"]:
            return self.components[1]
        if attr in ["z","Z"]:
            return self.components[2]
        
    def __setattr__(self,attr,value):
        if attr in ["x","X"]:
            if not isinstance(value,numbers.Real):
                raise ValueError(f"\"{value}\" is non-numeric")
            else:
                self.components[0]=value
        if attr in ["y","Y"]:
            if not isinstance(value,numbers.Real):
                raise ValueError(f"\"{value}\" is non-numeric")
            else:
                self.components[1]=value
        if attr in ["z","Z"]:
            if not isinstance(value,numbers.Real):
                raise ValueError(f"\"{value}\" is non-numeric")
            else:
                self.components[2]=value
        else:
            self.__dict__[attr] = value
    def cross(self,other):
        self_x,self_y,self_z = self
        other_x,other_y,other_z = other
        return vec3(
            self_y*other_z - self_z*other_y,
            self_z*other_x - self_x*other_z,
            self_x*other_y - self_y*other_x
        )
    def __len__(self):
        return 3
    def clamp(self,min_,max_):
        clamped_vec = []
        for i_min,i_self,i_max in zip(min_,self,max_):
            clamped_vec.append(i_min if i_self<i_min else i_max if i_self>i_max else i_self)
        return vec3(clamped_vec)   
    def __reversed__(self):
        return vec3(self[::-1])
    def _dual_op(op):
        def _vec_op(a,b):
            if isinstance(b,vector):
                if len(b)==len(a):
                    new_vector = [op(i_a,i_b) for i_a,i_b in zip(a,b)]
                    return vec3(new_vector)
                else:
                    raise TypeError("Vectors must have the same number of components")
            if isinstance(b,(list,tuple)):
                new_vector = [op(i,b[idx]) for idx,i in enumerate(a)]
                return vec3(new_vector)
            if isinstance(b,numbers.Real):
                new_vector = [op(i,b) for i in a]
                return vec3(new_vector)
        return _vec_op
    def _single_op(op):
        def _vec_op(a):
            new_vector = [op(i) for i in a]
            return vec3(new_vector)
        return _vec_op
    __rmul__ = _dual_op(operator.mul)
    __radd__ = _dual_op(operator.add)
    __rsub__ = _dual_op(operator.sub)
    __rtruediv__ = _dual_op(operator.truediv)
    __rfloordiv__ = _dual_op(operator.floordiv)
    __rmod__ = _dual_op(operator.mod)
    __rpow__ = _dual_op(operator.pow)

    sin = _single_op(math.sin)
    cos = _single_op(math.cos)
    tan = _single_op(math.tan)

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
