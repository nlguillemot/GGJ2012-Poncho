import vector2
from math import fabs

def AABB_2d_collide(x1,y1,w1,h1,x2,y2,w2,h2):
	if(y1+h1 < y2):
		return False
	elif(y1 > y2+h2):
		return False
	elif(x1+w1 < x2):
		return False
	elif(x1 > x2+w2):
		return False
	else:
		return True
	
def AABB_1d_collide(x1,w1,x2,w2):
	if(x1+w1 < x2):
		return False
	elif(x1 > x2+w2):
		return False
	else:
		return True

def AABB_intersection_depth(x1,y1,w1,h1,x2,y2,w2,h2):
	halfw1 = w1/2.0
	halfh1 = h1/2.0
	halfw2= w2/2.0
	halfh2 = h2/2.0
	center1 = vector2.vector2(x1 + halfw1, y1 + halfh1)
	center2 = vector2.vector2(x2 + halfw2, y2 + halfh2)
	distX = center1.x - center2.x
	distY = center1.y - center2.y
	minDistX = halfw1 + halfw2
	minDistY = halfh1 + halfh2
	
	if(fabs(distX) >= minDistX or fabs(distY) >= minDistY):
		return vector2.vector2(0,0)
	if(distX > 0):
		depthX = minDistX - distX
	else:
		depthX = -minDistX - distX
	if(distY > 0):
		depthY = minDistY - distY
	else:
		depthY = -minDistY - distY
	
	return vector2.vector2(depthX,depthY)

