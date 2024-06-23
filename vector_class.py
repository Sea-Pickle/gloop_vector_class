import math,operator,numbers
#by _gloop / gloop#5445

class vec:
	def __init__(self,*components:numbers.Real,truncate:bool=False,strict:bool=True):
		if components:
			self.components = []
			for c in components:
				if isinstance(c,(vector,list,tuple)):
					for i in c:
						if strict:
							if not isinstance(i,numbers.Real): raise ValueError(f'"{i}" of type "{type(i).__name__}" is non-numeric')
						self.components.append(i)
				else:
					if strict:
						if not isinstance(c,numbers.Real): raise ValueError(f'"{c}" of type "{type(c).__name__}" is non-numeric')
					self.components.append(c)

			if self.__class__!=vec:
				if len(self.components)==1:
					self.components*=self.__len__()
				if truncate:
					if len(self.components)>self.__len__():
						self.components = self.components[:self.__len__()]
			
			if len(self.components) != self.__len__():
				raise ValueError(f"Wrong number of components {len(self.components)} for {self.__class__}")
		else:
			raise ValueError("A vector must have at least one component")
	@classmethod
	def from_iterable(cls,iterable) -> "vec":
		return cls(*iterable)
	
	def __iter__(self): yield from self.components

	def __repr__(self) -> str: return f"vec{tuple(self.components)}"
	
	def __getitem__(self,items): return self.components[items]
	
	def __setitem__(self,items,values) -> None: self.components[items] = values
	
	def __delitem__(self,items) -> None: del self.components[items]
	
	def __hash__(self) -> int: return hash(tuple(self.components))
	
	def __contains__(self,val) -> bool: return any(i==val for i in self.components)
	
	def __bool__(self,strict:bool=False) -> bool:
		if strict:
			return all(self.components)
		return any(self.components)

	def length(self) -> float: return math.sqrt(sum(x**2 for x in self.components))

	def lerp(self,other,t) -> "vec":
		lerped_vec = []
		for (i_self,i_other) in zip(self.components,other.components):
			lerped_vec+=[(1-t)*i_self+t*i_other]
		return self.__class__(lerped_vec)
	
	def distance(self,other:"vec3") -> float: return math.dist(self,other)
	
	def distance2(self,other:"vec3") -> float: return sum((self-other)**2)
	
	def normalize(self) -> "vec": return self/self.length()

	def sign(self) -> "vec":
		sign_vec = [1 if i>0 else -1 if i<0 else 0 for i in self.components] 
		return self.__class__(sign_vec)
	
	def in_box(self,minimum:"vec",maximum:"vec",inclusive:bool=True) -> bool:
		if inclusive:
			return all([i_min<i_self<i_max for i_min,i_self,i_max in zip(minimum,self,maximum)])
		else:
			return all([i_min<=i_self<=i_max for i_min,i_self,i_max in zip(minimum,self,maximum)])

	def clamp(self,min_,max_) -> "vec":
		clamped_vec = []
		for i_min,i_self,i_max in zip(min_,self,max_):
			clamped_vec.append(i_min if i_self<i_min else i_max if i_self>i_max else i_self)
		return self.__class__(clamped_vec)

	def __matmul__(self,other:"vec3") -> float:
		n = 0
		for i_self in self:
			for i_other in other:
				n+=(i_self*i_other)
		return n
	
	def __len__(self) -> int:
		return len(self.components)
	
	def floor(self) -> "vec":
		return self.__class__([math.floor(i) for i in self.components])

	def ceil(self) -> "vec":
		return self.__class__([math.ceil(i) for i in self.components])

	def _equality_op(op) -> bool:
		def _vec_op(a,b):
			if isinstance(b,vector):
				if len(b)==len(a): return all([op(i_a,i_b) for i_a,i_b in zip(a,b)])
				raise TypeError(f"Vectors {a} and {b} are not the same length")
			if isinstance(b,(list,tuple)): return all([op(i,b[idx]) for idx,i in enumerate(a)])
			if isinstance(b,numbers.Real): return all([op(i,b) for i in a])
		return _vec_op

	def _dual_op(op) -> "vec":
		def _vec_op(a,b):
			if isinstance(b,vector):
				if len(b)==len(a):
					new_vector = [op(i_a,i_b) for i_a,i_b in zip(a,b)]
					return a.__class__(new_vector)
				else:
					raise TypeError(f"Vectors {a} and {b} are not the same length")
			if isinstance(b,(list,tuple)):
				new_vector = [op(i,b[idx]) for idx,i in enumerate(a)]
				return a.__class__(new_vector)
			if isinstance(b,numbers.Real):
				new_vector = [op(i,b) for i in a]
				return a.__class__(new_vector)
		return _vec_op
	
	def _single_op(op) -> "vec":
		def _vec_op(a):
			new_vector = [op(i) for i in a]
			return a.__class__(new_vector)
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
	__floor__ = _single_op(floor)
	__round__ = _single_op(round)
	__ceil__ = _single_op(ceil)
	__trunc__ = _single_op(math.trunc)
	__abs__ = _single_op(abs)
	__neg__ = _single_op(operator.neg)
	__pos__ = _single_op(operator.pos)

