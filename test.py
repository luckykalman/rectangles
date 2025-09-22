from rectangles import RectangleAnalyzer

rectangles=[
    {'x':1,'y':1,'width':3,'height':2},
    {'x':3,'y':6,'width':1,'height':1},
    {'x':3,'y':2,'width':3,'height':3},
    {'x':8,'y':1,'width':2,'height':4},
    {'x':7,'y':1,'width':5,'height':6},
    {'x':7,'y':4,'width':4,'height':2}
]

test=RectangleAnalyzer(rectangles)

overlaps=test.find_overlaps()
assert overlaps==[(0,2), (3,4), (3,5), (4,5)]

coverage_area=test.calculate_coverage_area()
assert coverage_area==45

overlap_regions=test.get_overlap_regions()
assert overlap_regions==[{'rect_indices': (0,2), 'region': {'x': 3, 'y': 2, 'width': 1, 'height': 1}},
                         {'rect_indices': (3,4), 'region': {'x': 8, 'y': 1, 'width': 2, 'height': 4}},
                         {'rect_indices': (3,5), 'region': {'x': 8, 'y': 4, 'width': 2, 'height': 1}},
                         {'rect_indices': (4,5), 'region': {'x': 7, 'y': 4, 'width': 4, 'height': 2}}]

covered=test.is_point_covered(6,6)
assert(covered==False)
covered=test.is_point_covered(7,7)
assert(covered==True)

max_overlap_point=test.find_max_overlap_point()
assert(max_overlap_point=={'x': 8, 'y': 4, 'count': 3})

stats=test.get_stats()
print(stats)
print('all tests passed')
