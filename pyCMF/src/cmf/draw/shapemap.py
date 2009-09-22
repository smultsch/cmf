import numpy
import pylab
from shapely.geometry import Polygon,MultiPolygon,Point,LineString,MultiLineString,MultiPoint,GeometryCollection

class shape_map(object):
    """ self.fc_function: A callable taking a feature and returning a color (fillcolor)
    self.lw_function: A callable taking a feature and returning a scalar (line width)
    """
    def refresh(self):
        for i,f in enumerate(self.features):
            for s in self.shapes[i]:
                if self.fc_function and hasattr(s, 'set_fc'):
                    s.set_fc(self.fc_function(f))
                if self.lw_function and hasattr(s, 'set_lw'):
                    s.set_lw(self.lw_function(f))
        if pylab.isinteractive():
            draw()
                      
    def __init__(self,features,**kwargs):
        self.features=features
        self.fc_function=None
        self.lw_function=None
        wasinteractive=pylab.isinteractive()
        if wasinteractive: pylab.ioff()
        self.shapes=[]
        for i,feature in enumerate(self.features):
            if isinstance(feature.shape, MultiPolygon):
                self.shapes.append([])
                for g in feature.shape.geoms:
                    x,y=numpy.asarray(feature.shape.exterior).swapaxes(0,1)
                    self.shapes[-1].append(pylab.fill(x,y,**kwargs)[0])
            if isinstance(feature.shape, Polygon):
                x,y=numpy.asarray(feature.shape.exterior).swapaxes(0,1)
                self.shapes.append(pylab.fill(x,y,**kwargs))
            elif isinstance(feature.shape, MultiLineString):
                self.shapes.append([])
                for g in feature.shape.geoms:
                    x,y=numpy.asarray(feature.shape).swapaxes(0,1)
                    self.shapes[-1].append(pylab.plot(x,y,**kwargs)[0])
            elif isinstance(feature.shape, LineString):
                x,y=numpy.asarray(feature.shape.exterior).swapaxes(0,1)
                self.shapes.append(plot(x,y,**kwargs))
            elif isinstance(feature.shape, Point):
                x,y=feature.shape.x,feature.shape.y
                self.shapes.append(plot([x],[y],**kwargs)[0])
        pylab.axis('equal')
        if wasinteractive:
            pylab.ion()
            pylab.draw()
                
                      

    

    