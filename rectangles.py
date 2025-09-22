import numpy as np
from collections import deque

class RectangleAnalyzer():
    def __init__(self, rectangles:list[dict]):
        """
        Initialize analyzer with list of rectangles.
        Each rectangle is a dict with keys: x, y, width, height
        """
        self.rectangles=rectangles
    
    def find_overlaps(self)->list[tuple]:
        """
        Find all pairs of overlapping rectangles.
        Returns: List of tuples (i, j) where i < j are indices
        Example: [(0, 1), (0, 2), (1, 2)]
        """
        indices=np.triu_indices(len(self.rectangles),k=1) # generates indices from a 2D plan, non-duplicated as taken from a triangle, avoids matching pairs using offset k
        combinations=list(zip(indices[0],indices[1]))
        overlaps=[c for c in combinations if self.rectangles[c[0]]['x']+self.rectangles[c[0]]['width']>self.rectangles[c[1]]['x'] and
                  self.rectangles[c[0]]['x']<self.rectangles[c[1]]['x']+self.rectangles[c[1]]['width'] and
                  self.rectangles[c[0]]['y']+self.rectangles[c[0]]['height']>self.rectangles[c[1]]['y'] and
                  self.rectangles[c[0]]['y']<self.rectangles[c[1]]['y']+self.rectangles[c[1]]['height']]
        return overlaps
    
    def calculate_coverage_area(self)->float:
        """
        Calculate total area covered by all rectangles.
        Overlapping areas should be counted only once.
        Returns: float/int representing total area
        """
        xList=[r['x'] for r in self.rectangles]+[r['x']+r['width'] for r in self.rectangles]
        xs=sorted(set(xList))
        rStack=deque(sorted(self.rectangles, key=lambda r:r['x'], reverse=True))
        xsplitRectangles=[]
        for x in xs:
            z=len(rStack)
            i=0
            while i<z:
                r=rStack.pop()
                if x>r['x'] and x<r['x']+r['width']:
                    # rectangle will be split
                    rB=r.copy()
                    rB['x']=x
                    rB['width']=r['x']+r['width']-x
                    rStack.append(rB)
                    rA=r.copy()
                    rA['width']=x-r['x']
                    rStack.append(rA)
                    z+=2
                elif x==r['x']+r['width']: xsplitRectangles.append(r) # rectangle is added
                else: rStack.appendleft(r) # rectangle is returned to the stack
                i+=1

        mergedRectangles=[]
        rStack=deque(sorted(xsplitRectangles, key=lambda r:r['x'], reverse=True))
        for x in xs[:-1]:
            yRectangles=[]
            r=rStack.pop()
            if x<r['x']: # no rectangle on this x index
                rStack.append(r)
                continue
            while x==r['x']: # pop all rectangles on this x index
                yRectangles.append(r)
                if rStack: r=rStack.pop()
                else: break
            rStack.append(r) # return back the rectangle that does not belong to this x index
            subStack=deque(sorted(yRectangles, key=lambda r:r['y'], reverse=True)) # sort on y axis the rectangles indexed on the same x
            temp=subStack.pop()
            while subStack:
                r=subStack.pop()
                if temp['y']+temp['height']>r['y']+r['height']: continue # rectangle is included in previous one
                elif temp['y']+temp['height']>r['y']: # merge rectangles on the y axis
                    temp['height']=r['y']-temp['y']+r['height']
                else: # nothing to merge
                    mergedRectangles.append(temp)
                    temp=r
            mergedRectangles.append(temp) # one rectangle in the x index
        
        coverage=0
        area=[coverage:=coverage+r['width']*r['height'] for r in mergedRectangles][-1]
        return area
    
    def get_overlap_regions(self)->list[dict]:
        """
        Find actual overlap regions between rectangles.
        Returns: List of dicts containing:
        - 'rect_indices': tuple of rectangle indices
        - 'region': dict with x, y, width, height of overlap
        """
        overlap_regions=[]
        overlaps=self.find_overlaps()
        for pair in overlaps:
            x=max(self.rectangles[pair[0]]['x'],self.rectangles[pair[1]]['x'])
            y=max(self.rectangles[pair[0]]['y'],self.rectangles[pair[1]]['y'])
            width=min(self.rectangles[pair[0]]['x']+self.rectangles[pair[0]]['width'],self.rectangles[pair[1]]['x']+self.rectangles[pair[1]]['width'])-x
            height=min(self.rectangles[pair[0]]['y']+self.rectangles[pair[0]]['height'],self.rectangles[pair[1]]['y']+self.rectangles[pair[1]]['height'])-y
            region={'x':x,'y':y,'width':width,'height':height}
            overlap_regions.append({'rect_indices':pair,'region':region})
        return overlap_regions
    
    def is_point_covered(self, x:int|float, y:int|float)->bool:
        """
        Check if a point is covered by any rectangle.
        Returns: boolean
        """
        for r in self.rectangles:
            if x>=r['x'] and x<=r['x']+r['width'] and y>=r['y'] and y<=r['y']+r['height']: return True
        return False
    
    def find_max_overlap_point(self)->dict:
        """
        Find a point covered by maximum number of rectangles.
        Returns: dict with 'x', 'y', 'count' keys
        Note: will always return the bottom left vertex on a cartesian plan from the max overlapping region
        """
        xList=[r['x'] for r in self.rectangles]+[r['x']+r['width'] for r in self.rectangles]
        xs=sorted(set(xList))
        rStack=deque(sorted(self.rectangles, key=lambda r:r['x'], reverse=True))
        xsplitRectangles=[]
        for x in xs:
            z=len(rStack)
            i=0
            while i<z:
                r=rStack.pop()
                if x>r['x'] and x<r['x']+r['width']:
                    # rectangle will be split
                    rB=r.copy()
                    rB['x']=x
                    rB['width']=r['x']+r['width']-x
                    rStack.append(rB)
                    rA=r.copy()
                    rA['width']=x-r['x']
                    rStack.append(rA)
                    z+=2
                elif x==r['x']+r['width']: xsplitRectangles.append(r) # rectangle is added
                else: rStack.appendleft(r) # rectangle is returned to the stack
                i+=1
        
        points=[]
        rStack=deque(sorted(xsplitRectangles, key=lambda r:r['x'], reverse=True))
        for x in xs[:-1]:
            yRectangles=[]
            r=rStack.pop()
            if x<r['x']: # no rectangle on this x index
                rStack.append(r)
                continue
            while x==r['x']: # pop all rectangles on this x index
                yRectangles.append(r)
                if rStack: r=rStack.pop()
                else: break
            rStack.append(r) # return back the rectangle that does not belong to this x index
            subStack=deque(sorted(yRectangles, key=lambda r:r['y'], reverse=True)) # sort on y axis the rectangles indexed on the same x
            temp=[]
            temp.append(subStack.pop())
            lap=1
            while subStack:
                r=subStack.pop()
                for stacking in temp:
                    if stacking['y']+stacking['height']>r['y']:
                        lap+=1
                points.append({'x':r['x'],'y':r['y'],'count':lap})
                lap=1
                temp.append(r)

        if points==[]: return {'x':r['x'],'y':r['y'],'count':1}
        else: return sorted(points, key=lambda p:p['count'])[-1]

    def get_stats(self)->dict:
        """
        Get coverage statistics.
        Returns: dict with:
        - 'total_rectangles': int
        - 'overlapping_pairs': int
        - 'total_area': float (union area)
        - 'overlap_area': float (sum of all overlap regions)
        - 'coverage_efficiency': float (total_area /
        sum_of_individual_areas)
        """
        overlaps=self.find_overlaps()
        total_area=self.calculate_coverage_area()
        overlap_regions=self.get_overlap_regions()
        area=0
        overlap_area=[area:=area+region['region']['width']*region['region']['height'] for region in overlap_regions][-1]
        area=0
        sum_of_individual_areas=[area:=area+r['width']*r['height'] for r in self.rectangles][-1]
        return {'total_rectangles':len(self.rectangles),'overlapping_pairs':len(overlaps),'total_area':total_area,
                'overlap_area':overlap_area,'coverage_efficiency':total_area/sum_of_individual_areas}