class vec2(vec):
	def __repr__(self) -> str:
		return f"vec2{tuple(self.components)}"
	
	def __getattr__(self, attr):
		if attr in ["x","X"]: return self.components[0]
		if attr in ["y","Y"]: return self.components[1]

	def __setattr__(self,attr,value) -> None:
		if attr in ["x","X"]:
			if not isinstance(value,numbers.Real):
				raise ValueError(f'"{value}" of type {type(value).__name__} is non-numeric')
			else:
				self.components[0] = value
		if attr in ["y","Y"]:
			if not isinstance(value,numbers.Real):
				raise ValueError(f'"{value}" of type {type(value).__name__} is non-numeric')
			else:
				self.components[1] = value
		else:
			self.__dict__[attr] = value

	def cross(self,other) -> float:
		return (self[0]*other[1])-(self[1]*other[0])

	def __len__(self) -> int:
		return 2

	def rotate(self,angle) -> "vec2": #2d rotation matrix done manually (probably temporary)
		ct,st = math.cos(angle),math.sin(angle)
		return vec2(
			(self.x*ct)-(self.y*st),
			(self.x*st)+(self.y*ct)
		)

class vec3(vec):
	def __repr__(self) -> str:
		return f"vec3{tuple(self.components)}"
	
	def __getattr__(self, attr):
		if attr in ["x","X"]: return self.components[0]
		if attr in ["y","Y"]: return self.components[1]
		if attr in ["z","Z"]: return self.components[2]
	
	def __setattr__(self,attr,value):
		if attr in ["x","X"]:
			if not isinstance(value,numbers.Real):
				raise ValueError(f'"{value}" of type "{type(value).__name__}" is non-numeric')
			else:
				self.components[0]=value
		if attr in ["y","Y"]:
			if not isinstance(value,numbers.Real):
				raise ValueError(f'"{value}" of type "{type(value).__name__}" is non-numeric')
			else:
				self.components[1]=value
		if attr in ["z","Z"]:
			if not isinstance(value,numbers.Real):
				raise ValueError(f'"{value}" of type "{type(value).__name__}" is non-numeric')
			else:
				self.components[2]=value
		else:
			self.__dict__[attr] = value
	
	def cross(self,other:"vec3") -> "vec3":
		self_x,self_y,self_z = self
		other_x,other_y,other_z = other
		return vec3(
			self_y*other_z - self_z*other_y,
			self_z*other_x - self_x*other_z,
			self_x*other_y - self_y*other_x
		)
	
	def __len__(self) -> int:
		return 3

vector = vec | vec2 | vec3
